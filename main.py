"""
This module contains the main SOS game and GUI logic.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox
from game_logic import SOSGameLogic, Tile

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
        self.default_font =     "Times New Roman"
        self.default_font_dict = {
            "XLarge_Default":   (self.default_font, 80),
            "Large_Default":    (self.default_font, 40),
            "Medium_Default":   (self.default_font, 20),
            "Small_Default":    (self.default_font, 15),
            "XSmall_Default":   (self.default_font, 10)
            }
        self.title_screen()

    def title_screen(self):
        """
        Displays the title and the initial settings needed to set up a SOS game.
        """
        pad_size = 5
        pad_mult = 10

        # SOS Title
        title_frame = tk.Frame(self.parent,padx=pad_size*pad_mult,pady=pad_size*pad_mult)
        title_frame.columnconfigure([0,1],weight=1)
        ttk.Label(title_frame,
                  text="S  O  S",
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
        dimension_frame.grid(row=2,column=0,columnspan=2,sticky="EW")

        # Checkbutton frame
        checkbox_frame = tk.Frame(title_frame,padx=pad_size,pady=pad_size)
        ttk.Label(checkbox_frame,
                  text="Game options",
                  font=self.default_font_dict["Medium_Default"],
                  anchor="w",
                  ).grid(row=0,column=0,sticky="ew")
        tk.Checkbutton(checkbox_frame,
                        text="Random size",
                        font=self.default_font_dict["Small_Default"],
                        anchor="w",
                        variable=self.game_logic.config_do_random_size
                        ).grid(row=1,column=0,sticky="ew")
        tk.Checkbutton(checkbox_frame,
                        text="CLICKHOLD",
                        font=self.default_font_dict["Small_Default"],
                        anchor="w",
                        variable=self.game_logic.config_do_clickhold
                        ).grid(row=2,column=0,sticky="ew")
        tk.Checkbutton(checkbox_frame,
                        text="vs. AI",
                        font=self.default_font_dict["Small_Default"],
                        anchor="w",
                        variable=self.game_logic.config_do_ai_opponent
                        ).grid(row=3,column=0,sticky="ew")
        checkbox_frame.grid(row=1,column=0,sticky="nsew")

        # Radiobutton frame
        radiotitle_frame = tk.Frame(title_frame,padx=pad_size,pady=pad_size)
        ttk.Label(radiotitle_frame,
                  text="Match type",
                  font=self.default_font_dict["Medium_Default"],
                  anchor="w"
                  ).grid(row=0,column=0,sticky="ew")
        tk.Radiobutton(radiotitle_frame,
                        text="Casual",
                        value="casual",
                        variable=self.game_logic.config_match_type,
                        font=self.default_font_dict["Small_Default"],
                        anchor="w",
                        ).grid(row=1,column=0,sticky="ew")
        tk.Radiobutton(radiotitle_frame,
                        text="Ranked",
                        value="ranked",
                        variable=self.game_logic.config_match_type,
                        font=self.default_font_dict["Small_Default"],
                        anchor="w",
                        ).grid(row=2,column=0,sticky="ew")
        radiotitle_frame.grid(row=1,column=1,sticky="nsew")

        # Start button
        tk.Button(title_frame,
                   text="Start!",
                   font=self.default_font_dict["Medium_Default"],
                   command=self.__validate_and_start
                   ).grid(row=3,column=0,columnspan=2,sticky="ew")
        title_frame.grid(row=0,column=0,sticky="nsew")

    def __validate_and_start(self):
        if self.game_logic.dimension_validate():
            self.__game_board(self.game_logic.game_board_dimension_variable.get())
        else:
            msgbox.showerror("Invalid Dimension", "Please enter a valid board dimension.")

    def __game_board(self, board_dimension:int):
        """
            Creates a game board, very barebones.
        """
        board_side_length = 750
        button_side_length = 750 // board_dimension

        new_window = tk.Toplevel(self.parent)
        new_window.title(f"SOS {board_dimension}x{board_dimension} || Human vs "
                         + ("AI" if self.game_logic.config_do_ai_opponent.get() else "Human")
                         + f" || {self.game_logic.config_match_type.get()}")
        new_window.rowconfigure([0,1],weight=1)
        new_window.columnconfigure([0],weight=0)
        new_window.columnconfigure([1],weight=1)
        new_window.geometry(f"{board_side_length+400}x{(int) (board_side_length)}")
        new_window.resizable(False,False)

        game_board_frame = tk.Frame(new_window, bg="white")
        game_board_frame.grid_propagate(False)
        for row_index in range(board_dimension):
            self.game_logic.gameboard_tile_instance_dict[row_index] = {}
            for column_index in range(board_dimension):
                self.game_logic.gameboard_tile_instance_dict[row_index][column_index] = Tile(x_coord = column_index, y_coord = row_index)
                new_button = tk.Button(
                        game_board_frame,
                        font=(self.default_font,int(500 / board_dimension)),
                        width=button_side_length,
                        compound="center",
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
        game_board_frame.grid(row=0,column=1,sticky="nsew",rowspan=2)

        self.__player_tab(new_window,1).grid(row=0,column=0,sticky="NSEW")
        self.__player_tab(new_window,2).grid(row=1,column=0,sticky="NSEW")
        self.__board_control_tab(new_window).grid(row=0,rowspan=2,column=3,sticky="NSEW")

    def __player_tab(self, master:tk.Frame, player_number:int):
        frame = tk.Frame(master=master, relief="raised", border=2, padx=15, pady=10, width=200)
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
                  text="AI" if self.game_logic.config_do_ai_opponent.get() and player_number == 2 else "HUMAN",
                  font=self.default_font_dict["Small_Default"]
                  ).grid(row=3,column=0,sticky="SEW")
        return frame
    
    def __board_control_tab(self, master:tk.Frame):
        frame = tk.Frame(master=master, relief="raised", border=2, padx=15, pady=10, width=200)
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
                        pady=44
                        ).grid(row=3,column=0,sticky="new")
        tk.Radiobutton(master=frame,
                        text="O",
                        value="O",
                        variable=self.game_logic.current_letter_variable,
                        font=self.default_font_dict["Large_Default"],
                        borderwidth=3,
                        indicatoron=False,
                        pady=44
                        ).grid(row=4,column=0,sticky="new")
        return frame

def initialize_application():
    """initializes the application, but without starting mainloop."""
    root = tk.Tk()
    app = MainApplication(root)
    return app

if __name__ == "__main__":
    initialize_application().mainloop()
