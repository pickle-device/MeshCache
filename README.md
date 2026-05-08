# MeshCache

A gem5 cache hierarchy configuration for Zen5-like architectures, built on
gem5's CHI (Coherent Hub Interface) ruby framework.

MeshCache models a multi-cluster topology: within each cluster, the cores and
their private caches are connected through a mesh interconnect, and clusters are
linked to one another point-to-point. Coherence is maintained via a
MOESI-like protocol.
