import unittest

from client.main import create_parser


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = create_parser()

    def test_foo(self):
        self.assertEqual("foo", "foo")
