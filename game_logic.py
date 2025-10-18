"""
    Contains all logic required for the SOS game.
"""

import tkinter as tk
from tkinter import ttk

class Tile:
    """
        Tile type containing the button's instance, coordinates, and the ownwer
        of the tile (the player that placed a letter there), to be used on a gameboard.
    """
    def __init__(self, button_instance:ttk.Button = None,
                 x_coord:int  = None, y_coord:int = None):
        self.button_instance = button_instance
        self.owner = None
        self.coordinate = (x_coord,y_coord)

    def set_button_instance(self, new_button):
        """
            Sets the button_instance variable to the new_button.
        """
        self.button_instance = new_button

class Player:
    """
        Contains player-specific information and functions.
    """
    def __init__(self, player_name:str, color:str):
        self.name = player_name
        self.color = color
        self.owned_tile = {"S":[], "O":[]}
        self.score = 0
        self.score_variable = tk.IntVar()

    def set_name(self, new_name:str):
        """
            Update this player's name with a new one.
        """
        self.name = new_name
    
    def add_owned_tile(self,letter:str, tile:Tile):
        """
            Add the newly acquired Tiles to this player.
        """
        self.owned_tile[letter].append(tile)

class SOSGameLogic:
    """
        Includes functions and logic for the SOS game board.
    """
    def __init__(self):
        self.gameboard_tile_instance_dict = {}
        self.player_dict = {1:Player("Blue One", "blue"), 2:Player("Red Two", "red")}
        
        self.game_board_dimension_variable = tk.IntVar(value=8)
        self.current_player_number_variable = tk.IntVar(value=1)
        self.current_player_name_variable = tk.StringVar(value=self.player_dict[self.current_player_number_variable.get()].name)
        self.current_letter_variable = tk.StringVar(value="S")
        
        self.config_match_type = tk.StringVar(value="casual")
        self.config_do_random_size = tk.BooleanVar()
        self.config_do_clickhold = tk.BooleanVar()
        self.config_do_ai_opponent = tk.BooleanVar()

    def dimension_validate(self):
        """
            Validate the dimensions the user has chosen to be within expected ranges.
            Expected range: 3 to 30, integer.
        """
        board_dimension = self.game_board_dimension_variable.get()
        if board_dimension < 3 or board_dimension > 30:
            return False
        return True

    def on_tile_click(self, tile:Tile):
        """
            Instructions to handle a specific tile('s button) being clicked. To summarize:
            1. Change button text and color, then disable the button to prevent any more clicks.
            2. Give ownership of the Tile to the Player that has clicked it, along with the Tile's letter.
            3. Then switch turn to the next player, by updating the current player to the next player.
        """
        self.__update_button(tile)
        self.player_dict[self.current_player_number_variable.get()].add_owned_tile(self.current_letter_variable.get(), tile)
        self.__switch_player()

    def __update_button(self, tile:Tile):
        tile.button_instance.config(text=self.current_letter_variable.get(),
                                    state=tk.DISABLED,
                                    disabledforeground=self.__get_current_player().color
                                    )

    def __switch_player(self):
        if self.current_player_number_variable.get() == 1:
            self.current_player_number_variable.set(2)
            self.current_player_name_variable.set(self.player_dict[2].name)
        else:
            self.current_player_number_variable.set(1)
            self.current_player_name_variable.set(self.player_dict[1].name)

    def __get_current_player(self):
        return self.player_dict[self.current_player_number_variable.get()]
