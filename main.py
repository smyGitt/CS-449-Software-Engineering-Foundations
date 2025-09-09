"""
This module contains the main SOS game and GUI logic.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox
from generate_element import StyledElement

# boilerplate from
# https://stackoverflow.com/questions/17466561/what-is-the-best-way-to-structure-a-tkinter-application

class MainApplication(tk.Frame):
    """
    This class contains the main SOS game and GUI logic.
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.default_fonts = {
            "LFont":("CC Wild Words", 40),
            "MFont":("CC Wild Words", 20),
            "SFont":("CC Wild Words", 10)
        }
        self.default_style = {
            "padding":5,
            "font":("CC Wild Words", 20),
            "background":"#FFFFFF",
            "foreground":"#000000",
            "highlightbackground":"#BBBBBB"
        }
        self.se = StyledElement(self.parent, self.default_fonts, self.default_style)
        self.game_board_button_dict = {}
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
        ttk.Button(title_frame,text="Start!",command=(self.game_board)).grid(row=2,column=0,columnspan=2,sticky="ew")
        ttk.Button(title_frame,text="Debug!",command=(
             lambda:msgbox.showinfo(
                message=f"Seleted options are: \n\
                    {self.config_do_random_size.get()} and {self.config_match_type.get()}"
            ))).grid(row=3,column=0,columnspan=2,sticky="ew")
        title_frame.grid(row=0,column=0,sticky="nsew")

    def game_board(self):
        """
            Creates a game board, very barebones.
        """
        board_dimension = 20
        board_side_length = 32*board_dimension

        new_window = tk.Toplevel(self.parent)
        new_window.geometry(f"{board_side_length}x{board_side_length}")
        if (self.config_do_ai_opponent):
            new_window.title("SOS Gameboard, vs AI")
        else:
            new_window.title("SOS Gameboard, vs Human")
        new_window.resizable(False,False)
        new_window.rowconfigure(0,weight=1)
        new_window.columnconfigure(0,weight=1)
        button_side_length = board_side_length//board_side_length
        game_board_frame = tk.Frame(new_window,width=board_side_length,height=board_side_length)
        for i in range(board_dimension):
            for j in range(board_dimension):
                coord = f"{i},{j}"
                button_frame = tk.Frame(game_board_frame, width=button_side_length, height=button_side_length)
                button_frame.rowconfigure(0,weight=1)
                button_frame.columnconfigure(0,weight=1)

                self.game_board_button_dict[coord] = ttk.Button(button_frame,text="", compound="center")
                self.game_board_button_dict[coord].grid(row=0,column=0,sticky="nsew")
                button_frame.grid(row=i,column=j,sticky="nsew")

                game_board_frame.columnconfigure(j,weight=1)
            game_board_frame.rowconfigure(i,weight=1)
        game_board_frame.grid(row=0,column=0,sticky="nsew")

def initialize_application():
    """initializes the application, but without starting mainloop."""
    root = tk.Tk()
    app = MainApplication(root)
    return app

if __name__ == "__main__":
    initialize_application().mainloop()
