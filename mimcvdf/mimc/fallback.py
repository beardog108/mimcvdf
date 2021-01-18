"""Slow fallback implementation of MIMC written in pure Python."""
"""
This module adapted from https://github.com/OlegJakushkin/deepblockchains/blob/master/vdf/mimc/python/mimc.py by Sourabh Niyogi https://github.com/sourabhniyogi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

is_fast = False

_modulus = 2**256 - 2**32 * 351 + 1
_little_fermat_expt = (_modulus*2-1)//3
_round_constants = [(i**7) ^ 42 for i in range(64)]


def forward_mimc(input_data: bytes, steps: int) -> bytes:
    inp = int.from_bytes(input_data, "big")
    for i in range(1,steps):
        inp = (inp**3 + _round_constants[i % len(_round_constants)]) % _modulus
    return inp.to_bytes((inp.bit_length() + 7) // 8, "big")


def reverse_mimc(input_data: bytes, steps: int) -> bytes:
    rtrace = int.from_bytes(input_data, "big")

    for i in range(steps - 1, 0, -1):
        rtrace = pow(rtrace-_round_constants[i%len(_round_constants)],
                     _little_fermat_expt, _modulus)
    return rtrace.to_bytes((rtrace.bit_length() + 7) // 8, "big")
