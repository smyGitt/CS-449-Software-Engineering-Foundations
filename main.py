"""
This module contains the main SOS game and GUI logic.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox
from generate_element_manager import ElementGenerationManager
from game_logic import SOSGameLogic as gLogic
from game_logic import Tile

# boilerplate from
# https://stackoverflow.com/questions/17466561/what-is-the-best-way-to-structure-a-tkinter-application

class MainApplication(tk.Frame):
    """
    This class contains the main SOS game and GUI logic.
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Set default font and style presets and create ElementGenerationManager.
        self.e_preset = ElementGenerationManager(
            self.parent,
            {
            "DefaultLFont":("CC Wild Words", 40),
            "DefaultMFont":("CC Wild Words", 20),
            "DefaultSFont":("CC Wild Words", 10)
            },
            {
            "padding":5,
            "background":"#FFFFFF",
            "foreground":"#000000",
            "highlightbackground":"#888888"
            }
        )
        
        # Update the default style preset above, append the default font.
        self.e_preset.edit_default_style({"font":self.e_preset.return_font_preset("DefaultMFont")})

        # Initialize game board dictionary.
        self.game_board_button_dict = {}

        # Initialize the title screen.
        self.title_screen()

    def switch_frame(self, prev_page, next_page):
        pass

    def title_screen(self):
        """
        Displays the title and the initial settings needed to set up a SOS game.
        """
        pad_size = 5
        pad_mult = 10
        text_font= ("CC Wild Words", 40)

        title_frame = tk.Frame(self.parent,padx=pad_size*pad_mult,pady=pad_size*pad_mult)
        ttk.Label(title_frame,
                  text="S O S",
                  font=text_font,
                  padding=pad_size).grid(row=0,column=0,columnspan=2,sticky="ew")

        # Checkbutton frame
        checkbox_frame = tk.Frame(title_frame,padx=pad_size,pady=pad_size)
        ttk.Label(checkbox_frame,text="Game options",anchor="w").grid(row=0,column=0,sticky="ew")
        self.config_do_random_size = tk.BooleanVar()
        ttk.Checkbutton(checkbox_frame,
                        text="Random board size",
                        variable=self.config_do_random_size).grid(row=1,column=0,sticky="ew")
        self.config_do_clickhold = tk.BooleanVar()
        ttk.Checkbutton(checkbox_frame,
                        text="CLICKHOLD",
                        variable=self.config_do_clickhold).grid(row=2,column=0,sticky="ew")
        self.config_do_ai_opponent = tk.BooleanVar()
        ttk.Checkbutton(checkbox_frame,
                        text="vs. AI Opponent",
                        variable=self.config_do_ai_opponent).grid(row=3,column=0,sticky="ew")
        checkbox_frame.grid(row=1,column=0,sticky="nsew")

        # Radiobutton frame
        radiotitle_frame = tk.Frame(title_frame,padx=pad_size,pady=pad_size)
        ttk.Label(radiotitle_frame, text="Match type").grid(row=0,column=1,sticky="ew")
        self.config_match_type = tk.StringVar(value="casual")
        ttk.Radiobutton(radiotitle_frame,
                        text="Casual",
                        value="casual",
                        variable=self.config_match_type).grid(row=1,column=1,sticky="ew")
        ttk.Radiobutton(radiotitle_frame,
                        text="Ranked",
                        value="ranked",
                        variable=self.config_match_type).grid(row=2,column=1,sticky="ew")
        radiotitle_frame.grid(row=1,column=1,sticky="nsew")

        # Start button, the messagebox is temporary for testing inputs above.
        ttk.Button(title_frame,text="Start!",command=(lambda: self.game_board(10))).grid(row=2,column=0,columnspan=2,sticky="ew")
        ttk.Button(title_frame,text="Debug!",command=(
             lambda:msgbox.showinfo(
                message=f"Seleted options are: \n\
                    {self.config_do_random_size.get()} and {self.config_match_type.get()}"
            ))).grid(row=3,column=0,columnspan=2,sticky="ew")
        title_frame.grid(row=0,column=0,sticky="nsew")

    def game_board(self, board_dimension:int):
        """
            Creates a game board, very barebones.
        """
        board_side_length = 32*board_dimension
        button_side_length = board_side_length//board_side_length # = 1? why is it even here

        new_window = tk.Toplevel(self.parent)
        new_window.geometry(f"{board_side_length}x{board_side_length}")
        if (self.config_do_ai_opponent):
            new_window.title("SOS Gameboard, vs AI")
        else:
            new_window.title("SOS Gameboard, vs Human")
        new_window.resizable(False,False)
        new_window.rowconfigure(0,weight=1)
        new_window.columnconfigure(0,weight=1)
        game_board_frame = tk.Frame(new_window,width=board_side_length,height=board_side_length)

        for row_index in range(board_dimension):
            self.game_board_button_dict[row_index] = {}
            for column_index in range(board_dimension):
                new_tile = Tile()
                new_button = ttk.Button(
                        game_board_frame,
                        text="",
                        compound="center",
                        command=(new_tile.on_click)
                )
                new_tile.set_button_instance(new_button)
                self.game_board_button_dict[row_index][column_index] = new_tile
                
                self.game_board_button_dict[row_index][column_index].button_instance.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew"
                    )
                game_board_frame.columnconfigure(column_index,weight=1)
            game_board_frame.rowconfigure(row_index,weight=1)
        game_board_frame.grid(row=0,column=0,sticky="nsew")

def initialize_application():
    """initializes the application, but without starting mainloop."""
    root = tk.Tk()
    app = MainApplication(root)
    return app

if __name__ == "__main__":
    initialize_application().mainloop()
