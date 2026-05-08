# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025-2026 The Regents of the University of California
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
