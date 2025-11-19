"""
This module contains the main SOS game and GUI logic.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox
from game_logic import SOSGameLogic, GUILogic, Tile

# boilerplate from
# https://stackoverflow.com/questions/17466561/what-is-the-best-way-to-structure-a-tkinter-application

class MainApplication(tk.Frame):
    """
        This class contains the main SOS game and GUI logic.
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Initialize game board dictionary.
        self.game_board_button_dict = {}

        # Initialize the title screen.
        self.game_logic =       SOSGameLogic()
        self.gui =              GUILogic()
        self.game_logic.gui =   self.gui
        self.default_font = self.gui.default_font
        self.default_font_dict = self.gui.fonts

        self.title_screen("SOS", self.__validate_and_start, [
            {"text": "Random size", "variable": self.game_logic.config_do_random_size },
            {"text": "CLICKHOLD",   "variable": self.game_logic.config_do_clickhold   }
        ])

    def title_screen(self, title, start_button_function, game_options):
        """
            Displays the title and the initial settings needed to set up a SOS game.
        """
        pad_size = 5
        pad_mult = 10

        # SOS Title
        title_frame = tk.Frame(self.parent,padx=pad_size*pad_mult,pady=pad_size*pad_mult)
        title_frame.columnconfigure([0,1],weight=1)
        ttk.Label(title_frame,
                  text=title,
                  font=self.default_font_dict["XLarge_Default"],
                  anchor="center",
                  padding=pad_size
                  ).grid(row=0,column=0,columnspan=2,sticky="ew")

        # Dimension / Size Change
        dimension_frame = tk.Frame(title_frame,padx=pad_size,pady=pad_size)
        ttk.Label(dimension_frame,
                  text="Board size (3 to 15): ",
                  font=self.default_font_dict["Small_Default"],
                  anchor="w"
                  ).grid(row=0,column=0,sticky="W")
        ttk.Entry(dimension_frame,
                  textvariable=self.game_logic.game_board_dimension_variable,
                  font=self.default_font_dict["Small_Default"],
                  ).grid(row=0,column=1,sticky="EW")
        dimension_frame.grid(row=3,column=0,columnspan=2,sticky="EW")

        # Checkbutton frame
        self.gui.create_check_buttons(title_frame, pad_size, "Game options", game_options
        ).grid(row=1,column=0,sticky="nsew")

        # Radiobutton frame (Match Type)
        self.gui.create_radio_button(title_frame, pad_size, "Match type", self.game_logic.config_match_type, [
            {"text": "Simple", "value": "Simple"},
            {"text": "General", "value": "General"}
        ]).grid(row=1,column=1,sticky="nsew")

        # Radiobutton frame (Blue Player)
        self.gui.create_radio_button(title_frame, pad_size, "Blue Player", self.game_logic.config_blue_player_type, [
            {"text": "Human", "value": "Human"},
            {"text": "Computer", "value": "Computer"}
        ]).grid(row=2,column=0,sticky="nsew")

        # Radiobutton frame (Red Player)
        self.gui.create_radio_button(title_frame, pad_size, "Red Player", self.game_logic.config_red_player_type, [
            {"text": "Human", "value": "Human"},
            {"text": "Computer", "value": "Computer"}
        ]).grid(row=2,column=1,sticky="nsew")

        # Start button
        tk.Button(title_frame,
                   text="Start!",
                   font=self.default_font_dict["Medium_Default"],
                   command=start_button_function
                   ).grid(row=4,column=0,columnspan=2,sticky="ew")
        title_frame.grid(row=0,column=0,sticky="nsew")

    def __validate_and_start(self):
        if self.game_logic.dimension_validate():
            self.game_logic.create_players()
            self.gui.master = self.game_board(self.game_logic.game_board_dimension_variable.get())
            self.game_logic.reset_state()
        else:
            msgbox.showerror("Invalid Dimension", "Please enter a valid board dimension.")

    def game_board(self, board_dimension:int):
        """
            Creates a game board with a given board size.
        """
        board_side_length = 500

        new_window = tk.Toplevel(self.parent)
        new_window.title(f"SOS {board_dimension}x{board_dimension} || {self.game_logic.config_match_type.get()}")
        new_window.rowconfigure([0,1],weight=1)
        new_window.columnconfigure([0],weight=0)
        new_window.columnconfigure([1],weight=1)
        new_window.geometry(f"{board_side_length+300}x{(int) (board_side_length)}")
        new_window.resizable(False,False)

        self.__playing_field(new_window, board_dimension, board_side_length).grid(row=0,column=1,sticky="nsew",rowspan=2)
        self.__player_tab(new_window,1).grid(row=0,column=0,sticky="NSEW")
        self.__player_tab(new_window,2).grid(row=1,column=0,sticky="NSEW")
        self.__board_control_tab(new_window).grid(row=0,rowspan=2,column=3,sticky="NSEW")

        return new_window

    def __playing_field(self, master:tk.Frame, board_dimension, board_side_length):
        button_side_length = board_side_length // board_dimension
        
        game_board_frame = tk.Frame(master, bg="white")
        game_board_frame.grid_propagate(False)
        for row_index in range(board_dimension):
            self.game_logic.gameboard_tile_instance_dict[row_index] = {}
            for column_index in range(board_dimension):
                self.game_logic.gameboard_tile_instance_dict[row_index][column_index] = Tile(x_coord = column_index, y_coord = row_index)
                new_button = tk.Button(
                        game_board_frame,
                        font=(self.default_font,int(300 / board_dimension)),
                        width=button_side_length,
                        compound="center",
                        bg="white",
                        command=(lambda tile = self.game_logic.gameboard_tile_instance_dict[row_index][column_index]:
                                 self.game_logic.on_tile_click(tile))
                )
                self.game_logic.gameboard_tile_instance_dict[row_index][column_index].set_button_instance(new_button)
                
                self.game_logic.gameboard_tile_instance_dict[row_index][column_index].button_instance.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew"
                    )
                game_board_frame.columnconfigure(column_index,weight=1)
            game_board_frame.rowconfigure(row_index,weight=1)
        return game_board_frame

    def __player_tab(self, master:tk.Frame, player_number:int):
        frame = tk.Frame(master=master, relief="raised", border=2, padx=15, pady=10, width=150)
        frame.grid_propagate(False)
        frame.rowconfigure([2],weight=1)
        frame.columnconfigure([0],weight=1)
        ttk.Label(master=frame,
                  text="NAME",
                  font=self.default_font_dict["Small_Default"],
                  ).grid(row=0,column=0,sticky="NSEW")
        ttk.Label(master=frame,
                  text=self.game_logic.player_dict[player_number].name,
                  font=self.default_font_dict["Medium_Default"],
                  foreground=self.game_logic.player_dict[player_number].color
                  ).grid(row=1,column=0,sticky="NEW")
        ttk.Label(master=frame,
                  textvariable=self.game_logic.player_dict[player_number].score_variable,
                  font=self.default_font_dict["Large_Default"], justify="right", anchor="center",
                  foreground=self.game_logic.player_dict[player_number].color
                  ).grid(row=2,column=0,sticky="NSEW")
        ttk.Label(master=frame,
                  text=self.game_logic.config_blue_player_type.get().upper() if player_number == 1 else self.game_logic.config_red_player_type.get().upper(),
                  font=self.default_font_dict["Small_Default"]
                  ).grid(row=3,column=0,sticky="SEW")
        return frame
    
    def __board_control_tab(self, master:tk.Frame):
        frame = tk.Frame(master=master, relief="raised", border=2, padx=15, pady=10, width=150)
        frame.grid_propagate(False)
        frame.rowconfigure([1],weight=1)
        frame.columnconfigure([0],weight=1)
        ttk.Label(master=frame,
                  text="TURN",
                  font=self.default_font_dict["Small_Default"],
                  ).grid(row=0,column=0,sticky="NEW")
        ttk.Label(master=frame,
                  textvariable=self.game_logic.current_player_name_variable,
                  font=self.default_font_dict["Medium_Default"]
                  ).grid(row=1,column=0,sticky="NEW")
        ttk.Label(master=frame,
                  text="LETTER",
                  font=self.default_font_dict["Small_Default"]
                  ).grid(row=2,column=0,sticky="NEW")
        tk.Radiobutton(master=frame,
                        text="S",
                        value="S",
                        variable=self.game_logic.current_letter_variable,
                        font=self.default_font_dict["Large_Default"],
                        borderwidth=3,
                        indicatoron=False,
                        pady=32
                        ).grid(row=3,column=0,sticky="new")
        tk.Radiobutton(master=frame,
                        text="O",
                        value="O",
                        variable=self.game_logic.current_letter_variable,
                        font=self.default_font_dict["Large_Default"],
                        borderwidth=3,
                        indicatoron=False,
                        pady=32
                        ).grid(row=4,column=0,sticky="new")
        return frame
        

def initialize_application():
    """
        initializes the application, but without starting mainloop.
    """
    root = tk.Tk()
    app = MainApplication(root)
    return app

if __name__ == "__main__":
    initialize_application().mainloop()