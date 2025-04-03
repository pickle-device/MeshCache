# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from gem5.utils.override import overrides

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.chi.nodes.dma_requestor import DMARequestor
from gem5.components.cachehierarchies.chi.nodes.memory_controller import (
    MemoryController,
)

from m5.objects import (
    SubSystem,
    RubySystem,
    NULL,
    RubyController,
    AddrRange,
    Port,
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
        self._create_links()

    def _create_links(self):
        self.controller_cross_tile_router_link = self.create_ext_link(
            self.controller, self.cross_tile_router
        )
