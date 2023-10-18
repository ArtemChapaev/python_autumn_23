import unittest

from lru_cache import LRUCache


class TestLRUCahe(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_lru_cache_using(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k2", "val2")

        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k2"), "val2")

    def test_lru_cache_one_item(self):
        cache = LRUCache(1)

        cache.set("k2", "val2")

        self.assertEqual(cache.get("k2"), "val2")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), None)

        cache.set("k1", "val1")

        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k1"), "val1")

    def test_lru_cache_lots_set(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")

        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), "val3")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), "val3")

    def test_lru_cache_error_using(self):
        with self.assertRaises(TypeError) as err:
            LRUCache('0')
            self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            LRUCache(-1)
            self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            LRUCache(1.5)
            self.assertEqual(TypeError, type(err.exception))

        cache = LRUCache(1)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), "val2")


if __name__ == '__main__':
    unittest.main()
