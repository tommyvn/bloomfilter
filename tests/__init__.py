from unittest import TestCase
from functools import reduce
from math import exp, ceil
from bloomfilter import union, intersection, element, optimal_hash_runs, optimal_filter_bits, len as bf_len
from bloomfilter import _DEFAULT_HASH_RUNS, _DEFAULT_FILTER_BITS


class TestUtils(TestCase):
    def test_optimal_hash_runs(self):
        self.assertEqual(optimal_hash_runs(2000, 16384), 6)
        self.assertEqual(optimal_hash_runs(200, 4096), 14)
        self.assertEqual(optimal_hash_runs(32, 8096), 175)

    def test_optimal_filter_bits(self):
        self.assertEqual(optimal_filter_bits(1000, 0.01), 9586)
        self.assertEqual(optimal_filter_bits(100, 0.01), 959)


class TestBloomFilter(TestCase):
    def test_element_is_deterministic(self):
        e1 = element(b"element")
        e2 = element(b"element")

        self.assertEqual(e1, e2)

    def test_element_is_int(self):
        e = element(b"element")

        self.assertTrue(type(e) is int)

    def test_intersection_duplicates(self):
        e1 = element(b"element 1")

        self.assertEqual(intersection(e1, e1),
                         e1)

    def test_intersection_unions(self):
        e1 = element(b"element 1")
        e2 = element(b"element 2")
        e3 = element(b"element 3")

        self.assertEqual(intersection(union(e1, e2, e3),
                                      union(e1, e2)),
                         union(e1, e2))

    def test_union_nests(self):
        e1 = element(b"element 1")
        e2 = element(b"element 2")
        e3 = element(b"element 3")

        self.assertEqual(union(e1, e2, e3),
                         union(e1,
                               union(e2, e3)))

    def test_false_positive_rate(self, item_count=1000, bloom_size=_DEFAULT_FILTER_BITS, bloom_hashes=_DEFAULT_HASH_RUNS):
        bloom = reduce(union,
                       map(lambda c: element(c.to_bytes(c.bit_length(), byteorder='big'),
                                             bloom_size,
                                             bloom_hashes),
                           range(item_count)))
        false_positive_probability = pow(1 - exp(-bloom_hashes / (bloom_size / item_count)), bloom_hashes)

        false_positives = 0
        for c in range(item_count * 2):
            new_c = c + item_count
            e = element(new_c.to_bytes(new_c.bit_length(), byteorder='big'),
                        bloom_size,
                        bloom_hashes)
            if intersection(bloom, e) == e:
                false_positives += 1
        false_positive_ratio = false_positives / (item_count * 2)
        max_deviation = false_positive_probability * 0.075
        self.assertAlmostEqual(false_positive_ratio, false_positive_probability, delta=max_deviation)

    def test_false_positive_rate_at_different_settings(self):
        for test_args in (dict(item_count=3000, bloom_size=_DEFAULT_FILTER_BITS * 2, bloom_hashes=_DEFAULT_HASH_RUNS // 2),
                          dict(item_count=300, bloom_size=_DEFAULT_FILTER_BITS // 2, bloom_hashes=_DEFAULT_HASH_RUNS * 2),
                          dict(item_count=1100, bloom_size=_DEFAULT_FILTER_BITS * 2, bloom_hashes=_DEFAULT_HASH_RUNS * 2),
                          dict(item_count=1000, bloom_size=_DEFAULT_FILTER_BITS, bloom_hashes=optimal_hash_runs(2000, _DEFAULT_FILTER_BITS))
                          ):
            with self.subTest(**test_args):
                self.test_false_positive_rate(**test_args)

    def test_len(self):
        bloom = 0b0
        for c in range(1, 1001):
            bloom = union(bloom, element(b"element " + str(c).encode()))
            with self.subTest(c=c):
                self.assertAlmostEqual(bf_len(bloom), c, delta=ceil(c * 0.025))
