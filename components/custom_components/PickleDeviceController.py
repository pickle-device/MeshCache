# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from m5.objects import ClockDomain
from m5.objects import RubyCache, RubyNetwork, RubyController, RubySystem, NULL

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.processors.abstract_core import AbstractCore
from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode
from .AbstractPickleDeviceNode import AbstractCustomNode

class PickleDeviceController(AbstractCustomNode):
    def __init__(
        self,
        ruby_system: RubySystem,
        cache_line_size: int,
        clk_domain: ClockDomain,
        device_cache_size: str,
        device_cache_assoc: int,
    ):
        super().__init__(ruby_system.network, cache_line_size, AbstractNode.versionCount())

        self.clk_domain = clk_domain
        
        self.cache = RubyCache(
            dataAccessLatency=0, tagAccessLatency=1,
            size=device_cache_size, assoc=device_cache_assoc
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
        self.alloc_on_seq_line_write = False
        self.alloc_on_readshared = True
        self.alloc_on_readunique = True
        self.alloc_on_readonce = True
        self.alloc_on_writeback = True
        self.alloc_on_atomic = False
        self.dealloc_on_unique = False
        self.dealloc_on_shared = False
        self.dealloc_backinv_unique = False
        self.dealloc_backinv_shared = False
        self.send_evictions = True
        self.number_of_TBEs = 16
        self.number_of_repl_TBEs = 16
        self.number_of_snoop_TBEs = 4
        self.number_of_DVM_TBEs = 16
        self.number_of_DVM_snoop_TBEs = 4
        self.unify_repl_TBEs = False
