# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from .MeshDescriptor import *


class PrebuiltMesh:
    @classmethod
    def getMesh0(cls, name, has_dma):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x=0, y=0), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=1), NodeType.MemTile)
        if has_dma:
            mesh.add_node(Coordinate(x=1, y=0), NodeType.DMATile)
            mesh.add_node(Coordinate(x=1, y=1), NodeType.DMATile)
        return mesh

    @classmethod
    def getMesh1(cls, name, has_dma):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x=0, y=0), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=0), NodeType.MemTile)
        mesh.add_node(Coordinate(x=0, y=1), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=1), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=3), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=3), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=4), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=4), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=5), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=5), NodeType.MemTile)
        if has_dma:
            mesh.add_node(Coordinate(x=0, y=6), NodeType.DMATile)
            mesh.add_node(Coordinate(x=1, y=6), NodeType.DMATile)
        return mesh

    @classmethod
    def getMesh2(cls, name, has_dma):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x=0, y=0), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=0), NodeType.MemTile)
        mesh.add_node(Coordinate(x=0, y=1), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=1), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=2), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=1, y=2), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=3), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=1, y=3), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=4), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=1, y=4), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=5), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=5), NodeType.MemTile)
        if has_dma:
            mesh.add_node(Coordinate(x=0, y=6), NodeType.DMATile)
            mesh.add_node(Coordinate(x=1, y=6), NodeType.DMATile)
        return mesh

    @classmethod
    def getMesh3(cls, name, has_dma):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x=0, y=0), NodeType.PickleDeviceTile)
        mesh.add_node(Coordinate(x=1, y=0), NodeType.MemTile)
        mesh.add_node(Coordinate(x=0, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=0, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=3), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=3), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=4), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=4), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=5), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=5), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=6), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=6), NodeType.MemTile)
        if has_dma:
            mesh.add_node(Coordinate(x=0, y=7), NodeType.DMATile)
            # mesh.add_node(Coordinate(x = 1, y = 7), NodeType.DMATile)
        return mesh

    @classmethod
    def getMesh4(cls, name, has_dma):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x=0, y=0), NodeType.PickleDeviceTile)
        mesh.add_node(Coordinate(x=0, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=0, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=2), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=3), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=1, y=3), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=4), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=1, y=4), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=5), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=1, y=5), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=6), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=6), NodeType.MemTile)
        if has_dma:
            mesh.add_node(Coordinate(x=0, y=7), NodeType.DMATile)
            mesh.add_node(Coordinate(x=1, y=7), NodeType.DMATile)
        return mesh

    @classmethod
    def getMesh5(cls, name, has_dma):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x=0, y=0), NodeType.PickleDeviceTile)
        mesh.add_node(Coordinate(x=0, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=0, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=3), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=3), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=4), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=4), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=5), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=5), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=6), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=6), NodeType.MemTile)
        if has_dma:
            mesh.add_node(Coordinate(x=0, y=7), NodeType.DMATile)
            mesh.add_node(Coordinate(x=1, y=7), NodeType.DMATile)
        return mesh

    @classmethod
    def getMesh6(cls, name, has_dma):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x=0, y=0), NodeType.PickleDeviceTile)
        mesh.add_node(Coordinate(x=0, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=0, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=2), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=3), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=3), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=4), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=1, y=4), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=5), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=1, y=5), NodeType.L3OnlyTile)
        mesh.add_node(Coordinate(x=0, y=6), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=6), NodeType.MemTile)
        if has_dma:
            mesh.add_node(Coordinate(x=0, y=7), NodeType.DMATile)
            mesh.add_node(Coordinate(x=1, y=7), NodeType.DMATile)
        return mesh

    @classmethod
    def getMesh7(cls, name):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x=0, y=0), NodeType.PickleDeviceTile)
        mesh.add_node(Coordinate(x=1, y=0), NodeType.MemTile)
        mesh.add_node(Coordinate(x=0, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=0, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=2), NodeType.DMATile)
        mesh.add_node(Coordinate(x=0, y=3), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=3), NodeType.MemTile)
        # mesh.add_node(Coordinate(x = 0, y = 4), NodeType.DMATile)
        return mesh

    @classmethod
    def getMesh8(cls, name):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x=0, y=0), NodeType.PickleDeviceTile)
        mesh.add_node(Coordinate(x=1, y=0), NodeType.FunctionalMemTile)
        mesh.add_node(Coordinate(x=0, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=1), NodeType.MemTile)
        mesh.add_node(Coordinate(x=0, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=3), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=3), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=4), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=4), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=5), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=5), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=6), NodeType.MemTile)
        mesh.add_node(Coordinate(x=1, y=6), NodeType.MemTile)
        mesh.add_node(Coordinate(x=0, y=7), NodeType.DMATile)
        return mesh
