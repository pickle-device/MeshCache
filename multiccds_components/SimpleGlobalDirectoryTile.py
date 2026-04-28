# Copyright (c) 2026 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from m5.objects import SubSystem, RubySystem, AddrRange, Port

from gem5.components.boards.abstract_board import AbstractBoard
from ..components.NetworkComponents import RubyNetworkComponent
from .GlobalDirectory import GlobalDirectory

# Similar to MemTile but does not have cross tile routers
class SimpleGlobalDirectoryTile(SubSystem, RubyNetworkComponent):
    def __init__(
        self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        address_ranges: list[AddrRange],
    ):
        SubSystem.__init__(self=self)
        RubyNetworkComponent.__init__(self=self)
        self._address_ranges = address_ranges

        self.global_directory = GlobalDirectory(
            ruby_system = ruby_system,
            address_ranges = address_ranges,
            cache_line_size = board.get_cache_line_size(),
            clk_domain = board.get_clock_domain(),
        )
        self.global_directory_router = self.create_router(ruby_system)
        self.global_directory_router_link = self.create_ext_link(
            self.global_directory, self.global_directory_router
        )

    def get_address_ranges(self) -> list[AddrRange]:
        return self._address_ranges

