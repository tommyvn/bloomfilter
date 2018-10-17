from functools import reduce
import hashlib
from typing import Callable
from math import log, ceil


_DEFAULT_FILTER_BITS: int = 32*256
_DEFAULT_HASH_RUNS: int = 32


def sha256_hash_fun(e: bytes, c: int) -> int:
    to_hash = bytes([c]) + e
    sha256_obj = hashlib.sha256(to_hash)
    n = int.from_bytes(sha256_obj.digest(), 'little')
    return n


def optimal_hash_runs(total_items: int,
                      filter_bits: int = _DEFAULT_FILTER_BITS) -> int:
    return round((filter_bits / total_items) * log(2))


def optimal_filter_bits(total_items: int,
                        error_rate: int) -> int:
    return ceil((total_items * log(error_rate)) / log(1 / pow(2, log(2))))


def len(bloomfilter: int,
        filter_bits: int = _DEFAULT_FILTER_BITS,
        hash_runs: int = _DEFAULT_HASH_RUNS) -> float:
    return -filter_bits / hash_runs * log(1 - bin(bloomfilter).count("1") / filter_bits)  # sad face about the .count()


def element(b: bytes,
            filter_bits: int = _DEFAULT_FILTER_BITS,
            hash_runs: int = _DEFAULT_HASH_RUNS,
            hash_funs: Callable[[bytes, int], int] = sha256_hash_fun) -> int:
    bloom = 0b0
    for c in range(hash_runs):
        n = hash_funs(b, c)
        bloom = bloom | (0b1 << n % filter_bits)
    return bloom


def union(*bloomfilters: int) -> int:
    return reduce(lambda a, b: a | b, bloomfilters)


def intersection(*bloomfilters: int) -> int:
    return reduce(lambda a, b: a & b, bloomfilters)


__all__ = ["element", "union", "intersection", "len",
           "optimal_hash_runs", "optimal_filter_bits"]
