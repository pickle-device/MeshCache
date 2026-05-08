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


class SizeArithmetic:
    suffixes = {
        "B": 2**0,
        "KiB": 2**10,
        "MiB": 2**20,
        "GiB": 2**30,
        "TiB": 2**40,
    }
    suffix_order = ["B", "KiB", "MiB", "GiB", "TiB"]

    def __init__(self, raw_form: str):
        self.raw_form = raw_form
        self.bytes = self.parse_to_bytes()

    # parse f"{integer}{unit}" to (integer, unit)
    def parse_to_bytes(self):
        letters = list(self.raw_form)
        idx = len(letters)
        for letter in reversed(letters):
            if letter.isnumeric():
                break
            idx -= 1
        prefix = self.raw_form[:idx]
        suffix = self.raw_form[idx:]
        if not suffix in SizeArithmetic.suffixes:
            print(f"Suffix {suffix} is not supported.")
            assert False
        prefix = int(prefix, 10)
        suffix_magnitude = SizeArithmetic.suffixes[suffix]
        return prefix * suffix_magnitude

    def get_minimal_form(self):
        b = self.bytes
        order = 0
        while b // 1024 > 0:
            b //= 1024
            order += 1
        suffix = SizeArithmetic.suffix_order[order]
        return f"{b}{suffix}"

    def get(self):
        return f"{self.bytes}B"

    def __add__(self, rhs):
        bytes = self.bytes + rhs.bytes
        return SizeArithmetic(f"{bytes}B")

    def __sub__(self, rhs):
        bytes = self.bytes - rhs.bytes
        return SizeArithmetic(f"{bytes}B")

    def __mul__(self, scalar):
        bytes = self.bytes * scalar
        return SizeArithmetic(f"{bytes}B")

    def __floordiv__(self, scalar):
        bytes = self.bytes // scalar
        return SizeArithmetic(f"{bytes}B")

    def __str__(self):
        return self.get()


if __name__ == "__main__":
    s1 = "4096MiB"
    print(s1, "->", SizeArithmetic(s1).get_minimal_form())
    s2 = SizeArithmetic(s1) // 32
    print(f"{s1}/32 ->", s2.get_minimal_form())
