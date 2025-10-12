# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from m5.objects import ClockDomain
from m5.objects import RubyCache, RubyNetwork, RubyController, RubySystem, NULL

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.processors.abstract_core import AbstractCore
from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode
from .AbstractPickleDeviceNode import AbstractCustomNode


class NoCacheController(AbstractCustomNode):
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
            size="1KiB", # dummy number cache is not used
            assoc=8, # dummy number, cache is not used
        )

        self.sequencer = NULL
        self.ruby_system = ruby_system
        self.use_prefetcher = False
        self.prefetcher = NULL
        self.allow_SD = True
        self.is_HN = False
        self.enable_DMT = False
        self.enable_DCT = False
        # We are not using this cache, so no alloc/dealloc
        self.alloc_on_seq_acc = False
        self.alloc_on_seq_line_write = False
        self.alloc_on_readshared = False
        self.alloc_on_readunique = False
        self.alloc_on_readonce = False
        self.alloc_on_writeback = False
        self.alloc_on_atomic = False
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
