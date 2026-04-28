# Copyright (c) 2026 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause


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
