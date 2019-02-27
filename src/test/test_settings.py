import unittest
from settings import Settings
from unittest.mock import Mock


class TestSettings(unittest.TestCase):

    def test_get_type(self):
        a = 'a'
        self.assertIsInstance(Settings.get_type(a), str, "The 'get_type(cls, attribute: any)' " +
                              "method does not return a string.")
        self.assertNotRegex(Settings.get_type(a), r"<+", msg="The return value of the 'get_type(attribute: str)' " +
                                                             "method contains a '<' character")
        self.assertNotRegex(Settings.get_type(a), r"\s+", msg="The return value of the 'get_type(attribute: str)' " +
                                                              "method contains a '<space>' character")
        self.assertNotRegex(Settings.get_type(a), r">+", msg="The return value of the 'get_type(attribute: str)' " +
                                                             "method contains a '>' character")

    def test_changing_a_setting(self):
        before = Settings.revealLettersRatio
        set_to = 1.0
        self.assertNotEqual(before, set_to)
        after = Settings.change('revealLettersRatio', set_to)
        self.assertNotEqual(before, after)

    def test_changing_a_setting_throws_an_exception(self):
        with self.assertRaises(AttributeError, msg="The 'change(cls, setting: str, value: any)' " +
                                                   "method does not raise an 'AttributeError' " +
                                                   "when trying to access a non-existent attribute"):
            Settings.change('someSettings', 1)
        with self.assertRaises(TypeError, msg="The 'change()' method does not raise a 'TypeError' when " +
                                              " setting a non-matching value type to the attribute"):
            Settings.change('revealLettersRatio', '1')


if __name__ == '__main__':
    unittest.main()
