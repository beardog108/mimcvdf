import sys
import os
sys.path.append('..')
import unittest
from time import time
from hashlib import sha3_256

import mimcvdf

class TestVDF(unittest.TestCase):

    def test_both(self):
        h = mimcvdf.vdf_create(b"test")
        self.assertTrue(mimcvdf.vdf_verify(b"test", h))

    def test_invalid_both(self):
        h = mimcvdf.vdf_create(b"test")
        self.assertFalse(mimcvdf.vdf_verify(b"invalid", h))

    def test_above_zero_rounds(self):
        self.assertRaises(AssertionError, mimcvdf.vdf_create, b"test", 0)
        self.assertRaises(AssertionError, mimcvdf.vdf_create, b"test", -1)
        self.assertRaises(AssertionError, mimcvdf.vdf_create, b"test", 1)
        self.assertRaises(AssertionError, mimcvdf.vdf_create, b"test", -10000)

    def test_dec_false(self):
        for i in range(3):
            h = mimcvdf.vdf_create(os.urandom(i), 2, dec=False)
            self.assertTrue(h.isalnum())
            self.assertTrue(len(h) == 63 or len(h) == 64)
            self.assertIs(type(h), str)

    def test_dec_true(self):
        for i in range(3):
            h = mimcvdf.vdf_create(os.urandom(i), 2, dec=True)
            self.assertIs(type(h), int)

    def test_dec_true_verify(self):
        h = mimcvdf.vdf_create(b"test", dec=True)
        self.assertTrue(mimcvdf.vdf_verify(b"test", h))

    def test_hash_starting_with_zero(self):
        s = b"test vector 1097"
        self.assertEqual(0, sha3_256(s).digest()[0])
        h = mimcvdf.vdf_create(s)
        self.assertTrue(mimcvdf.vdf_verify(s, h))


unittest.main()
