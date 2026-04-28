# Copyright (c) 2026 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode

from m5.objects import NULL, RubyCache, RubySystem, ClockDomain, AddrRange


# A global directory is a directory keeping track of all cache lines in every CCD.
# In CHI, every cache controller has some storage so we need to make sure we
# do not store any data here.
class GlobalDirectory(AbstractNode):
    def __init__(
        self,
        ruby_system: RubySystem,
        address_ranges: list[AddrRange],
        cache_line_size: int,
        clk_domain: ClockDomain,
    ):
        super().__init__(ruby_system.network, cache_line_size)
        print("global directory")
        # No storage, just a directory. So we make it a very small cache with 2 lines.
        self.cache = RubyCache(
            size="256B", assoc=2, start_index_bit=self.getBlockSizeBits()
        )
        self.addr_ranges = address_ranges
        self.clk_domain = clk_domain
        self.use_prefetcher = False
        self.prefetcher = NULL
        self.ruby_system = ruby_system
        self.send_evictions = False
        self.sequencer = NULL
        self.is_HN = True
        self.enable_DMT = True # direct memory transfer, only enabled for home node
        self.enable_DCT = True # direct cache transfer, only enabled for home node
        self.allow_SD = True
        self.alloc_on_seq_acc = False
        self.alloc_on_seq_line_write = False
        self.alloc_on_atomic = False
        self.alloc_on_readshared = False
        self.alloc_on_readunique = False
        self.alloc_on_readonce = False
        self.alloc_on_writeback = False
        self.dealloc_on_unique = False
        self.dealloc_on_shared = False
        self.dealloc_backinv_unique = False
        self.dealloc_backinv_shared = False
        self.number_of_TBEs = 1024
        self.number_of_repl_TBEs = 1024
        self.number_of_snoop_TBEs = 256
        self.number_of_DVM_TBEs = 1024
        self.number_of_DVM_snoop_TBEs = 256
        self.unify_repl_TBEs = False
