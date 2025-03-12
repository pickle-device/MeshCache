# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from math import log2
from typing import List

from gem5.utils.requires import requires
from gem5.utils.override import overrides
from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.abstract_board import AbstractBoard

from gem5.components.cachehierarchies.ruby.abstract_ruby_cache_hierarchy import AbstractRubyCacheHierarchy
from gem5.components.cachehierarchies.abstract_three_level_cache_hierarchy import AbstractThreeLevelCacheHierarchy
from gem5.components.cachehierarchies.abstract_cache_hierarchy import AbstractCacheHierarchy
from gem5.components.cachehierarchies.chi.nodes.dma_requestor import DMARequestor
from gem5.components.cachehierarchies.chi.nodes.memory_controller import MemoryController
from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode

from m5.objects import RubySystem, RubyPortProxy, RubySequencer, AddrRange, RubyController, TrafficMux

from .components.CoreTile import CoreTile
from .components.DMATile import DMATile
from .components.L3OnlyTile import L3OnlyTile
from .components.L3Slice import L3Slice
from .components.MemTile import MemTile
from .components.PickleDeviceTile import PickleDeviceTile
from .components.MeshDescriptor import MeshTracker, NodeType
from .components.MeshNetwork import MeshNetwork
from .utils.SizeArithmetic import SizeArithmetic
from .MeshCache import MeshCache

class MeshCacheWithPickleDevice(MeshCache):
    def __init__(
        self,
        l1i_size: str,
        l1i_assoc: int,
        l1d_size: str,
        l1d_assoc: int,
        l2_size: str,
        l2_assoc: int,
        l3_size: str,
        l3_assoc: int,
        num_core_complexes: int,
        is_fullsystem: bool,
        data_prefetcher_class,
        mesh_descriptor: MeshTracker,
        device_cache_size: str,
        device_cache_assoc: int,
    ):
        self._data_prefetcher_class = data_prefetcher_class
        MeshCache.__init__(
            self=self,
            l1i_size=l1i_size,
            l1i_assoc=l1i_assoc,
            l1d_size=l1d_size,
            l1d_assoc=l1d_assoc,
            l2_size=l2_size,
            l2_assoc=l2_assoc,
            l3_size=l3_size,
            l3_assoc=l3_assoc,
            num_core_complexes=num_core_complexes,
            is_fullsystem=is_fullsystem,
            mesh_descriptor=mesh_descriptor
        )
        self._pickle_devices = []
        self._device_cache_size = device_cache_size
        self._device_cache_assoc = device_cache_assoc

    def set_pickle_devices(self, pickle_devices):
        self._pickle_devices = pickle_devices

    def set_traffic_uncacheable_forwarders(self, uncacheable_forwarders):
        self._uncacheable_forwarders = uncacheable_forwarders

    @overrides(MeshCache)
    def _create_core_tiles(self, board: AbstractBoard, pickle_devices, uncacheable_forwarders, data_prefetcher_class) -> None:
        core_tile_coordinates = self._mesh_descriptor.get_tiles_coordinates(NodeType.CoreTile)
        cores = board.get_processor().get_cores()
        num_l3_slices = self._mesh_descriptor.get_num_l3_slices()
        l3_slice_size = (SizeArithmetic(self._l3_size) // num_l3_slices).get()
        self.core_tiles = [CoreTile(
            board = board,
            ruby_system = self.ruby_system,
            coordinate = core_tile_coordinate,
            mesh_descriptor = self._mesh_descriptor,
            core = core,
            core_id = core_id,
            l1i_size = self._l1i_size,
            l1i_associativity = self._l1i_assoc,
            l1d_size = self._l1d_size,
            l1d_associativity = self._l1d_assoc,
            l2_size = self._l2_size,
            l2_associativity = self._l2_assoc,
            l3_slice_size = l3_slice_size,
            l3_associativity = self._l3_assoc,
            pickle_device=pickle_devices[0],
            uncacheable_forwarder=uncacheable_forwarders[core_id],
            data_prefetcher_class=data_prefetcher_class
        ) for core_id, (core, core_tile_coordinate) in enumerate(zip(cores, core_tile_coordinates))]
        for tile in self.core_tiles:
            self.ruby_system.network.incorporate_ruby_subsystem(tile)

    @overrides(MeshCache)
    def incorporate_cache(self, board: AbstractBoard) -> None:
        self._setup_ruby_system()
        self._get_board_info(board)

        self._create_core_tiles(board, self._pickle_devices, self._uncacheable_forwarders, self._data_prefetcher_class)
        self._create_l3_only_tiles(board)
        self._create_memory_tiles(board)
        self._create_dma_tiles(board)
        self._create_pickle_device_component_tiles(board, self._pickle_devices)
        self._assign_addr_range(board)
        self._set_downstream_destinations()
        self.ruby_system.network.create_mesh()
        self._incorperate_system_ports(board)

        self._finalize_ruby_system()

    @overrides(MeshCache)
    def support_pickle_device_tile(self) -> bool:
        return True

    def _create_pickle_device_component_tiles(self, board: AbstractBoard, pickle_devices) -> None:
        pickle_device_tile_coordinates = self._mesh_descriptor.get_tiles_coordinates(NodeType.PickleDeviceTile)
        self.pickle_device_component_tiles = [PickleDeviceTile(
            board = board,
            ruby_system = self.ruby_system,
            coordinate = pickle_device_tile_coordinate,
            mesh_descriptor = self._mesh_descriptor,
            device_cache_size = self._device_cache_size,
            device_cache_assoc = self._device_cache_assoc
        ) for pickle_device_tile_coordinate in pickle_device_tile_coordinates]
        assert(len(pickle_devices) == len(self.pickle_device_component_tiles))
        for pd, tile in zip(pickle_devices, self.pickle_device_component_tiles):
            self.traffic_mux = TrafficMux()
            self.traffic_mux.rsp_ports = pd.request_port
            pd.mmu.connectWalkerPorts(self.traffic_mux.rsp_ports, self.traffic_mux.rsp_ports)
            self.traffic_mux.req_port = tile.controller.sequencer.in_ports
        all_l2_controllers = [tile.l2_cache for tile in self.core_tiles]
        for tile in self.pickle_device_component_tiles:
            self.ruby_system.network.incorporate_ruby_subsystem(tile)

    def post_instantiate(self) -> None:
        pass

    @overrides(MeshCache)
    def _assign_addr_range(self, board: AbstractBoard) -> None:
        MeshCache._assign_addr_range(self, board)
        pickle_device_tile = self.pickle_device_component_tiles[0]
        pickle_device_tile.controller.addr_ranges = [
            AddrRange((1 << 64) - 2, size = 1)
        ]

    @overrides(MeshCache)
    def _set_downstream_destinations(self) -> None:
        all_l3_slices = self._get_all_l3_slices()
        all_mem_ctrls = [mem_tile.memory_controller for mem_tile in self.memory_tiles]
        pickle_device_tile = self.pickle_device_component_tiles[0]
        all_l3_slices_and_pickle_device_tile = all_l3_slices + [pickle_device_tile.controller]
        for tile in self.core_tiles:
            tile.set_l2_downstream_destinations(all_l3_slices_and_pickle_device_tile)
        pickle_device_tile.controller.downstream_destinations = all_l3_slices
        for l3_slice in all_l3_slices:
            l3_slice.downstream_destinations = all_mem_ctrls
        if self._has_dma:
            for tile in self.dma_tiles:
                tile.dma_controller.downstream_destinations = all_l3_slices
