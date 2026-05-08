# Copyright (c) 2026 The Regents of the University of California
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


from m5.objects import SubSystem, RubySystem, AddrRange

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
            ruby_system=ruby_system,
            address_ranges=address_ranges,
            cache_line_size=board.get_cache_line_size(),
            clk_domain=board.get_clock_domain(),
        )
        self.global_directory_router = self.create_router(ruby_system)
        self.global_directory_router_link = self.create_ext_link(
            self.global_directory, self.global_directory_router
        )

    def get_address_ranges(self) -> list[AddrRange]:
        return self._address_ranges
