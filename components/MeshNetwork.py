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


from .MeshDescriptor import Coordinate, MeshTracker
from .NetworkComponents import RubyNetworkComponent

from m5.objects import SimpleNetwork, RubySystem

from typing import Any


class MeshNetwork(SimpleNetwork, RubyNetworkComponent):
    def __init__(self, ruby_system: RubySystem, mesh_descriptor: MeshTracker) -> None:
        SimpleNetwork.__init__(self=self)
        RubyNetworkComponent.__init__(self=self)

        self.ruby_system = ruby_system
        self.number_of_virtual_networks = ruby_system.number_of_virtual_networks

        self.routers = []
        self.int_links = []
        self.ext_links = []
        self.netifs = []

        self._tile_routers = []
        self._sequencer_tracker = 0
        self._mesh_descriptor = mesh_descriptor

    def get_num_sequencers(self):
        return self._sequencer_tracker

    def get_next_sequencer_id(self):
        self._sequencer_tracker += 1
        return self._sequencer_tracker - 1

    def create_mesh(self) -> None:
        mesh_width = self._mesh_descriptor.get_width()
        mesh_height = self._mesh_descriptor.get_height()

        self._north_links = []
        self._south_links = []
        self._west_links = []
        self._east_links = []

        for y in range(mesh_height):
            for x in range(mesh_width):
                curr_node_coordinate = Coordinate(x, y)
                if not self._mesh_descriptor.has_node(curr_node_coordinate):
                    continue

                # North
                north_neighbor_coordinate = curr_node_coordinate.get_north()
                if self._mesh_descriptor.has_node(north_neighbor_coordinate):
                    self._north_links.append(
                        self.create_int_link(
                            self._mesh_descriptor.get_cross_tile_router(
                                curr_node_coordinate
                            ),
                            self._mesh_descriptor.get_cross_tile_router(
                                north_neighbor_coordinate
                            ),
                        )
                    )

                # South
                south_neighbor_coordinate = curr_node_coordinate.get_south()
                if self._mesh_descriptor.has_node(south_neighbor_coordinate):
                    self._south_links.append(
                        self.create_int_link(
                            self._mesh_descriptor.get_cross_tile_router(
                                curr_node_coordinate
                            ),
                            self._mesh_descriptor.get_cross_tile_router(
                                south_neighbor_coordinate
                            ),
                        )
                    )

                # West
                west_neighbor_coordinate = curr_node_coordinate.get_west()
                if self._mesh_descriptor.has_node(west_neighbor_coordinate):
                    self._west_links.append(
                        self.create_int_link(
                            self._mesh_descriptor.get_cross_tile_router(
                                curr_node_coordinate
                            ),
                            self._mesh_descriptor.get_cross_tile_router(
                                west_neighbor_coordinate
                            ),
                        )
                    )

                # East
                east_neighbor_coordinate = curr_node_coordinate.get_east()
                if self._mesh_descriptor.has_node(east_neighbor_coordinate):
                    self._east_links.append(
                        self.create_int_link(
                            self._mesh_descriptor.get_cross_tile_router(
                                curr_node_coordinate
                            ),
                            self._mesh_descriptor.get_cross_tile_router(
                                east_neighbor_coordinate
                            ),
                        )
                    )

        # gem5 doesn't like empty arrays
        if self._north_links:
            self.north_links = self._north_links
        if self._south_links:
            self.south_links = self._south_links
        if self._west_links:
            self.west_links = self._west_links
        if self._east_links:
            self.east_links = self._east_links
