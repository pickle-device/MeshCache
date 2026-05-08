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


from m5.objects import ClockDomain, NULL
from m5.objects import RubyCache, RubySystem
from m5.objects import (
    StridePrefetcher,
    IndirectMemoryPrefetcher,
    AccessMapPatternMatching,
    AMPMPrefetcher,
    MultiPrefetcher,
)  # , SmsPrefetcher, BOPPrefetcher
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
        if prefetcher_class == None or prefetcher_class == "none":
            self.use_prefetcher = False
            self.prefetcher = NULL
        elif prefetcher_class == "imp":
            self.use_prefetcher = True
            self.prefetcher = IndirectMemoryPrefetcher(
                pt_table_entries="2048",
                pt_table_assoc=16,
                ipd_table_entries="1024",
                ipd_table_assoc=16,
                streaming_distance=16,
                pt_table_replacement_policy=LRURP(),
                ipd_table_replacement_policy=LRURP(),
                queue_size=128,
                max_prefetch_requests_with_pending_translation=128,
            )
        elif prefetcher_class == "stride":
            self.use_prefetcher = True
            self.prefetcher = StridePrefetcher(
                degree=16,
                distance=0,
                table_entries="2048",
                table_assoc=16,
                table_replacement_policy=LRURP(),
                queue_size=128,
                max_prefetch_requests_with_pending_translation=128,
            )
        elif prefetcher_class == "ampm":
            self.use_prefetcher = True
            self.prefetcher = AMPMPrefetcher(
                ampm=AccessMapPatternMatching(
                    access_map_table_entries="2048",
                    access_map_table_assoc=16,
                    access_map_table_replacement_policy=LRURP(),
                ),
                queue_size=128,
                max_prefetch_requests_with_pending_translation=128,
            )
        elif prefetcher_class == "sms":
            self.use_prefetcher = True
            self.prefetcher = SmsPrefetcher()
        elif prefetcher_class == "bop":
            self.use_prefetcher = True
            self.prefetcher = BOPPrefetcher()
        elif prefetcher_class == "dmp":
            self.use_prefetcher = True
            # The setup of DMP prefetch is a bit special as the prefetch queue
            # needs to be shared between L1D and L2 cache.
            # So, the construction of DMP prefetcher will be done in CoreTile.
            # The current NULL assignment is just a placeholder to make sure
            # the prefetcher is not used before it is properly set up in
            # CoreTile.
            self.prefetcher = NULL
        elif prefetcher_class == "multiv1":
            self.use_prefetcher = True
            self.prefetcher = MultiPrefetcher(
                prefetchers=[
                    StridePrefetcher(
                        degree=20,
                        distance=0,
                        table_entries="2048",
                        table_assoc=16,
                        table_replacement_policy=LRURP(),
                        queue_size=128,
                        max_prefetch_requests_with_pending_translation=128,
                    ),
                    IndirectMemoryPrefetcher(
                        pt_table_entries="2048",
                        pt_table_assoc=16,
                        ipd_table_entries="1024",
                        ipd_table_assoc=16,
                        streaming_distance=16,
                        pt_table_replacement_policy=LRURP(),
                        ipd_table_replacement_policy=LRURP(),
                        queue_size=128,
                        max_prefetch_requests_with_pending_translation=128,
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
        self.number_of_TBEs = 64
        self.number_of_repl_TBEs = 64
        self.number_of_snoop_TBEs = 16
        self.number_of_DVM_TBEs = 64
        self.number_of_DVM_snoop_TBEs = 16
        self.unify_repl_TBEs = False
