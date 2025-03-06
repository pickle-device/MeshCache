# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.chi.nodes.memory_controller import MemoryController

from m5.objects import SubSystem, RubySystem, NULL, RubyController, AddrRange, Port

from .MeshDescriptor import Coordinate, MeshTracker
from .Tile import Tile

class MemTile(Tile):
    def __init__(self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        coordinate: Coordinate,
        mesh_descriptor: MeshTracker,
        address_range: AddrRange,
        memory_port: Port
    ):
        Tile.__init__(self=self, board=board, ruby_system=ruby_system, coordinate=coordinate, mesh_descriptor=mesh_descriptor)

        self.memory_controller = MemoryController(
            network=ruby_system.network,
            ranges=[address_range],
            port=memory_port
        )
        self.memory_controller.ruby_system = ruby_system
        self._create_links()

    def _create_links(self):
        self.memory_router = self.create_router(self._ruby_system)
        self.memory_router_link = self.create_ext_link(self.memory_controller, self.memory_router)
        self.memory_router_to_cross_tile_router = self.create_int_link(self.memory_router, self.cross_tile_router)
        self.cross_tile_router_to_memory_router = self.create_int_link(self.cross_tile_router, self.memory_router)
