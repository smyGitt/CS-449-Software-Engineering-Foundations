"""
    This module contains a class that creates elements 
    with the default stying inherited from the application.
"""

from tkinter import ttk

class StyledElement():
    """
        This class manages the creation of presets, and create
        elements from existing presets. Good for keeping consistent
        styling in the application.
    """
    def __init__(self, default_master, default_font, default_style):
        self.presets = {}
        self.default_parent = default_master
        self.font_list = default_font
        self.default_style = default_style

    def create_preset(self, preset_name,element_master, element_type, **kwargs):
        """
            Adds a new preset to the class element preset list, which can be used
            to create a new tk element with the preset.
        """
        self.presets[preset_name] = {"element_type": element_type, "options":{"master":element_master, **kwargs}}

    def add_font_preset(self, font_preset_name, new_font):
        """
            Adds a new font to the class font list, which can be used
            to create a new tk element with the preset font.
        """
        self.font_list[font_preset_name] = new_font

    def return_font_preset(self, font_name):
        """
            Returns the font from the preset.
        """
        return self.font_list[font_name].copy()

    def return_preset_element(self, preset_name):
        """
            Returns the element that uses preset styling.
        """
        target_type = self.presets[preset_name]["element_type"]
        if target_type == "label":
            return ttk.Label()
        
    def return_preset_element_debug(self, preset_name):
        """
            Returns the preset without converting it into ttk element.
        """
        return self.presets[preset_name]

    def return_font_preset_debug(self):
        """
            Returns the entire font list/dict.
        """
        return self.font_list