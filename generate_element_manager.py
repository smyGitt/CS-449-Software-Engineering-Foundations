"""
    This module contains a class that creates elements 
    with the default stying inherited from the application.
"""

import copy

class ElementGenerationManager():
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

    def edit_default_style(self, style_dict: dict):
        """
            Edits the default style. style_dict accepts dictionaries, and will
            automatically append or update each item to the default style dictionary.
        """
        for key in style_dict.keys():
            # lower() used to prevent any case sensitivity issues.
            # TK styling keys only use lowercases.
            self.default_style[key.lower()] = style_dict[key]

    def create_preset(self, preset_name: str,element_master, element_type: str, **kwargs):
        """
            Adds a new preset to the class element preset list, which can be used
            to create a new tk element with the preset.
        """
        self.presets[preset_name.title()] = {"element_type": element_type.lower(), "options":{"master":element_master, **kwargs}}

    def create_font_preset(self, font_preset_name: str, new_font: tuple):
        """
            Adds a new font to the class font list, which can be used
            to create a new tk element with the preset font.
            font_preset_name is a string, new_font is a tuple.
        """
        self.font_list[font_preset_name] = new_font

    def return_font_preset(self, font_name):
        """
            Returns the font from the preset.
        """
        return copy.deepcopy(self.font_list[font_name])
        
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