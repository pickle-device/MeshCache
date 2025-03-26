# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from typing import List

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.processors.abstract_core import AbstractCore
from gem5.isas import ISA

from m5.objects import SubSystem, RubySystem, NULL, RubyController, RubySequencer, TrafficSnooper

from .L1Cache import L1Cache
from .L2Cache import L2Cache
from .L3Slice import L3Slice
from .MeshDescriptor import Coordinate, MeshTracker
from .Tile import Tile

class CoreTile(Tile):
    def __init__(self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        coordinate: Coordinate,
        mesh_descriptor: MeshTracker,
        core: AbstractCore,
        core_id: int,
        l1i_size: str,
        l1i_associativity: int,
        l1d_size: str,
        l1d_associativity: int,
        l2_size: str,
        l2_associativity: int,
        l3_slice_size: str,
        l3_associativity: int,
        pickle_device,
        uncacheable_forwarder,
        data_prefetcher_class: str,
    ) -> None:
        Tile.__init__(self=self, board=board, ruby_system=ruby_system, coordinate=coordinate, mesh_descriptor=mesh_descriptor)

        self._core = core
        self._core_id = core_id
        self._l1i_size = l1i_size
        self._l1i_associativity = l1i_associativity
        self._l1d_size = l1d_size
        self._l1d_associativity = l1d_associativity
        self._l2_size = l2_size
        self._l2_associativity = l2_associativity
        self._l3_slice_size = l3_slice_size
        self._l3_associativity = l3_associativity
        self._pickle_device = pickle_device
        self._uncacheable_forwarder = uncacheable_forwarder
        self._data_prefetcher_class = data_prefetcher_class

        self._create_caches()
        self._create_links()
    
    def set_l2_downstream_destinations(self, destionations: List[RubyController]) -> None:
        # the destinations of each l2_cache should be all of L3 slices / MemCtrl
        self.l2_cache.downstream_destinations = destionations

    def set_l3_downstream_destinations(self, destionations: List[RubyController]) -> None:
        # the destinations of each l2_cache should be all of L3 slices / MemCtrl
        self.l3_slice.downstream_destinations = destionations

    def _create_caches(self):
        self.l1i_cache = L1Cache(
            size = self._l1i_size,
            associativity = self._l1i_associativity,
            ruby_system = self._ruby_system,
            core = self._core,
            cache_line_size = self._board.get_cache_line_size(),
            clk_domain = self._board.get_clock_domain(),
            prefetcher_class = "stride" # always use stride prefetcher
        )

        self.l1d_cache = L1Cache(
            size = self._l1d_size,
            associativity = self._l1d_associativity,
            ruby_system = self._ruby_system,
            core = self._core,
            cache_line_size = self._board.get_cache_line_size(),
            clk_domain = self._board.get_clock_domain(),
            prefetcher_class = self._data_prefetcher_class
        )

        self.l2_cache = L2Cache(
            size = self._l2_size,
            associativity = self._l2_associativity,
            ruby_system = self._ruby_system,
            cache_line_size = self._board.get_cache_line_size(),
            clk_domain = self._board.get_clock_domain(),
            #prefetcher_class = self._data_prefetcher_class
            prefetcher_class = self._data_prefetcher_class
        )

        self.l3_slice = L3Slice(
            size = self._l3_slice_size,
            associativity = self._l3_associativity,
            ruby_system = self._ruby_system,
            cache_line_size = self._board.get_cache_line_size(),
            clk_domain = self._board.get_clock_domain(),
            prefetcher_class = None
        )

        l1i_cache_sequencer_id = self._ruby_system.network.get_next_sequencer_id()
        self.l1i_cache.sequencer = RubySequencer(
            version = l1i_cache_sequencer_id,
            coreid = self._core_id,
            dcache = NULL,
            clk_domain = self.l1i_cache.clk_domain,
            ruby_system = self._ruby_system
        )

        l1d_cache_sequencer_id = self._ruby_system.network.get_next_sequencer_id()
        self.l1d_cache.sequencer = RubySequencer(
            version = l1d_cache_sequencer_id,
            coreid = self._core_id,
            dcache = self.l1d_cache.cache,
            clk_domain = self.l1d_cache.clk_domain,
            ruby_system = self._ruby_system
        )

        if self._board.has_io_bus():
            self.l1d_cache.sequencer.connectIOPorts(self._board.get_io_bus())

        self._core.connect_icache(self.l1i_cache.sequencer.in_ports)
        #self._core.connect_dcache(self.l1d_cache.sequencer.in_ports)
        # add uncacheable_forwarder diverting uncacheable requests of specific ranges to the pickle device
        self._uncacheable_forwarder.in_port = self._core.core.dcache_port
        self._uncacheable_forwarder.out_port = self.l1d_cache.sequencer.in_ports        
        self._uncacheable_forwarder.snoop_port = self._pickle_device.uncacheable_snoop_port

        self._core.connect_walker_ports(
            self.l1i_cache.sequencer.in_ports,
            self.l1d_cache.sequencer.in_ports
        )

        if self._board.get_processor().get_isa() == ISA.X86:
            self._core.connect_interrupt(
                self.l1d_cache.sequencer.interrupt_out_port,
                self.l1d_cache.sequencer.in_ports
            )
        else:
            self._core.connect_interrupt()

        self.l1i_cache.downstream_destinations = [self.l2_cache]
        self.l1d_cache.downstream_destinations = [self.l2_cache]

    def _create_links(self):
        self.intra_tile_router = self.create_router(self._ruby_system)
        self.l1i_router_link = self.create_ext_link(self.l1i_cache, self.intra_tile_router, bandwidth_factor=64)
        self.l1d_router_link = self.create_ext_link(self.l1d_cache, self.intra_tile_router, bandwidth_factor=64)
        self.l2_router_link = self.create_ext_link(self.l2_cache, self.intra_tile_router, bandwidth_factor=64)
        self.intra_tile_router_to_cross_tile_router_link = self.create_int_link(self.intra_tile_router, self.cross_tile_router)
        self.cross_tile_router_to_intra_tile_router_link = self.create_int_link(self.cross_tile_router, self.intra_tile_router)

        self.l3_router = self.create_router(self._ruby_system)
        self.l3_router_link = self.create_ext_link(self.l3_slice, self.l3_router)
        self.l3_router_to_cross_tile_router_link = self.create_int_link(self.l3_router, self.cross_tile_router)
        self.cross_tile_router_to_l3_router_link = self.create_int_link(self.cross_tile_router, self.l3_router)
