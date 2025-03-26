# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode
from gem5.components.boards.abstract_board import AbstractBoard

from m5.objects import RubySystem, ClockDomain, SubSystem

from .MeshDescriptor import MeshTracker, Coordinate
from .NetworkComponents import RubyRouter, RubyNetworkComponent


class Tile(SubSystem, RubyNetworkComponent):
    def __init__(
        self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        coordinate: Coordinate,
        mesh_descriptor: MeshTracker,
    ) -> None:
        SubSystem.__init__(self=self)
        RubyNetworkComponent.__init__(self=self)

        self._board = board
        self._ruby_system = ruby_system
        self._cache_line_size = board.get_cache_line_size()
        self._mesh_descriptor = mesh_descriptor
        self.add_cross_tile_router(coordinate)

    def add_cross_tile_router(self, coordinate):
        self.cross_tile_router = self.create_router(self._ruby_system)
        self._mesh_descriptor.add_cross_tile_router(coordinate, self.cross_tile_router)
