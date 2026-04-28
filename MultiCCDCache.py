# Copyright (c) 2026 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from math import log2
from typing import List, Tuple

from gem5.utils.requires import requires
from gem5.utils.override import overrides
from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.abstract_board import AbstractBoard

from gem5.components.cachehierarchies.ruby.abstract_ruby_cache_hierarchy import (
    AbstractRubyCacheHierarchy,
)
from gem5.components.cachehierarchies.abstract_three_level_cache_hierarchy import (
    AbstractThreeLevelCacheHierarchy,
)
from gem5.components.cachehierarchies.abstract_cache_hierarchy import (
    AbstractCacheHierarchy,
)
from gem5.components.cachehierarchies.chi.nodes.dma_requestor import DMARequestor
from gem5.components.cachehierarchies.chi.nodes.memory_controller import (
    MemoryController,
)
from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode

from m5.objects import (
    RubySystem,
    RubyPortProxy,
    RubySequencer,
    AddrRange,
    RubyCacheBlockTracker,
)

from .multiccds_components.CCD import CCD
from .multiccds_components.IOD import IOD
from .components.MeshDescriptor import MeshTracker, NodeType
from .components.MultiMeshNetwork import MultiMeshNetwork


class MultiCCDCache(AbstractRubyCacheHierarchy, AbstractThreeLevelCacheHierarchy):
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
        num_ccds: int,
        is_fullsystem: bool,
        data_prefetcher_class: str,
        mesh_descriptors: list[MeshTracker],
        num_memory_channels: int,
    ):
        AbstractRubyCacheHierarchy.__init__(self=self)
        AbstractThreeLevelCacheHierarchy.__init__(
            self=self,
            l1i_size=l1i_size,
            l1i_assoc=l1i_assoc,
            l1d_size=l1d_size,
            l1d_assoc=l1d_assoc,
            l2_size=l2_size,
            l2_assoc=l2_assoc,
            l3_size=l3_size,
            l3_assoc=l3_assoc,
        )

        self._data_prefetcher_class = data_prefetcher_class
        self._num_ccds = num_ccds
        self._is_fullsystem = is_fullsystem
        self._mesh_descriptors = mesh_descriptors
        self._num_memory_channels = num_memory_channels
        self._has_dma = False
        self._has_l3_only_tiles = False

        for mesh_descriptor in mesh_descriptors:
            pickle_device_tile_coordinates = mesh_descriptor.get_tiles_coordinates(
                NodeType.PickleDeviceTile
            )
            if (
                len(pickle_device_tile_coordinates) > 0
                and not self.support_pickle_device_tile()
            ):
                print(
                    "MeshCache does not support PickleDeviceTile. However, MeshCacheWithPickleDevice does."
                )
                exit(1)

        requires(coherence_protocol_required=CoherenceProtocol.CHI)

    @overrides(AbstractCacheHierarchy)
    def incorporate_cache(self, board: AbstractBoard) -> None:
        self._setup_ruby_system()
        self._get_board_info(board)

        # This function will create the core tiles and the l3-only tiles.
        self._create_ccds(
            l1i_size=self._l1i_size,
            l1i_assoc=self._l1i_assoc,
            l1d_size=self._l1d_size,
            l1d_assoc=self._l1d_assoc,
            l2_size=self._l2_size,
            l2_assoc=self._l2_assoc,
            l3_size=self._l3_size,
            l3_assoc=self._l3_assoc,
            board=board,
            ruby_system=self.ruby_system,
            mesh_descriptors=self._mesh_descriptors,
            data_prefetcher_class=self._data_prefetcher_class,
        )
        self._create_iod(
            board=board,
            ruby_system=self.ruby_system,
            num_memory_channels=self._num_memory_channels,
            is_fullsystem=self._is_fullsystem,
        )
        self._incorporate_system_ports(board)
        self._set_downstream_destinations(board)
        # self._setup_cache_block_tracker(board)

        self._finalize_ruby_system()

    def support_pickle_device_tile(self) -> bool:
        return False

    def _get_board_info(self, board: AbstractBoard) -> None:
        self._cache_line_size = board.cache_line_size
        self._clk_domain = board.clk_domain

    def _setup_ruby_system(self) -> None:
        self.ruby_system = RubySystem()
        self.ruby_system.number_of_virtual_networks = 4
        self.ruby_system.network = MultiMeshNetwork(
            ruby_system=self.ruby_system, mesh_descriptors=self._mesh_descriptors
        )
        self.ruby_system.network.number_of_virtual_networks = 4
        self.ruby_system.num_of_sequencers = 0

    def _create_ccds(
        self,
        l1i_size: str,
        l1i_assoc: int,
        l1d_size: str,
        l1d_assoc: int,
        l2_size: str,
        l2_assoc: int,
        l3_size: str,
        l3_assoc: int,
        board: AbstractBoard,
        ruby_system: RubySystem,
        mesh_descriptors: list[MeshTracker],
        data_prefetcher_class: str,
    ) -> None:
        cores = board.get_processor().get_cores()
        # partition the cores to each mesh
        core_lists = []
        current_core_index = 0
        for mesh_descriptor in mesh_descriptors:
            num_core_tiles = mesh_descriptor.get_num_core_tiles()
            core_list = cores[current_core_index : current_core_index + num_core_tiles]
            core_lists.append(core_list)
            current_core_index += num_core_tiles
        if current_core_index != len(cores):
            print("Error: The number of cores in the board does not match the total number of core tiles in the mesh descriptors.")
            exit(1)
        self.ccds = [
            CCD(
                l1i_size=l1i_size,
                l1i_assoc=l1i_assoc,
                l1d_size=l1d_size,
                l1d_assoc=l1d_assoc,
                l2_size=l2_size,
                l2_assoc=l2_assoc,
                l3_size=l3_size,
                l3_assoc=l3_assoc,
                ccd_index=ccd_index,
                board=board,
                core_list=core_list,
                ruby_system=ruby_system,
                mesh_descriptor=mesh_descriptor,
                data_prefetcher_class=data_prefetcher_class,
            )
            for ccd_index, core_list in enumerate(core_lists)
        ]
        for ccd in self.ccds:
            self.ruby_system.network.incorporate_ruby_subsystem(ccd)

    def _create_iod(
        self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        num_memory_channels: int,
        is_fullsystem: bool,
    ) -> None:
        self.iod = IOD(
            board=board,
            ruby_system=ruby_system,
            num_memory_channels=num_memory_channels,
            is_fullsystem=is_fullsystem,
        )
        self.ruby_system.network.incorporate_ruby_subsystem(self.iod)

    def _incorporate_system_ports(self, board: AbstractBoard) -> None:
        self.ruby_system.sys_port_proxy = RubyPortProxy()
        self.ruby_system.sys_port_proxy.ruby_system = self.ruby_system
        board.connect_system_port(self.ruby_system.sys_port_proxy.in_ports)

    def _set_downstream_destinations(self, board: AbstractBoard) -> None:
        # Set L3's downstream destination to the global directory
        all_global_directories = self.iod.get_global_directories()
        for ccd in self.ccds:
            for l3_slice in ccd.get_all_l3_slices():
                l3_slice.downstream_destinations = all_global_directories
        # Set global directory's downstream destination to the mem controllers
        all_memory_controllers = [
            memory_controller
            for memory_controller in self.iod.get_memory_controllers()
        ]
        for global_directory in self.iod.get_global_directories():
            global_directory.downstream_destinations = all_memory_controllers
        # Set DMA controller's downstream destination to the global directory
        all_global_directories = self.iod.get_global_directories()
        if hasattr(self.iod, "dma_tiles"):
            for dma_tile in self.iod.dma_tiles:
                dma_tile.dma_controller.downstream_destinations = all_global_directories

    def _finalize_ruby_system(self) -> None:
        self.ruby_system.num_of_sequencers = (
            self.ruby_system.network.get_num_sequencers()
        )
        self.ruby_system.network.int_links = self.ruby_system.network._int_links
        self.ruby_system.network.ext_links = self.ruby_system.network._ext_links
        self.ruby_system.network.routers = self.ruby_system.network._routers
        self.ruby_system.network.setup_buffers()
