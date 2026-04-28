# Copyright (c) 2026 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause


from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.chi.nodes.dma_requestor import DMARequestor

from m5.objects import SubSystem, RubySystem, AddrRange, Port, RubySequencer, NULL

from ..components.NetworkComponents import RubyRouter, RubyNetworkComponent

# Similar to DMATile but does not have cross tile routers
class SimpleDMATile(SubSystem, RubyNetworkComponent):
    def __init__(
        self,
        board: AbstractBoard,
        ruby_system: RubySystem,
        dma_port: Port,
    ):
        SubSystem.__init__(self=self)
        RubyNetworkComponent.__init__(self=self)
        self.dma_controller = DMARequestor(
            network=ruby_system.network,
            cache_line_size=board.get_cache_line_size(),
            clk_domain=board.get_clock_domain(),
        )
        self.dma_controller.ruby_system = ruby_system
        self.dma_controller.sequencer = RubySequencer(
            version=self._ruby_system.network.get_next_sequencer_id(),
            in_ports=dma_port,
            dcache=NULL,
            ruby_system=ruby_system,
        )
        self.dma_controller.sequencer.is_cpu_sequencer = False
        self.dma_controller.dealloc_backinv_shared = False
        self.dma_controller.dealloc_backinv_unique = False
        self.dma_controller.alloc_on_atomic = False

        self.dma_router = self.create_router(self._ruby_system)
        self.dma_router_link = self.create_ext_link(
            self.dma_controller, self.dma_router
        )

    def get_dma_router(self) -> RubyRouter:
        return self.dma_router
