# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from typing import List

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.processors.abstract_core import AbstractCore
from gem5.isas import ISA

from m5.objects import SubSystem, RubySystem, NULL, RubyController, RubySequencer

from .L3Slice import L3Slice
from .MeshDescriptor import Coordinate, MeshTracker
from .Tile import Tile


class L3OnlyTile(Tile):
    def __init__(
        self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        coordinate: Coordinate,
        mesh_descriptor: MeshTracker,
        l3_slice_size: str,
        l3_associativity: int,
        prefetcher_class: str,
        is_home_node: bool = True,
    ) -> None:
        Tile.__init__(
            self=self,
            board=board,
            ruby_system=ruby_system,
            coordinate=coordinate,
            mesh_descriptor=mesh_descriptor,
        )

        self._l3_slice_size = l3_slice_size
        self._l3_associativity = l3_associativity
        self._prefetcher_class = prefetcher_class

        self._create_caches(is_home_node=is_home_node)
        self._create_links()

    def set_l3_downstream_destinations(
        self, destinations: List[RubyController]
    ) -> None:
        # the destinations of each l2_cache should be all of L3 slices / MemCtrl
        self.l3_slice.downstream_destinations = destinations

    def _create_caches(self, is_home_node: bool):
        self.l3_slice = L3Slice(
            size=self._l3_slice_size,
            associativity=self._l3_associativity,
            ruby_system=self._ruby_system,
            cache_line_size=self._board.get_cache_line_size(),
            clk_domain=self._board.get_clock_domain(),
            prefetcher_class=self._prefetcher_class,
            is_home_node=is_home_node,
        )

    def _create_links(self):
        self.l3_router = self.create_router(self._ruby_system)
        self.l3_router_link = self.create_ext_link(self.l3_slice, self.l3_router)
        self.l3_router_to_cross_tile_router_link = self.create_int_link(
            self.l3_router, self.cross_tile_router
        )
        self.cross_tile_router_to_l3_router_link = self.create_int_link(
            self.cross_tile_router, self.l3_router
        )
