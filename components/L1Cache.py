# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025-2026 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from m5.objects import ClockDomain
from m5.objects import RubyCache, RubyNetwork, RubyController, RubySystem, NULL
from m5.objects import (
    StridePrefetcher,
    IndirectMemoryPrefetcher,
    AccessMapPatternMatching,
    AMPMPrefetcher,
    DifferentialMatchingPrefetcher,
    MultiPrefetcher,
)  # , SmsPrefetcher, BOPPrefetcher
from m5.objects import LRURP

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.processors.abstract_core import AbstractCore
from gem5.components.cachehierarchies.chi.nodes.abstract_node import AbstractNode


class L1Cache(AbstractNode):
    def __init__(
        self,
        size: str,
        associativity: int,
        ruby_system: RubySystem,
        core: AbstractCore,
        cache_line_size: int,
        clk_domain: ClockDomain,
        prefetcher_class: str,
    ):
        super().__init__(ruby_system.network, cache_line_size)

        self.cache = RubyCache(
            size=size,
            assoc=associativity,
            start_index_bit=self.getBlockSizeBits(),
        )
        self.ruby_system = ruby_system
        self.clk_domain = clk_domain
        self.send_evictions = core.requires_send_evicts()
        if prefetcher_class == None or prefetcher_class == "none":
            self.use_prefetcher = False
            self.prefetcher = NULL
        elif prefetcher_class == "imp":
            self.use_prefetcher = True
            self.prefetcher = IndirectMemoryPrefetcher(
                pt_table_entries="256",
                pt_table_assoc=8,
                ipd_table_entries="128",
                ipd_table_assoc=8,
                streaming_distance=4,
                pt_table_replacement_policy=LRURP(),
                ipd_table_replacement_policy=LRURP(),
                queue_size=32,
                max_prefetch_requests_with_pending_translation=32,
            )
        elif prefetcher_class == "stride":
            self.use_prefetcher = True
            self.prefetcher = StridePrefetcher(
                degree=4,
                distance=0,
                table_entries="256",
                table_assoc=8,
                table_replacement_policy=LRURP(),
                queue_size=32,
                max_prefetch_requests_with_pending_translation=32,
            )
        elif prefetcher_class == "ampm":
            self.use_prefetcher = True
            self.prefetcher = AMPMPrefetcher(
                ampm=AccessMapPatternMatching(
                    access_map_table_entries="256",
                    access_map_table_assoc=8,
                    access_map_table_replacement_policy=LRURP(),
                ),
                queue_size=32,
                max_prefetch_requests_with_pending_translation=32,
            )
        elif prefetcher_class == "sms":
            self.use_prefetcher = True
            self.prefetcher = SmsPrefetcher()
        elif prefetcher_class == "bop":
            self.use_prefetcher = True
            self.prefetcher = BOPPrefetcher()
        elif prefetcher_class == "dmp":
            self.use_prefetcher = False
            self.prefetcher = NULL
            self.dmp_prefetcher = DifferentialMatchingPrefetcher(
                clock_domain=clk_domain,
                memory_size="1KiB", # placeholder value
                # will be set after L2 cache intialization in CoreTile
                dmp_prefetch_queue=NULL,
                stride_prefetch_queue=NULL,
                # will be set to this L1 cache in CoreTile
                l1_controller=NULL,
                l2_controller=NULL,
                stride_prefetcher_can_cross_page=False,
                page_size="4KiB",
            )
        elif prefetcher_class == "multiv1":
            self.use_prefetcher = True
            self.prefetcher = MultiPrefetcher(
                prefetchers=[
                    StridePrefetcher(
                        degree=4,
                        distance=0,
                        table_entries="256",
                        table_assoc=8,
                        table_replacement_policy=LRURP(),
                        queue_size=32,
                        max_prefetch_requests_with_pending_translation=32,
                    ),
                    IndirectMemoryPrefetcher(
                        pt_table_entries="256",
                        pt_table_assoc=8,
                        ipd_table_entries="128",
                        ipd_table_assoc=8,
                        streaming_distance=4,
                        pt_table_replacement_policy=LRURP(),
                        ipd_table_replacement_policy=LRURP(),
                        queue_size=32,
                        max_prefetch_requests_with_pending_translation=32,
                    ),
                ]
            )
        else:
            print("Unknown prefetcher")
            assert False
        print("l1", size, prefetcher_class)
        self.is_HN = False
        self.enable_DMT = False
        self.enable_DCT = False
        self.allow_SD = True
        self.fwd_unique_on_readshared = False
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
        self.number_of_TBEs = 16
        self.number_of_repl_TBEs = 16
        self.number_of_snoop_TBEs = 4
        self.number_of_DVM_TBEs = 16
        self.number_of_DVM_snoop_TBEs = 4
        self.unify_repl_TBEs = False
