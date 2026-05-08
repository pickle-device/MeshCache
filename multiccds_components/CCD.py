# Copyright (c) 2026 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from math import log2

from gem5.components.boards.abstract_board import AbstractBoard

from m5.objects import (
    RubySystem,
    SubSystem,
    AddrRange,
    RubyCacheBlockTracker,
    RubyDataMovementTracker,
)

from ..components.MeshDescriptor import MeshTracker, NodeType
from ..components.NetworkComponents import RubyNetworkComponent

from ..components.CoreTile import CoreTile
from ..components.L3OnlyTile import L3OnlyTile
from ..components.L3Slice import L3Slice
from ..components.MeshDescriptor import MeshTracker, NodeType
from ..utils.SizeArithmetic import SizeArithmetic


# Will be similar to MeshCache, but this abstraction does not handle
# memory system setup
class CCD(SubSystem, RubyNetworkComponent):
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
        ccd_index: int,
        board: AbstractBoard,
        core_list,  # what type?
        ruby_system: RubySystem,
        mesh_descriptor: MeshTracker,
        data_prefetcher_class: str,
    ) -> None:
        SubSystem.__init__(self=self)
        RubyNetworkComponent.__init__(self=self)

        num_IO_tiles = (
            len(mesh_descriptor.get_tiles_coordinates(NodeType.MemTile))
            + len(mesh_descriptor.get_tiles_coordinates(NodeType.DMATile))
            + len(mesh_descriptor.get_tiles_coordinates(NodeType.FunctionalMemTile))
        )

        assert (
            num_IO_tiles == 0
        ), "In CCD-centric setup, each CCD is not responsible for setting up the memory and IO controllers."

        self._l1i_size = l1i_size
        self._l1i_assoc = l1i_assoc
        self._l1d_size = l1d_size
        self._l1d_assoc = l1d_assoc
        self._l2_size = l2_size
        self._l2_assoc = l2_assoc
        self._l3_size = l3_size
        self._l3_assoc = l3_assoc

        self._ccd_index = ccd_index

        self._board = board
        self._core_list = core_list
        self._ruby_system = ruby_system
        self._cache_line_size = board.get_cache_line_size()
        self._mesh_descriptor = mesh_descriptor
        self._data_prefetcher_class = data_prefetcher_class
        self._has_l3_only_tiles = False

        print("Creating ccd_index:", ccd_index)

        self._create_core_tiles(board, core_list, data_prefetcher_class)
        self._create_l3_only_tiles(board)
        self._assign_addr_range(board)
        self._set_downstream_destinations()
        self._setup_cache_block_tracker(board)

    def get_all_l3_slices(self) -> list[L3Slice]:
        if self._has_l3_only_tiles:
            all_l3_slices = [tile.l3_slice for tile in self.core_tiles] + [
                tile.l3_slice for tile in self.l3_only_tiles
            ]
        else:
            all_l3_slices = [tile.l3_slice for tile in self.core_tiles]
        return all_l3_slices

    def _create_core_tiles(
        self, board: AbstractBoard, core_list, data_prefetcher_class: str  # what type?
    ) -> None:
        core_tile_coordinates = self._mesh_descriptor.get_tiles_coordinates(
            NodeType.CoreTile
        )
        num_l3_slices = self._mesh_descriptor.get_num_l3_slices()
        l3_slice_size = (SizeArithmetic(self._l3_size) // num_l3_slices).get()
        self.core_tiles = [
            CoreTile(
                board=board,
                ruby_system=self._ruby_system,
                coordinate=core_tile_coordinate,
                mesh_descriptor=self._mesh_descriptor,
                core=core,
                core_id=core_id // 2,
                l1i_size=self._l1i_size,
                l1i_associativity=self._l1i_assoc,
                l1d_size=self._l1d_size,
                l1d_associativity=self._l1d_assoc,
                l2_size=self._l2_size,
                l2_associativity=self._l2_assoc,
                l3_slice_size=l3_slice_size,
                l3_associativity=self._l3_assoc,
                pickle_device=[],
                uncacheable_forwarder=[],
                data_prefetcher_class=data_prefetcher_class,
                is_l3_home_node=False,
            )
            for core_id, (core, core_tile_coordinate) in enumerate(
                zip(core_list, core_tile_coordinates)
            )
        ]
        for tile in self.core_tiles:
            self._ruby_system.network.incorporate_ruby_subsystem(tile)

    def _create_l3_only_tiles(self, board: AbstractBoard) -> None:
        l3_only_tiles_coordinates = self._mesh_descriptor.get_tiles_coordinates(
            NodeType.L3OnlyTile
        )
        num_l3_slices = self._mesh_descriptor.get_num_l3_slices()
        l3_slice_size = (SizeArithmetic(self._l3_size) // num_l3_slices).get()
        if len(l3_only_tiles_coordinates) > 0:
            self._has_l3_only_tiles = True
            self.l3_only_tiles = [
                L3OnlyTile(
                    board=board,
                    ruby_system=self._ruby_system,
                    coordinate=tile_coordinate,
                    mesh_descriptor=self._mesh_descriptor,
                    l3_slice_size=l3_slice_size,
                    l3_associativity=self._l3_assoc,
                    prefetcher_class=None,
                )
                for tile_coordinate in l3_only_tiles_coordinates
            ]
            for tile in self.l3_only_tiles:
                self._ruby_system.network.incorporate_ruby_subsystem(tile)

    def _find_board_mem_start(self, board: AbstractBoard) -> None:
        mem_start = 1 << 64
        for r in board.mem_ranges:
            mem_start = min(r.start.value, mem_start)
        return mem_start

    def _assign_addr_range(self, board: AbstractBoard) -> None:
        mem_start = self._find_board_mem_start(board)
        mem_size = board.get_memory().get_size()
        interleaving_size = "4KiB"
        num_offset_bits = int(log2(SizeArithmetic(interleaving_size).bytes))
        all_l3_slices = self.get_all_l3_slices()
        num_l3_slices = len(all_l3_slices)
        num_slice_indexing_bits = int(log2(num_l3_slices))
        address_ranges = [
            AddrRange(
                start=mem_start,
                size=mem_size,
                intlvHighBit=num_offset_bits + num_slice_indexing_bits - 1,
                intlvBits=num_slice_indexing_bits,
                intlvMatch=i,
            )
            for i in range(num_l3_slices)
        ]
        for address_range, l3_slice in zip(address_ranges, all_l3_slices):
            l3_slice.addr_ranges = address_range

    def _set_downstream_destinations(self) -> None:
        all_l3_slices = self.get_all_l3_slices()
        for tile in self.core_tiles:
            tile.set_l2_downstream_destinations(all_l3_slices)

    def _setup_cache_block_tracker(self, board: AbstractBoard) -> None:
        self.cache_block_tracker = RubyCacheBlockTracker(
            ruby_system=self._ruby_system,
        )
        # Add demand requestors for getting requestor IDs
        for core in board.get_processor().get_cores():
            if hasattr(core, "generator"):
                self.cache_block_tracker.addDemandRequestor(core.generator)
            else:
                self.cache_block_tracker.addDemandRequestorWithSubrequestor(
                    core.core, "data"
                )
        # Add prefetcher requestors for getting requestor IDs
        if self._data_prefetcher_class == "dmp":
            for core_tile in self.core_tiles:
                self.cache_block_tracker.addPrefetcherRequestor(
                    core_tile.l1d_cache.dmp_prefetcher.dmp_prefetch_queue
                )
                self.cache_block_tracker.addPrefetcherRequestor(
                    core_tile.l1d_cache.dmp_prefetcher.stride_prefetch_queue
                )
        else:
            for core_tile in self.core_tiles:
                if core_tile.l1d_cache.use_prefetcher:
                    self.cache_block_tracker.addPrefetcherRequestor(
                        core_tile.l1d_cache.prefetcher
                    )
                if core_tile.l2_cache.use_prefetcher:
                    self.cache_block_tracker.addPrefetcherRequestor(
                        core_tile.l2_cache.prefetcher
                    )
        # Add sequencers for probing demand accesses
        for core_tile in self.core_tiles:
            self.cache_block_tracker.addDemandSequencer(core_tile.l1d_cache.sequencer)
        # Add cache controllers for probing LLC directory allocations and LLC cache evictions
        for l3_slice in self.get_all_l3_slices():
            self.cache_block_tracker.addCacheController(l3_slice)

    def setup_data_movement_tracker(self) -> None:
        for core_tile in self.core_tiles:
            core_tile.l1d_cache.data_tracker = RubyDataMovementTracker(
                controller=core_tile.l1d_cache,
                ruby_system=self._ruby_system,
            )
            core_tile.l2_cache.data_tracker = RubyDataMovementTracker(
                controller=core_tile.l2_cache,
                ruby_system=self._ruby_system,
            )
            core_tile.l3_slice.data_tracker = RubyDataMovementTracker(
                controller=core_tile.l3_slice,
                ruby_system=self._ruby_system,
            )
        if self._has_l3_only_tiles:
            for l3_only_tile in self._l3_only_tiles:
                l3_only_tile.l3_slice.data_tracker = RubyDataMovementTracker(
                    controller=l3_only_tile.l3_slice,
                    ruby_system=self._ruby_system,
                )
