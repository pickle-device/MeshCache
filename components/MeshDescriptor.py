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


from typing import Any, Optional, Tuple, List

from .NetworkComponents import RubyRouter, RubyExtLink


class Coordinate:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_north(self) -> "Coordinate":
        return Coordinate(self.x, self.y - 1)

    def get_south(self) -> "Coordinate":
        return Coordinate(self.x, self.y + 1)

    def get_west(self) -> "Coordinate":
        return Coordinate(self.x - 1, self.y)

    def get_east(self) -> "Coordinate":
        return Coordinate(self.x + 1, self.y)

    def get_hash(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    @classmethod
    def create_coordinate_from_tuple(cls, t) -> "Coordinate":
        return Coordinate(t[0], t[1])


class NodeType:
    EmptyTile = 0
    CoreTile = 1
    L3OnlyTile = 2
    MemTile = 3
    DMATile = 4
    PickleDeviceTile = 5
    FunctionalMemTile = 6  # this is for system ports

    @classmethod
    def to_string(cls, obj: "NodeType") -> str:
        name_map = {
            NodeType.EmptyTile: "EmptyTile",
            NodeType.CoreTile: "CoreTile",
            NodeType.L3OnlyTile: "L3OnlyTile",
            NodeType.MemTile: "MemTile",
            NodeType.DMATile: "DMATile",
            NodeType.PickleDeviceTile: "PickleDeviceTile",
            NodeType.FunctionalMemTile: "FunctionalMemTile",
        }
        return name_map[obj]


class MeshNode:
    def __init__(self, coordinate: Coordinate, node_type: NodeType) -> None:
        self.coordinate = coordinate
        self.node_type = node_type
        self.associated_objects = {}

    def add_associated_objects(self, object_name: str, obj: Any) -> None:
        assert not object_name in self.associated_objects and f"{object_name} exists"
        self.associated_objects[object_name] = obj

    def __str__(self) -> str:
        return f"{str(self.coordinate)}: {NodeType.to_string(self.node_type)}"


class MeshTracker:
    def __init__(self, name: str) -> None:
        self.name = name
        self.grid_tracker = {}
        self.node_cross_tile_router = {}
        # self.node_ext_link = {}

    def add_node(self, coordinate: Coordinate, node_type: NodeType) -> None:
        new_node = MeshNode(coordinate, node_type)
        assert (
            not coordinate.get_hash() in self.grid_tracker
            and "Trying to add an occupied node"
        )
        self.grid_tracker[coordinate.get_hash()] = new_node

    def add_cross_tile_router(self, coordinate: Coordinate, router: RubyRouter) -> None:
        assert (
            coordinate.get_hash() in self.grid_tracker
            and f"Node with coordinate {coordinate} does not exist"
        )
        self.node_cross_tile_router[coordinate.get_hash()] = router

    # def add_ext_link(self, coordinate: Coordinate, ext_link: RubyExtLink) -> None:
    #    assert(coordinate.get_hash() in self.grid_tracker, f"Node with coordinate {coordinate} does not exist")
    #    self.node_ext_link[coordinate.get_hash()] = ext_link
    def get_sorted_coordinate(self) -> List[Coordinate]:
        coor = list(self.grid_tracker.keys())
        width = self.get_width()
        coor = sorted(coor, key=lambda k: k[0] + width * k[1])
        return coor

    def has_node(self, coordinate: Coordinate) -> bool:
        return coordinate.get_hash() in self.grid_tracker

    def get_node(self, coordinate: Coordinate) -> Optional[MeshNode]:
        if not self.has_node(coordinate):
            return None
        return self.grid_tracker[coordinate.get_hash()]

    def get_north_neighbor(self, coordinate: Coordinate) -> Optional[MeshNode]:
        return self.get_node(coordinate.get_north())

    def get_south_neighbor(self, coordinate: Coordinate) -> Optional[MeshNode]:
        return self.get_node(coordinate.get_south())

    def get_west_neighbor(self, coordinate: Coordinate) -> Optional[MeshNode]:
        return self.get_node(coordinate.get_west())

    def get_east_neighbor(self, coordinate: Coordinate) -> Optional[MeshNode]:
        return self.get_node(coordinate.get_east())

    def get_nodes(self) -> List[MeshNode]:
        return list(self.grid_tracker.values())

    def get_cross_tile_router(self, coordinate: Coordinate) -> RubyRouter:
        return self.node_cross_tile_router[coordinate.get_hash()]

    def get_ext_link(self, coordinate: Coordinate) -> RubyExtLink:
        return self.node_ext_link[coordinate.get_hash()]

    def get_tiles_coordinates(self, tile_type: NodeType) -> List[Coordinate]:
        coor = self.get_sorted_coordinate()
        filtered_coor = filter(
            lambda c: self.grid_tracker[c].node_type == tile_type, coor
        )
        return list(map(Coordinate.create_coordinate_from_tuple, filtered_coor))

    def get_num_core_tiles(self):
        return len(self.get_tiles_coordinates(NodeType.CoreTile))

    def get_num_pickle_device_tiles(self):
        return len(self.get_tiles_coordinates(NodeType.PickleDeviceTile))

    def get_num_l3_slices(self):  # tiles that have an L3 slice
        return len(self.get_tiles_coordinates(NodeType.CoreTile)) + len(
            self.get_tiles_coordinates(NodeType.L3OnlyTile)
        )

    def get_num_mem_tiles(self):
        return len(self.get_tiles_coordinates(NodeType.MemTile))

    def get_width(self) -> int:
        max_x = -1
        for x, y in self.grid_tracker.keys():
            max_x = max(x, max_x)
        return max_x + 1

    def get_height(self) -> int:
        max_y = -1
        for x, y in self.grid_tracker.keys():
            max_y = max(y, max_y)
        return max_y + 1

    def __str__(self) -> str:
        s = []
        for coor in self.get_sorted_coordinate():
            s.append(str(self.grid_tracker[coor]))
        return "\n".join(s) + "\n"
