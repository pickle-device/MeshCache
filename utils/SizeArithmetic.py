# Copyright (c) 2024 Advanced Micro Devices, Inc.
# Copyright (c) 2025 The Regents of the University of California
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause


class SizeArithmetic:
    suffixes = {
        "B": 2 ** 0,
        "KiB": 2 ** 10,
        "MiB": 2 ** 20,
        "GiB": 2 ** 30,
        "TiB": 2 ** 40,
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
