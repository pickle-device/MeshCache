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
