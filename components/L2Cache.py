# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from m5.objects import ClockDomain, NULL
from m5.objects import RubyCache, RubyNetwork, RubyController, RubySystem
from m5.objects import StridePrefetcher, IndirectMemoryPrefetcher, AccessMapPatternMatching, AMPMPrefetcher, MultiPrefetcher#, SmsPrefetcher, BOPPrefetcher
from m5.objects import LRURP

from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode

class L2Cache(AbstractNode):
    def __init__(
        self,
        size: str,
        associativity: int,
        ruby_system: RubySystem,
        cache_line_size: int,
        clk_domain: ClockDomain,
        prefetcher_class
    ):
        super().__init__(ruby_system.network, cache_line_size)

        self.cache = RubyCache(
            size=size, assoc=associativity, start_index_bit=self.getBlockSizeBits(),
        )
        self.ruby_system = ruby_system

        self.clk_domain = clk_domain
        if prefetcher_class == None:
            self.use_prefetcher = False
            self.prefetcher = NULL
        elif prefetcher_class == "IMP":
            self.use_prefetcher = True
            self.prefetcher = IndirectMemoryPrefetcher(
                pt_table_entries = "2048",
                pt_table_assoc = 16,
                ipd_table_entries = "1024",
                ipd_table_assoc = 16,
                streaming_distance = 16,
                pt_table_replacement_policy = LRURP(),
                ipd_table_replacement_policy = LRURP(),
                queue_size = 128,
                max_prefetch_requests_with_pending_translation = 128,
            )
        elif prefetcher_class == "Stride":
            self.use_prefetcher = True
            self.prefetcher = StridePrefetcher(
                degree = 20,
                distance = 0,
                table_entries = "2048",
                table_assoc = 16,
                table_replacement_policy = LRURP(),
                queue_size = 128,
                max_prefetch_requests_with_pending_translation = 128,
            )
        elif prefetcher_class == "AMPM":
            self.use_prefetcher = True
            self.prefetcher = AMPMPrefetcher(
                ampm = AccessMapPatternMatching(
                    access_map_table_entries = "2048",
                    access_map_table_assoc = 16,
                    access_map_table_replacement_policy = LRURP(),
                ),
                queue_size = 128,
                max_prefetch_requests_with_pending_translation = 128,
            )
        elif prefetcher_class == "SMS":
            self.use_prefetcher = True
            self.prefetcher = SmsPrefetcher()
        elif prefetcher_class == "BOP":
            self.use_prefetcher = True
            self.prefetcher = BOPPrefetcher()
        elif prefetcher_class == "MultiV1":
            self.use_prefetcher = True
            self.prefetcher = MultiPrefetcher(
                prefetchers = [
                    StridePrefetcher(
                        degree = 20,
                        distance = 0,
                        table_entries = "2048",
                        table_assoc = 16,
                        table_replacement_policy = LRURP(),
                        queue_size = 128,
                        max_prefetch_requests_with_pending_translation = 128,
                    ),
                    IndirectMemoryPrefetcher(
                        pt_table_entries = "2048",
                        pt_table_assoc = 16,
                        ipd_table_entries = "1024",
                        ipd_table_assoc = 16,
                        streaming_distance = 16,
                        pt_table_replacement_policy = LRURP(),
                        ipd_table_replacement_policy = LRURP(),
                        queue_size = 128,
                        max_prefetch_requests_with_pending_translation = 128,
                    ),
                ]
            )
        else:
            print("Unknown prefetcher")
            assert False
        print("l2", size, prefetcher_class)
        self.send_evictions = False
        self.sequencer = NULL
        self.is_HN = False
        self.enable_DMT = False
        self.enable_DCT = False
        self.allow_SD = True
        self.fwd_unique_on_readshared = False
        self.alloc_on_seq_acc = False
        self.alloc_on_seq_line_write = False
        self.alloc_on_atomic = True
        self.alloc_on_readshared = True
        self.alloc_on_readunique = True
        self.alloc_on_readonce = True
        self.dealloc_on_unique = False
        self.dealloc_on_shared = False
        self.dealloc_backinv_unique = True
        self.dealloc_backinv_shared = True
        self.alloc_on_writeback = False
        self.number_of_TBEs = 16
        self.number_of_repl_TBEs = 16
        self.number_of_snoop_TBEs = 4
        self.number_of_DVM_TBEs = 16
        self.number_of_DVM_snoop_TBEs = 4
        self.unify_repl_TBEs = False
