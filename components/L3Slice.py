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


from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode

from m5.objects import NULL, RubyCache
from m5.objects import (
    StridePrefetcher,
    IndirectMemoryPrefetcher,
    AccessMapPatternMatching,
    AMPMPrefetcher,
)  # , SmsPrefetcher, BOPPrefetcher


class L3Slice(AbstractNode):
    def __init__(
        self,
        size,
        associativity,
        ruby_system,
        cache_line_size,
        clk_domain,
        prefetcher_class,
        is_home_node,
    ):
        super().__init__(ruby_system.network, cache_line_size)
        self.cache = RubyCache(
            size=size, assoc=associativity, start_index_bit=self.getBlockSizeBits()
        )
        self.clk_domain = clk_domain
        self.use_prefetcher = False
        self.ruby_system = ruby_system

        self.send_evictions = False
        if prefetcher_class == None:
            self.use_prefetcher = False
            self.prefetcher = NULL
        elif prefetcher_class == "IMP":
            self.use_prefetcher = True
            self.prefetcher = IndirectMemoryPrefetcher()
        elif prefetcher_class == "Stride":
            self.use_prefetcher = True
            self.prefetcher = StridePrefetcher()
        elif prefetcher_class == "AMPM":
            self.use_prefetcher = True
            self.prefetcher = AMPMPrefetcher()
        elif prefetcher_class == "SMS":
            self.use_prefetcher = True
            self.prefetcher = SmsPrefetcher()
        elif prefetcher_class == "BOP":
            self.use_prefetcher = True
            self.prefetcher = BOPPrefetcher()
        else:
            print("Unknown prefetcher")
            assert False
        print("l3", size, prefetcher_class)
        self.sequencer = NULL
        self.prefetcher = NULL
        self.is_HN = is_home_node
        self.enable_DMT = is_home_node
        self.enable_DCT = is_home_node
        self.allow_SD = True
        self.alloc_on_seq_acc = False
        self.alloc_on_seq_line_write = False
        self.alloc_on_atomic = False
        self.alloc_on_readshared = False
        self.alloc_on_readunique = False
        self.alloc_on_readonce = False
        self.alloc_on_writeback = True  # Victim cache
        self.dealloc_on_unique = False
        self.dealloc_on_shared = False  # True?
        self.dealloc_backinv_unique = False
        self.dealloc_backinv_shared = False
        self.number_of_TBEs = 256
        self.number_of_repl_TBEs = 256
        self.number_of_snoop_TBEs = 64
        self.number_of_DVM_TBEs = 256
        self.number_of_DVM_snoop_TBEs = 64
        self.unify_repl_TBEs = False
