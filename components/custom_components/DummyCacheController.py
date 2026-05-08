# Copyright (c) 2025 The Regents of the University of California
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

from m5.objects import ClockDomain
from m5.objects import RubyCache, RubyNetwork, RubyController, RubySystem, NULL

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.processors.abstract_core import AbstractCore
from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode
from .AbstractPickleDeviceNode import AbstractCustomNode


# A small cache acting as no-storage cache
class DummyCacheController(AbstractCustomNode):
    def __init__(
        self,
        ruby_system: RubySystem,
        cache_line_size: int,
        clk_domain: ClockDomain,
    ):
        super().__init__(
            ruby_system.network, cache_line_size, AbstractNode.versionCount()
        )

        self.clk_domain = clk_domain

        self.cache = RubyCache(
            dataAccessLatency=0,
            tagAccessLatency=1,
            size="256B",  # using the smallest amount of cache that works
            assoc=2,
        )

        self.sequencer = NULL
        self.ruby_system = ruby_system
        self.use_prefetcher = False
        self.prefetcher = NULL
        self.allow_SD = True
        self.is_HN = False
        self.enable_DMT = False
        self.enable_DCT = False
        self.alloc_on_seq_acc = True
        self.alloc_on_seq_line_write = True
        self.alloc_on_readshared = True
        self.alloc_on_readunique = True
        self.alloc_on_readonce = True
        self.alloc_on_writeback = False
        self.alloc_on_atomic = True
        self.dealloc_on_unique = False
        self.dealloc_on_shared = False
        self.dealloc_backinv_unique = False
        self.dealloc_backinv_shared = False
        self.send_evictions = True
        # These hold the number of outstanding requests
        self.number_of_TBEs = 128
        self.number_of_repl_TBEs = 128
        self.number_of_snoop_TBEs = 128
        self.number_of_DVM_TBEs = 128
        self.number_of_DVM_snoop_TBEs = 128
        self.unify_repl_TBEs = False
