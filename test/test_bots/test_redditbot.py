import unittest
import sys
sys.path.append(".")

from rmtibot.redditbot import test_unit


class TestRedditInstance(unittest.TestCase):
    def test_should_pass(self):
        self.assertEqual(test_unit(3), 4, "Set up Reddit Intance.")

if __name__ == "__main__":
    unittest.main()