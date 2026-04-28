# Copyright (c) 2026 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from math import log2

from MeshCache.multiccds_components import SimpleGlobalDirectoryTile

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode
from gem5.components.cachehierarchies.chi.nodes.memory_controller import (
    MemoryController,
)

from m5.objects import RubySystem, ClockDomain, SubSystem, AddrRange

from ..components.MeshDescriptor import MeshTracker, Coordinate, NodeType
from ..components.NetworkComponents import RubyRouter, RubyNetworkComponent

from .GlobalDirectory import GlobalDirectory
from .SimpleDMATile import SimpleDMATile
from .SimpleGlobalDirectoryTile import SimpleGlobalDirectoryTile
from .SimpleMemTile import SimpleMemTile
from ..components.MeshDescriptor import MeshTracker, NodeType
from ..components.MeshNetwork import MeshNetwork
from ..components.NetworkComponents import RubyRouter
from ..utils.SizeArithmetic import SizeArithmetic

# Will be similar to MeshCache, but this abstraction does not handle
# memory system setup
class IOD(SubSystem, RubyNetworkComponent):
    def __init__(
        self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        num_memory_channels: int,
        is_fullsystem: bool,
    ) -> None:
        SubSystem.__init__(self=self)
        RubyNetworkComponent.__init__(self=self)

        self._board = board
        self._ruby_system = ruby_system
        self._num_memory_channels = num_memory_channels

        self._create_mem_tiles(board, ruby_system, is_fullsystem)
        self._create_global_directory_tiles(board, ruby_system)
        self._link_mem_tiles_to_global_directory()
        self._create_dma_tiles(board, ruby_system, is_fullsystem)
        # we are not using the DMA controllers, and I don't know what's the best
        # way to set up the links between the DMA tiles and the
        # global directory / memory tiles, so I'll just connect the DMA tiles
        # to the global directory for now.
        self._link_dma_tiles_to_global_directory()

    def get_global_directories(self) -> list[GlobalDirectory]:
        return [tile.global_directory for tile in self.global_directory_tiles]

    def get_memory_controllers(self) -> list[MemoryController]:
        return [tile.memory_controller for tile in self.mem_tiles]

    def _create_mem_tiles(self, board: AbstractBoard, ruby_system: RubySystem, is_fullsystem: bool):
        if is_fullsystem:
            functional_mem_ports = board.get_mem_ports()[:1]
            mem_ports = board.get_mem_ports()[1:]
        else:
            functional_mem_ports = []
            mem_ports = board.get_mem_ports()

        # create memory tile for each memory port
        self.mem_tiles = [
            SimpleMemTile(
                ruby_system = ruby_system,
                address_range = address_range,
                memory_port = memory_port,
            )
            for address_range, memory_port in mem_ports
        ]
        for tile in self.mem_tiles:
            self.incorporate_ruby_subsystem(tile)

        # create functional memory tiles if full system
        if functional_mem_ports:
            functional_mem_address_range, functional_mem_port = functional_mem_ports[0]
            self.functional_memory_tile = SimpleMemTile(
                ruby_system=ruby_system,
                address_range=functional_mem_address_range,
                memory_port=functional_mem_port
            )
            self.incorporate_ruby_subsystem(self.functional_memory_tile)

    def _create_global_directory_tiles(self, board: AbstractBoard, ruby_system: RubySystem):
        # create global directory tile
        self.global_directory_tiles = [
            SimpleGlobalDirectoryTile(
                board=board,
                ruby_system=ruby_system,
                address_ranges=mem_tile.get_address_range(),
            ) for mem_tile in self.mem_tiles
        ]
        for tile in self.global_directory_tiles:
            self.incorporate_ruby_subsystem(tile)

    def _link_mem_tiles_to_global_directory(self):
        for mem_tile, global_directory_tile in zip(self.mem_tiles, self.global_directory_tiles):
            mem_tile.memory_router_to_global_directory_link = self.create_int_link(
                mem_tile.memory_router, global_directory_tile.global_directory_router
            )
            mem_tile.global_directory_router_to_memory_link = self.create_int_link(
                global_directory_tile.global_directory_router, mem_tile.memory_router
            )

    def _create_dma_tiles(self, board: AbstractBoard, ruby_system: RubySystem, is_fullsystem: bool):
        if not board.has_dma_ports():
            return
        self.dma_tiles = [
            SimpleDMATile(
                board=board,
                ruby_system=ruby_system,
                dma_port=dma_port,
            )
            for dma_port in board.get_dma_ports()
        ]
        for tile in self.dma_tiles:
            self.incorporate_ruby_subsystem(tile)

    def _link_dma_tiles_to_global_directory(self):
        if not hasattr(self, "dma_tiles"):
            return
        for dma_tile in self.dma_tiles:
            dma_tile.dma_router_to_global_directory_link = self.create_int_link(
                dma_tile.dma_router, self.global_directory_tiles[0].global_directory_router
            )
            dma_tile.global_directory_router_to_dma_link = self.create_int_link(
                self.global_directory_tiles[0].global_directory_router, dma_tile.dma_router
            )
