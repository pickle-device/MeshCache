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

from m5.objects import (
    RubySystem,
    RubySequencer,
)

from .MeshDescriptor import Coordinate, MeshTracker
from .Tile import Tile
from .custom_components.PickleDeviceController import PickleDeviceController


class PickleDeviceTile(Tile):
    def __init__(
        self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        coordinate: Coordinate,
        mesh_descriptor: MeshTracker,
        device_cache_size: str,
        device_cache_assoc: int,
        num_tbes: int,
    ):
        Tile.__init__(
            self=self,
            board=board,
            ruby_system=ruby_system,
            coordinate=coordinate,
            mesh_descriptor=mesh_descriptor,
        )
        self.controller = PickleDeviceController(
            ruby_system=self._ruby_system,
            cache_line_size=self._board.get_cache_line_size(),
            clk_domain=self._board.get_clock_domain(),
            device_cache_size=device_cache_size,
            device_cache_assoc=device_cache_assoc,
            num_tbes=num_tbes,
        )
        device_sequencer_id = self._ruby_system.network.get_next_sequencer_id()
        self.controller.sequencer = RubySequencer(
            version=device_sequencer_id,
            coreid=99,
            dcache=self.controller.cache,
            clk_domain=self.controller.clk_domain,
            ruby_system=self._ruby_system,
        )
        self.controller.sequencer.max_outstanding_requests = num_tbes
        self._create_links()

    def _create_links(self):
        self.controller_cross_tile_router_link = self.create_ext_link(
            self.controller,
            self.cross_tile_router,
        )
