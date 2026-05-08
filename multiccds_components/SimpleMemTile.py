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


from gem5.components.cachehierarchies.chi.nodes.memory_controller import (
    MemoryController,
)

from m5.objects import SubSystem, RubySystem, AddrRange, Port

from ..components.NetworkComponents import RubyRouter, RubyNetworkComponent

# Similar to MemTile but does not have cross tile routers
class SimpleMemTile(SubSystem, RubyNetworkComponent):
    def __init__(
        self,
        ruby_system: RubySystem,
        address_range: AddrRange,
        memory_port: Port,
    ):
        SubSystem.__init__(self=self)
        RubyNetworkComponent.__init__(self=self)
        self._address_range = address_range

        self.memory_controller = MemoryController(
            network=ruby_system.network, ranges=[address_range], port=memory_port
        )
        self.memory_controller.ruby_system = ruby_system
        self.memory_router = self.create_router(ruby_system)
        self.memory_router_link = self.create_ext_link(
            self.memory_controller, self.memory_router
        )

    def get_address_range(self) -> AddrRange:
        return self._address_range

    def get_memory_router(self) -> RubyRouter:
        return self.memory_router
