# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from abc import abstractmethod
from gem5.isas import ISA
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.abstract_core import AbstractCore

from m5.objects import Cache_Controller, MessageBuffer, RubyNetwork

import math


class TriggerMessageBuffer(MessageBuffer):
    """
    MessageBuffer for triggering internal controller events.
    These buffers should not be affected by the Ruby tester randomization
    and allow poping messages enqueued in the same cycle.
    """

    randomization = "disabled"
    allow_zero_latency = True


class OrderedTriggerMessageBuffer(TriggerMessageBuffer):
    ordered = True


class AbstractCustomNode(Cache_Controller):
    """A node is the abstract unit for caches in the CHI protocol.

    You can extend the AbstractNode to create caches (private or shared) and
    directories with or without data caches.
    """

    _version = 0

    # TODO: I don't love that we have to pass in the cache line size.
    # However, we need some way to set the index bits
    def __init__(
        self, network: RubyNetwork, cache_line_size: int, ruby_version_count: int
    ):
        super().__init__()

        # Note: Need to call versionCount method on *this* class, not the
        # potentially derived class
        self.version = ruby_version_count
        self._cache_line_size = cache_line_size

        # Set somewhat large number since we really a lot on internal
        # triggers. To limit the controller performance, tweak other
        # params such as: input port buffer size, cache banks, and output
        # port latency
        self.transitions_per_cycle = 1024
        # This should be set to true in the data cache controller to enable
        # timeouts on unique lines when a store conditional fails
        self.sc_lock_enabled = False

        # Use 32-byte channels (two flits per message)
        self.data_channel_size = 32

        # Use near atomics (see: https://github.com/gem5/gem5/issues/449)
        self.policy_type = 0

        self.connectQueues(network)

    def getBlockSizeBits(self):
        bits = int(math.log(self._cache_line_size, 2))
        if 2 ** bits != self._cache_line_size.value:
            raise Exception("Cache line size not a power of 2!")
        return bits

    def connectQueues(self, network: RubyNetwork):
        """Connect all of the queues for this controller.
        This may be extended in subclasses.
        """
        self.mandatoryQueue = MessageBuffer()
        self.prefetchQueue = MessageBuffer()

        self.triggerQueue = TriggerMessageBuffer()
        self.retryTriggerQueue = OrderedTriggerMessageBuffer()
        self.replTriggerQueue = OrderedTriggerMessageBuffer()
        self.reqRdy = TriggerMessageBuffer()
        self.snpRdy = TriggerMessageBuffer()

        self.reqOut = MessageBuffer()
        self.rspOut = MessageBuffer()
        self.snpOut = MessageBuffer()
        self.datOut = MessageBuffer()
        self.reqIn = MessageBuffer()
        self.rspIn = MessageBuffer()
        self.snpIn = MessageBuffer()
        self.datIn = MessageBuffer()
        self.reqOut.out_port = network.in_port
        self.rspOut.out_port = network.in_port
        self.snpOut.out_port = network.in_port
        self.datOut.out_port = network.in_port
        self.reqIn.in_port = network.out_port
        self.rspIn.in_port = network.out_port
        self.snpIn.in_port = network.out_port
        self.datIn.in_port = network.out_port
