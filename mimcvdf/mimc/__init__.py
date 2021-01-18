"""Mimc hash function."""

try:
    from .native import forward_mimc, reverse_mimc
    is_fast = True
except ImportError:
    from .fallback import forward_mimc, reverse_mimc
    is_fast = False
