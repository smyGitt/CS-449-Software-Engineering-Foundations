"""
This module tests the application using unittest.
"""

import unittest
from generate_element_manager import ElementGenerationManager

class TestFunctions(unittest.TestCase):
    """
        Class for testing new functions.
    """
    def test_merge_dict(self):
        """
            Testing dictionary merge with overlapping keys.
        """
        # Test environment setup
        default_fonts = {
            "LFont":("CC Wild Words", 40),
            "MFont":("CC Wild Words", 20),
            "SFont":("CC Wild Words", 10)
        }
        default_style = {
            "padding":5,
            "font":("CC Wild Words", 20),
            "background":"#FFFFFF",
            "foreground":"#000000",
            "highlightbackground":"#BBBBBB"
        }
        se = ElementGenerationManager("some_master",default_fonts,default_style)
        se.create_preset("new preset","other_master","button")

        # Actual test
        self.assertEqual(se.return_preset_element_debug("new preset")["element_type"],
                         "button",
                         "Element type 'button' should be merged.")
        self.assertEqual(se.return_preset_element_debug("new preset")["options"]["master"],
                         "other_master",
                         "some_master should be replaced by other_master")

    def test_append_to_dict(self):
        """
            Testing adding new items to the dictionary.
        """
        # Test environment setup
        default_fonts = {
            "LFont":("CC Wild Words", 40),
            "MFont":("CC Wild Words", 20),
            "SFont":("CC Wild Words", 10)
        }
        default_style = {
            "padding":5,
            "font":("CC Wild Words", 20),
            "background":"#FFFFFF",
            "foreground":"#000000",
            "highlightbackground":"#BBBBBB"
        }
        se = ElementGenerationManager("some_master",default_fonts,default_style)
        se.create_font_preset("SomeFont",("Times New Roman", 400))

        expected_result = {
            "LFont":("CC Wild Words", 40),
            "MFont":("CC Wild Words", 20),
            "SFont":("CC Wild Words", 10),
            "SomeFont":("Times New Roman", 400)
        }

        # Actual test
        self.assertEqual(se.return_font_preset_debug(), expected_result,
                         "SomeFont should be the last item in the font list/dict")
        
if __name__ == '__main__':
    unittest.main()
