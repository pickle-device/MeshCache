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
