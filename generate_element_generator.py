"""
    Generates elements with the provided style and other sub-options.
"""

from tkinter import ttk
from generate_element_manager import ElementGenerationManager

class ElementGenerationGenerator(ElementGenerationManager):
    """
        From the given information and style options, generates a new tkinter element.
    """
    def return_label(self, label_text: str, preset_option_dict: dict):
        """
            Return a label with the preset provided. 
        """
        return ttk.Label(text=label_text, style=preset_option_dict)

    def return_button(self, button_text: str, preset_option_dict: dict):
        """
            Return a button with the preset provided.
        """
        return ttk.Button(text=button_text, style=preset_option_dict)
