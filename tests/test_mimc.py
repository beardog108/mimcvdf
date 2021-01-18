import sys
import os
sys.path.append('..')
import unittest
import time
from hashlib import sha3_256

import mimcvdf.mimc

class TestMimc(unittest.TestCase):

    def test_bytes(self):
        start = time.time()
        data = b"a" * 6000000
        h = sha3_256()
        h.update(data)
        data = h.digest()

        forw = mimcvdf.forward_mimc(data, 2000)

        rev = mimcvdf.reverse_mimc(forw, 2000)

        print(data.hex())
        print(forw.hex(), rev.hex())
        self.assertEqual(rev, data)

    def test_expected_data(self):
        h = sha3_256()
        h.update(b"test")
        data = h.digest()
        self.assertEqual(
            "66ea2a863bd103f2c7f190503cf8456198f31660069d4903afbd5f2e40a28695",
            mimcvdf.forward_mimc(data, 2000).hex()
        )

unittest.main()
