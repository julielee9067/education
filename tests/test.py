import unittest


class TestBaseCase(unittest.TestCase):
    def test_foo(self):
        self.assertEqual("foo", "foo")
