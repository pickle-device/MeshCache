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

    @classmethod
    def getMesh9(cls, name):
        mesh = MeshTracker(name=name)
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
        return mesh

    @classmethod
    def getMesh10(cls, name):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x=0, y=0), NodeType.PickleDeviceTile)
        mesh.add_node(Coordinate(x=1, y=0), NodeType.FunctionalMemTile)
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
        mesh.add_node(Coordinate(x=0, y=7), NodeType.DMATile)
        return mesh


    @classmethod
    def getMesh11(cls, name):
        mesh = MeshTracker(name=name)
        mesh.add_node(Coordinate(x=0, y=0), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=0), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=1), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=1), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=2), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=0, y=3), NodeType.CoreTile)
        mesh.add_node(Coordinate(x=1, y=3), NodeType.CoreTile)
        return mesh