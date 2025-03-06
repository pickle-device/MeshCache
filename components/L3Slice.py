# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode

from m5.objects import NULL, RubyCache
from m5.objects import StridePrefetcher, IndirectMemoryPrefetcher, AccessMapPatternMatching, AMPMPrefetcher#, SmsPrefetcher, BOPPrefetcher

class L3Slice(AbstractNode):
    def __init__(self, size, associativity, ruby_system, cache_line_size, clk_domain, prefetcher_class):
        super().__init__(ruby_system.network, cache_line_size)
        self.cache = RubyCache(size=size, assoc=associativity, start_index_bit=self.getBlockSizeBits())
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
        self.is_HN = True
        self.enable_DMT = True
        self.enable_DCT = True
        self.allow_SD = True
        self.alloc_on_seq_acc = False
        self.alloc_on_seq_line_write = False
        self.alloc_on_atomic = False
        self.alloc_on_readshared = False
        self.alloc_on_readunique = False
        self.alloc_on_readonce = False
        self.alloc_on_writeback = True # Victim cache
        self.dealloc_on_unique = False
        self.dealloc_on_shared = False # True?
        self.dealloc_backinv_unique = False
        self.dealloc_backinv_shared = False
        self.number_of_TBEs = 128
        self.number_of_repl_TBEs = 128
        self.number_of_snoop_TBEs = 4
        self.number_of_DVM_TBEs = 16
        self.number_of_DVM_snoop_TBEs = 4
        self.unify_repl_TBEs = False
