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


from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.chi.nodes.memory_controller import (
    MemoryController,
)

from m5.objects import RubySystem, AddrRange, Port

from .MeshDescriptor import Coordinate, MeshTracker
from .Tile import Tile


class MemTile(Tile):
    def __init__(
        self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        coordinate: Coordinate,
        mesh_descriptor: MeshTracker,
        address_range: AddrRange,
        memory_port: Port,
    ):
        Tile.__init__(
            self=self,
            board=board,
            ruby_system=ruby_system,
            coordinate=coordinate,
            mesh_descriptor=mesh_descriptor,
        )

        self.memory_controller = MemoryController(
            network=ruby_system.network, ranges=[address_range], port=memory_port
        )
        self.memory_controller.ruby_system = ruby_system
        self._create_links()

    def _create_links(self):
        self.memory_router = self.create_router(self._ruby_system)
        self.memory_router_link = self.create_ext_link(
            self.memory_controller, self.memory_router
        )
        self.memory_router_to_cross_tile_router = self.create_int_link(
            self.memory_router, self.cross_tile_router
        )
        self.cross_tile_router_to_memory_router = self.create_int_link(
            self.cross_tile_router, self.memory_router
        )
