from tkinter import ttk

class Tile:
    """
        Tile type containing the button's instance, coordinates, and the ownwer
        of the tile (the player that placed a letter there), to be used on a gameboard.
    """
    def __init__(self,
                button_instance:ttk.Button = None, owner:str = None):
        self.button_instance = button_instance
        self.owner = owner

    def on_click(self):
        """
            Function that runs when the tile (button) is pressed.
        """
        print("clicked")

    def set_button_instance(self, new_button):
        """
            Sets the button_instance variable to the new_button.
        """
        self.button_instance = new_button

class SOSGameLogic:
    """
        Includes functions and logic for the SOS game board.
    """
    def process_turn(self, playerName:str, letterChoice:str, tile:Tile = None):
        pass