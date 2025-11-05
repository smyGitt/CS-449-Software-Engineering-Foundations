"""
    Contains all logic required for the SOS game.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox

class Tile:
    """
        Tile type containing the button's instance, coordinates, and the ownwer
        of the tile (the player that placed a letter there), to be used on a gameboard.
    """
    def __init__(self, button_instance:ttk.Button = None,
                 x_coord:int  = None, y_coord:int = None):
        self.button_instance = button_instance
        self.owner = None
        self.coord = (x_coord,y_coord)

    def set_button_instance(self, new_button):
        """
            Sets the button_instance variable to the new_button.
        """
        self.button_instance = new_button
    
    def debug_print_all_info(self):
        """
            Prints all data contained within this instance of Tile class.
        """
        print("button instance:"+str(self.button_instance!=None)+"\n"
              + "owner:"+ (self.owner.name if self.owner != None else "not owned")
              + "coord x:"+str(self.coord[0])+", coord y:"+str(self.coord[1]))

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

    def add_one_score(self):
        """
            Adds one score to this player.
        """
        self.score += 1
        self.score_variable.set(self.score)
        print("added score to", self.name)

    def reset_score(self):
        """
            Resets score to 0.
        """
        self.score = 0
        self.score_variable.set(0)

class SOSGameLogic:
    """
        Includes functions and logic for the SOS game board.
    """
    def __init__(self):
        self.master = None
        self.gameboard_tile_instance_dict = {}
        self.board_dimension = 8
        self.board_size = self.board_dimension * self.board_dimension
        self.player_dict = {1:Player("Blue One", "#70b8fa"), 2:Player("Red Two", "#e94444")}
        self.conflict_tile_color = "#ca80e2"
        self.occupied_tile_count = 0
        self.gained_point = False
        
        self.game_board_dimension_variable = tk.IntVar(value=self.board_dimension)
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
        if board_dimension < 3 or board_dimension > 15:
            return False
        self.__update_board_size_information(board_dimension)
        return True

    def __update_board_size_information(self, board_dimension):
        self.board_dimension = board_dimension
        self.board_size = board_dimension * board_dimension

    def on_tile_click(self, tile:Tile):
        """
            Instructions to handle a specific tile('s button) being clicked. To summarize:
            0. Check if the button text is empty, that is, it has not been clicked by anyone.
            1. Change button text and color, then disable the button to prevent any more clicks.
            2. Give ownership of the Tile to the Player that has clicked it, along with the
               Tile's letter.
            3. Then switch turn to the next player, by updating the current player to the
               next player.
        """
        if tile.button_instance.cget("text") == "":
            self.__update_button_state(tile)
            self.occupied_tile_count += 1
            bool_gained_point, num_points = self.__move_analysis(tile, False, self.gameboard_tile_instance_dict)
            if bool_gained_point:
                self.__update_point(num_points)
            self.player_dict[self.current_player_number_variable.get()].add_owned_tile(
                self.current_letter_variable.get(), tile
            )
            if self.__bool_check_game_over():
                self.__game_over()
            else:
                self.__switch_player(bool_gained_point)

    def __update_button_state(self, tile:Tile):
        tile.button_instance.config(text=self.current_letter_variable.get(), state=tk.DISABLED)
        
    def __update_button_color(self, tile:Tile):
        curr_color = tile.button_instance.cget("bg")
        player_color = self.__get_current_player().color
        if (curr_color != player_color) and (curr_color != "white"):
            tile.button_instance.config(disabledforeground="white", bg=self.conflict_tile_color)
        else:
            tile.button_instance.config(disabledforeground="white", bg=player_color)

    def __update_SOS_buttons(self, coord_array):
        for coord in coord_array:
            self.__update_button_color(self.gameboard_tile_instance_dict[coord[1]][coord[0]])
            print("painted",str(coord))

    def __switch_player(self, gained_point):
        if not gained_point:
            if self.current_player_number_variable.get() == 1:
                self.current_player_number_variable.set(2)
                self.current_player_name_variable.set(self.player_dict[2].name)
            else:
                self.current_player_number_variable.set(1)
                self.current_player_name_variable.set(self.player_dict[1].name)
        else:
            self.gained_point = False

    def __get_current_player(self):
        return self.player_dict[self.current_player_number_variable.get()]
    
    def __update_point(self, points_gained):
        curr_player = self.__get_current_player()
        for i in range(points_gained):
            curr_player.add_one_score()
        self.gained_point = True

    def __bool_check_game_over(self):
        if self.config_match_type.get() == "casual":
            if self.gained_point:
                return True
        return self.__bool_check_remaining_moves()

    def __game_over(self):
        self.__disable_all_buttons()
        player_dict = self.player_dict
        if player_dict[1].score > player_dict[2].score:
            self.__create_popup("Game Over!", f"{player_dict[1].name} won the game!")
        elif player_dict[2].score > player_dict[1].score:
            self.__create_popup("Game Over!", f"{player_dict[2].name} won the game!")
        else:
            self.__create_popup("Game Over!", "Tied! Nobody wins!")
        self.master.destroy()

    def reset_state(self):
        """
            Resets the current data to the default state.
        """
        self.player_dict[1].reset_score()
        self.player_dict[2].reset_score()
        self.current_player_number_variable.set(1)
        self.gained_point = False
        self.occupied_tile_count = 0

    def __create_popup(self, title, message):
        msgbox.showinfo(parent=self.master, title=title, message=message)

    def __disable_all_buttons(self):
        for y, row in self.gameboard_tile_instance_dict.items():
            for x, tile in row.items():
                tile.button_instance.config(state=tk.DISABLED)

    def __bool_check_remaining_moves(self):
        return self.board_size == self.occupied_tile_count

    def __move_analysis(self, tile:Tile, analysis_only:bool, board:dict):
        """
            Calcultes the point gained from the most recent move, then adds points to the player accordingly.
            \nReturns a tuple: (bool, number of points gained).
        """
        # Get the details of the current tile and game state.
        x,y = tile.coord
        letter = self.current_letter_variable.get()
        board_dimension = self.board_dimension - 1
        points_gained = 0
        # Below are SOS checking in 8 directions for each letter. Notation: - means tiles being checked, x is the current tile.
        if letter == "S":
            #   -   <- above2
            #   -   <- above1
            #   x
            # Check if it is near the edge and therefore impossible 
            if y > 1:
                above1 = board[y-1][x].button_instance.cget("text")
                above2 = board[y-2][x].button_instance.cget("text")
                pattern = "S" + above1 + above2
                if pattern == "SOS":
                    print("-\n-\nx")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x,y-1),(x,y-2),(x,y)])

            # -     <- above2
            #  -    <- above1
            #   x
            if y > 1 and x > 1:
                above1 = board[y-1][x-1].button_instance.cget("text")
                above2 = board[y-2][x-2].button_instance.cget("text")
                pattern = "S" + above1 + above2
                if pattern == "SOS":
                    print("-\n -\n  x")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x-1,y-1),(x-2,y-2),(x,y)])
            
            # v  left2
            #  v  left1
            # --x
            if x > 1:
                left1 = board[y][x-1].button_instance.cget("text")
                left2 = board[y][x-2].button_instance.cget("text")
                pattern = "S" + left1 + left2
                if pattern == "SOS":
                    print("--x")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x-1,y),(x-2,y),(x,y)])
            
            #   x   
            #  -    <- below1
            # -     <- below2
            if y < board_dimension - 1 and x > 1:
                below1 = board[y+1][x-1].button_instance.cget("text")
                below2 = board[y+2][x-2].button_instance.cget("text")
                pattern = "S" + below1 + below2
                if pattern == "SOS":
                    print("  x\n -\n-")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x-1,y+1),(x-2,y+2),(x,y)])
            
            #   x   
            #   -   <- below1
            #   -   <- below2
            if y < board_dimension - 1:
                below1 = board[y+1][x].button_instance.cget("text")
                below2 = board[y+2][x].button_instance.cget("text")
                pattern = "S" + below1 + below2
                if pattern == "SOS":
                    print("x\n-\n-")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x,y+1),(x,y+2),(x,y)])
            
            #   x   
            #    -  <- below1
            #     - <- below2
            if y < board_dimension - 1 and x < board_dimension - 1:
                below1 = board[y+1][x+1].button_instance.cget("text")
                below2 = board[y+2][x+2].button_instance.cget("text")
                pattern = "S" + below1 + below2
                if pattern == "SOS":
                    print("x\n -\n  -")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x+1,y+1),(x+2,y+2),(x,y)])
            
            #     v  right2
            #    v  right1
            #   x--
            if x < board_dimension - 1:
                right1 = board[y][x+1].button_instance.cget("text")
                right2 = board[y][x+2].button_instance.cget("text")
                pattern = "S" + right1 + right2
                if pattern == "SOS":
                    print("x--")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x+1,y),(x+2,y),(x,y)])
            
            #     - <- above2
            #    -  <- above1
            #   x  
            if y > 1 and x < board_dimension - 1:
                above1 = board[y-1][x+1].button_instance.cget("text")
                above2 = board[y-2][x+2].button_instance.cget("text")
                pattern = "S" + above1 + above2
                if pattern == "SOS":
                    print("  -\n -\nx")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x+1,y-1),(x+2,y-2),(x,y)])
        
        if letter == "O":
            #   -   <- above1
            #   x   
            #   -   <- below1
            # Check if it is near the edge and therefore impossible 
            if y > 0 and y < board_dimension - 1:
                above1 = board[y-1][x].button_instance.cget("text")
                below1 = board[y+1][x].button_instance.cget("text")
                pattern = above1 + "O" + below1
                if pattern == "SOS":
                    print("-\nx\n-")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x,y-1),(x,y+1),(x,y)])

            # -     <- above1
            #  x    
            #   -   <- below1
            if (y > 0 and y < board_dimension) and (x > 0 and x < board_dimension):
                above1 = board[y-1][x-1].button_instance.cget("text")
                below1 = board[y+1][x+1].button_instance.cget("text")
                pattern = above1 + "O" + below1
                if pattern == "SOS":
                    print("-\n x\n  -")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x-1,y-1),(x+1,y+1),(x,y)])
            
            # v  left1
            # -x-   
            #   ^  right1
            if x > 0 and x < board_dimension:
                left1  = board[y][x-1].button_instance.cget("text")
                right1 = board[y][x+1].button_instance.cget("text")
                pattern = left1 + "O" + right1
                if pattern == "SOS":
                    print("-x-")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x-1,y),(x+1,y),(x,y)])
            
            #   -   <- above1
            #  x    
            # -     <- below1
            if (y > 0 and y < board_dimension) and (x > 0 and x < board_dimension):
                above1 = board[y-1][x+1].button_instance.cget("text")
                below1 = board[y+1][x-1].button_instance.cget("text")
                pattern = above1 + "O" + below1
                if pattern == "SOS":
                    print("  -\n x\n-")
                    points_gained += 1
                    if not analysis_only: 
                        self.__update_SOS_buttons([(x+1,y-1),(x-1,y+1),(x,y)])

        return (points_gained != 0), points_gained
