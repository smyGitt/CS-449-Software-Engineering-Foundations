"""
    Contains all logic required for the SOS game.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox
import random
from abc import abstractmethod

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
    def __init__(self, player_name:str, color:str, gui):
        self.name = player_name
        self.color = color
        self.owned_tile = {"S":[], "O":[]}
        self.score = 0
        self.score_variable = tk.IntVar()
        self.gui = gui

    def set_name(self, new_name:str) -> None:
        """
            Update this player's name with a new one.
        """
        self.name = new_name
    
    def add_owned_tile(self,letter:str, tile:Tile) -> None:
        """
            Add the newly acquired Tiles to this player.
        """
        self.owned_tile[letter].append(tile)

    def add_one_score(self) -> None:
        """
            Adds one score to this player.
        """
        self.score += 1
        self.score_variable.set(self.score)
        print("added score to", self.name)

    def reset_score(self) -> None:
        """
            Resets score to 0.
        """
        self.score = 0
        self.score_variable.set(0)

    def make_move(self, tile:Tile, letter:str) -> None:
        self.gui.config_button(tile, letter, "disabled")

    def take_turn(self, game_logic) -> None:
        pass

class ComputerPlayer(Player):
    def __init__(self, player_name:str, color:str, gui):
        super().__init__(player_name, color, gui)

    def take_turn(self, game_logic) -> None:
        game_logic.gui.master.after(100, lambda: self._computer_move_logic(game_logic))

    def _computer_move_logic(self, game_logic) -> None:
        available_moves = game_logic._return_possible_score_per_tile()

        # Determine which letters will result in more points.
        highest_point_s = 0
        for points_possible, tiles in available_moves["S"].items():
            highest_point_s = points_possible if len(tiles) > 0 else highest_point_s

        highest_point_o = 0
        for points_possible, tiles in available_moves["O"].items():
            highest_point_o = points_possible if len(tiles) > 0 else highest_point_o

        # Choose the letter based on the findings above.
        letter_chosen = "S" # Default letter
        if highest_point_s == highest_point_o:
            letter_chosen = random.choice(["S", "O"])
        else:
            letter_chosen = "S" if highest_point_s > highest_point_o else "O"

        # Pick a random tile from the highest scoring tiles list to place the chosen letter in.
        tile_chosen = random.choice(available_moves[letter_chosen][highest_point_s if letter_chosen == "S" else highest_point_o])
        
        super().make_move(tile_chosen, letter_chosen)
        game_logic.process_turn_and_switch(tile_chosen, letter_chosen)

class SOSGameLogic:
    """
        Includes functions and logic for the SOS game board.
    """
    def __init__(self):
        self.gui = None
        self.master = None
        self.gameboard_tile_instance_dict = {}
        self.board_dimension = 8
        self.board_size = self.board_dimension * self.board_dimension
        self.player_dict = {} 
        self.occupied_tile_count = 0
        self.gained_point = False
        
        self.game_board_dimension_variable = tk.IntVar(value=self.board_dimension)
        self.current_player_number_variable = tk.IntVar(value=1)
        self.current_player_name_variable = tk.StringVar()
        self.current_letter_variable = tk.StringVar(value="S")
        
        self.config_match_type = tk.StringVar(value="Simple")
        self.config_do_random_size = tk.BooleanVar()
        self.config_do_clickhold = tk.BooleanVar()
        self.config_blue_player_type = tk.StringVar(value="Human")
        self.config_red_player_type = tk.StringVar(value="Human")

    def dimension_validate(self) -> bool:
        """
            Validate the dimensions the user has chosen to be within expected ranges.
            Expected range: 3 to 15, integer.
        """
        board_dimension = self.game_board_dimension_variable.get()
        if board_dimension < 3 or board_dimension > 15:
            return False
        self.__update_board_size_information(board_dimension)
        return True

    def create_players(self) -> None:
        """
            Initialize computer / human players PER COLOR based on user's choice.
        """
        if self.config_blue_player_type.get() == "Computer":
            self.player_dict[1] = ComputerPlayer("Blue Clanker", "blue", self.gui)
        else:
            self.player_dict[1] = Player("Blue One", "blue", self.gui)

        if self.config_red_player_type.get() == "Computer":
            self.player_dict[2] = ComputerPlayer("Red Clanker", "red", self.gui)
        else:
            self.player_dict[2] = Player("Red Two", "red", self.gui)
            
        self.current_player_name_variable.set(self.player_dict[1].name)

    def __update_board_size_information(self, board_dimension) -> None:
        self.board_dimension = board_dimension
        self.board_size = board_dimension * board_dimension

    def on_tile_click(self, tile:Tile) -> None:
        """
            Instructions to handle a specific tile('s button) being clicked. To summarize:
            0. Check if the button text is empty, that is, it has not been clicked by anyone.
            1. Change button text and color, then disable the button to prevent any more clicks.
            2. Give ownership of the Tile to the Player that has clicked it, along with the
               Tile's letter.
            3. Then switch turn to the next player, by updating the current player to the
               next player.
        """
        if tile.button_instance.cget("text") != "": return # just in case
        current_letter = self.current_letter_variable.get()
        self.__get_current_player().make_move(tile, current_letter)
        self.process_turn_and_switch(tile, current_letter)

    def process_turn_and_switch(self, tile:Tile, letter:str) -> None:
        self.occupied_tile_count += 1
        
        # Point gain check.
        bool_gained_point, num_points = self.move_analysis(tile, False, self.gameboard_tile_instance_dict, letter)
        self.player_dict[self.current_player_number_variable.get()].add_owned_tile(letter, tile)
        if bool_gained_point:               self.__update_point(num_points)
        
        # Game over check.
        if self.__bool_check_game_over():   self.__game_over()
        else:
            if not bool_gained_point:
                current = self.current_player_number_variable.get()
                self.current_player_number_variable.set(2 if current == 1 else 1)
                self.current_player_name_variable.set(self.player_dict[self.current_player_number_variable.get()].name)
            else:
                self.gained_point = False
            
            self.__get_current_player().take_turn(self)

    def __update_SOS_buttons(self, coord_array) -> None:
        for coord in coord_array:
            self.gui.config_button(self.gameboard_tile_instance_dict[coord[1]][coord[0]],
                                   new_state="disabled",
                                   new_color=self.__get_current_player().color
                                   )
            print("painted",str(coord), end=" ")
        print()
    
    def __get_current_player(self) -> Player:
        return self.player_dict[self.current_player_number_variable.get()]
    
    def __update_point(self, points_gained) -> None:
        curr_player = self.__get_current_player()
        for i in range(points_gained):
            curr_player.add_one_score()
        self.gained_point = True

    def __bool_check_game_over(self) -> bool:
        if self.config_match_type.get() == "Simple":
            if self.gained_point:
                return True
        return self.board_size == self.occupied_tile_count

    def __game_over(self) -> None:
        self.__disable_all_buttons()
        player_dict = self.player_dict
        if player_dict[1].score > player_dict[2].score:
            self.gui.create_popup("Game Over!", f"{player_dict[1].name} won the game!")
        elif player_dict[2].score > player_dict[1].score:
            self.gui.create_popup("Game Over!", f"{player_dict[2].name} won the game!")
        else:
            self.gui.create_popup("Game Over!", "Tied! Nobody wins!")
        self.gui.master.destroy()

    def reset_state(self) -> None:
        """
            Resets the current data to the default state.
        """
        self.player_dict[1].reset_score()
        self.player_dict[2].reset_score()
        self.current_player_number_variable.set(1)
        self.current_player_name_variable.set(self.player_dict[1].name)
        self.gained_point = False
        self.occupied_tile_count = 0

        self.__get_current_player().take_turn(self)

    def __disable_all_buttons(self) -> None:
        for y, row in self.gameboard_tile_instance_dict.items():
            for x, tile in row.items():
                self.gui.config_button(tile, new_state="disabled")

    def _return_possible_score_per_tile(self) -> dict[str,dict[int,list]]:
        """
            Returns the scores possible for the currently available tiles, excluding the
            non-empty tiles.
            \nReturn format is { letter: { points possible: [ tile ] } }.
        """
        output = {"S":{0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]},
                  "O":{0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}}
        for y, row in self.gameboard_tile_instance_dict.items():
            for x, tile in row.items():
                if tile.button_instance.cget("text") == "":
                    for letter in ["S","O"]:
                        result = self.move_analysis(tile, True, self.gameboard_tile_instance_dict, letter)
                        output[letter][result[1]].append(tile)
        return output

    def move_analysis(self, tile:Tile, analysis_only:bool, board:dict, curr_letter:str = "") -> tuple[bool, int]:
        """
            Calcultes the point gained from the most recent move, then adds points to the player accordingly.
            \nReturns a tuple: (bool, number of points gained).
        """
        # Get the details of the current tile and game state.
        x,y = tile.coord
        letter = self.current_letter_variable.get() if curr_letter == "" else curr_letter
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

class GUILogic:
    def __init__(self):
            self.master = None
            self.color_dict = {"blue": "#70b8fa", "red": "#e94444", "purple": "#ca80e2"}
            
            self.default_font =     "Times New Roman"
            self.fonts = {
                "XLarge_Default":   (self.default_font, 30),
                "Large_Default":    (self.default_font, 20),
                "Medium_Default":   (self.default_font, 15),
                "Small_Default":    (self.default_font, 10),
                "XSmall_Default":   (self.default_font, 5)
            }
        
    def create_popup(self, title, message) -> None:
        msgbox.showinfo(parent=self.master, title=title, message=message)

    def config_button(self, tile:Tile, letter:str = None, new_state = None, new_color= None) -> None:
        """
            letter: "S" or "O".
            new_state: "disabled" or "active"
        """
        if letter != None: tile.button_instance.config(text=letter)

        if new_state != None:
            if new_state == "disabled":
                tile.button_instance.config(state=tk.DISABLED)
            elif new_state == "active":
                tile.button_instance.config(state=tk.ACTIVE)
        
        if new_color != None:
            curr_color = tile.button_instance.cget("bg")
            if (curr_color != self.color_dict[new_color]) and (curr_color != "white"):
                tile.button_instance.config(disabledforeground="white", bg=self.color_dict["purple"])
            else:
                tile.button_instance.config(disabledforeground="white", bg=self.color_dict[new_color])
        
    def create_check_buttons(self, master:tk.Frame, pad:int, label_text:str, check_buttons_content:list[dict]) -> tk.Frame:
        """
            Creates check buttons. Check buttons content should be [ { text: str, variable: xVar() } ]
        """
        # Checkbutton frame
        checkbox_frame = tk.Frame(master,padx=pad,pady=pad)
        ttk.Label(checkbox_frame,
                  text=label_text,
                  font=self.fonts["Medium_Default"],
                  anchor="w",
                  ).grid(row=0,column=0,sticky="ew")
        for index, check_button in enumerate(check_buttons_content, start = 1):
            tk.Checkbutton(checkbox_frame,
                            text=check_button["text"],
                            font=self.fonts["Small_Default"],
                            anchor="w",
                            variable=check_button["variable"]
                            ).grid(row=index,column=0,sticky="ew")
        return checkbox_frame

    def create_radio_button(self, master:tk.Frame, pad:int, label_text:str, variable, radio_buttons:list[dict[str, str]]) -> tk.Frame:
        """
            Creates radio buttons. Radio buttons should contain the text shown and set value, and variable the target value.
            \nEach radio button dict contains {"text": "", "value": ""}.
        """
        radiotitle_frame = tk.Frame(master,padx=pad,pady=pad)
        ttk.Label(radiotitle_frame,
                  text=label_text,
                  font=self.fonts["Medium_Default"],
                  anchor="w"
                  ).grid(row=0,column=0,sticky="ew")
        for index, radio_button in enumerate(radio_buttons, start = 1):
            tk.Radiobutton(radiotitle_frame,
                            text=radio_button["text"],
                            value=radio_button["value"],
                            variable=variable,
                            font=self.fonts["Small_Default"],
                            anchor="w",
                            ).grid(row=index,column=0,sticky="ew")
        return radiotitle_frame