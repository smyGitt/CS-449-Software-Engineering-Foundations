"""
This module tests the application using unittest.
"""

import unittest
import tkinter as tk
import main
from unittest import mock

class TestFunctions(unittest.TestCase):
    """
        Class for testing new functions.
    """
    def test_all_ac(self):
        """
            test automatic test cases for all AC.
        """
        ac_list = ["1.1","1.2","1.3",
                   "2.1","2.2",
                   "3.1","3.2",
                   "4.1","4.2",
                   "5.1","5.2","5.3",
                   "6.1","6.2","6.3",
                   "7.1","7.2"]
        for ac in ac_list:
            self.perform_unittest(ac)

    def perform_unittest(self, acceptance_criteria:str):
        """
            Performs unit test with the given acceptance criteria.
        """
        if acceptance_criteria == "1.1":
            self.__test_ac_1_1()

        elif acceptance_criteria == "1.2":
            self.__test_ac_1_2()
  
        elif acceptance_criteria == "1.3":
            self.__test_ac_1_3()

        elif acceptance_criteria == "4.1":
            self.__test_ac_4_1()
            
        elif acceptance_criteria == "4.2":
            self.__test_ac_4_2()

        elif acceptance_criteria == "5.1":
            self.__test_ac_5_1()

        elif acceptance_criteria == "5.2":
            self.__test_ac_5_2()

        elif acceptance_criteria == "5.3":
            self.__test_ac_5_3()

        elif acceptance_criteria == "6.1":
            self.__test_ac_6_1()
        
        elif acceptance_criteria == "6.2":
            self.__test_ac_6_2()

        elif acceptance_criteria in ("2.1", "2.2","3.1", "3.2", "6.3"):
            print(f"AC {acceptance_criteria}: Manual test required.")

        elif acceptance_criteria in ("7.1", "7.2"):
            print(f"AC {acceptance_criteria}: Feature not complete.")

        else:
            print(f"AC {acceptance_criteria} not found")

    def __test_ac_1_1(self):
        test_ma = main.MainApplication(tk.Frame())
        test_ma.game_logic.game_board_dimension_variable.set(10)
        self.assertTrue(test_ma.game_logic.dimension_validate(),
                         "10 should be between the allowed dimension range.")

    def __test_ac_1_2(self):
        test_ma = main.MainApplication(tk.Frame())
        test_ma.game_logic.game_board_dimension_variable.set(2)
        self.assertFalse(test_ma.game_logic.dimension_validate(),
                         "2 should be smaller than the minimum allowed int: 3.")

    def __test_ac_1_3(self):
        test_ma = main.MainApplication(tk.Frame())
        test_ma.game_logic.game_board_dimension_variable.set(16)
        self.assertFalse(test_ma.game_logic.dimension_validate(),
                         "16 should be larger than the maximum allowed int: 15.")

    def __test_ac_4_1(self):
        """
        Tests AC 4.1: Player makes a valid, non-winning move.
        """
        test_ma = main.MainApplication(tk.Frame())
        test_ma.game_logic.game_board_dimension_variable.set(8)
        test_ma.game_board(8)

        # Given: Blue player's turn (default) and 'S' selected (default)
        self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), 1)
        self.assertEqual(test_ma.game_logic.current_letter_variable.get(), "S")

        # When: The player clicks an empty cell (e.g., at [2][2])
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[2][2]
        test_ma.game_logic.on_tile_click(tile_to_click)

        # Then: An 'S' appears at the selected cell
        self.assertEqual(tile_to_click.button_instance.cget("text"), "S")
        
        # Then: The button is disabled with the correct player color
        self.assertEqual(tile_to_click.button_instance.cget("state"), tk.DISABLED)
        self.assertEqual(tile_to_click.button_instance.cget("bg"), "#70b8fa")

        # Then: The turn indicator switches to "Red player's turn"
        self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), 2)
        self.assertEqual(test_ma.game_logic.current_player_name_variable.get(), "Red Two")
        
        # Then: The tile is now owned by Player 1
        self.assertIn(tile_to_click, test_ma.game_logic.player_dict[1].owned_tile["S"])

    def __test_ac_4_2(self):
        """
        Tests AC 4.2: Player attempts to move on an occupied cell.
        """
        test_ma = main.MainApplication(tk.Frame())
        test_ma.game_logic.game_board_dimension_variable.set(8)
        test_ma.game_board(8)

        # Given: It is the Blue player's turn (default)
        self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), 1)

        # Given: The chosen cell already contains a letter (manually set)
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[3][3]
        # Manually occupy the tile (e.g., by the Red player)
        tile_to_click.button_instance.config(text="O", state=tk.DISABLED, bg="#e94444")
        tile_to_click.owner = test_ma.game_logic.player_dict[2]

        # Store the state *before* the invalid click
        original_text = tile_to_click.button_instance.cget("text") # Should be "O"
        original_player_num = test_ma.game_logic.current_player_number_variable.get() # Should be 1
        original_player_name = test_ma.game_logic.current_player_name_variable.get() # "Blue One"

        # When: The player clicks a non-empty cell
        # Note: In the real app, the tk.DISABLED state blocks the GUI click.
        # This test calls the logic function directly to test its robustness.
        test_ma.game_logic.on_tile_click(tile_to_click)

        # Then: The board and selected cell remains unchanged
        self.assertEqual(tile_to_click.button_instance.cget("text"), original_text,
                         "AC 4.2 Test Fail: Button text changed on an occupied tile.")
        
        # Then: The turn indicator still shows "Blue player's turn"
        self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), original_player_num,
                         "AC 4.2 Test Fail: Player turn switched on an invalid move.")
        self.assertEqual(test_ma.game_logic.current_player_name_variable.get(), original_player_name,
                         "AC 4.2 Test Fail: Player name switched on an invalid move.")

    @mock.patch('tkinter.messagebox.showinfo') # Mocks the popup function
    @mock.patch.object(tk.Toplevel, 'destroy') # Mocks the window destroy function
    def __test_ac_5_1(self, mock_destroy, mock_showinfo):
        """
        Tests AC 5.1: A player wins the game in ‘Casual’ match.
        """
        test_ma = main.MainApplication(tk.Frame())
        test_ma.game_logic.game_board_dimension_variable.set(5)
        test_ma.game_logic.master = test_ma.game_board(5)
        
        # Given: A 'Casual' match is in progress
        test_ma.game_logic.config_match_type.set("casual")
        
        # Given: An 'S' at (2,2) and an 'O' at (2,3)
        test_ma.game_logic.gameboard_tile_instance_dict[2][2].button_instance.config(text="S")
        test_ma.game_logic.gameboard_tile_instance_dict[2][3].button_instance.config(text="O")
        
        # Given: It is the Red player's turn
        test_ma.game_logic.current_player_number_variable.set(2)
        test_ma.game_logic.current_player_name_variable.set(test_ma.game_logic.player_dict[2].name)
        
        # Given: The Red player selects 'S'
        test_ma.game_logic.current_letter_variable.set("S")
        
        # When: The Red player places an 'S' at (2,4)
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[2][4]
        test_ma.game_logic.on_tile_click(tile_to_click)
        
        # Then: The game immediately ends
        # We check if the popup was called and the window was destroyed
        mock_showinfo.assert_called_once_with(parent=test_ma.game_logic.master, 
                                              title="Game Over!", 
                                              message="Red Two won the game!")
        mock_destroy.assert_called_once()
        
        # Then: The S-O-S tiles are colored
        red_color = test_ma.game_logic.player_dict[2].color
        self.assertEqual(test_ma.game_logic.gameboard_tile_instance_dict[2][2].button_instance.cget("bg"), red_color)
        self.assertEqual(test_ma.game_logic.gameboard_tile_instance_dict[2][3].button_instance.cget("bg"), red_color)
        self.assertEqual(test_ma.game_logic.gameboard_tile_instance_dict[2][4].button_instance.cget("bg"), red_color)

    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch.object(tk.Toplevel, 'destroy')
    def __test_ac_5_2(self, mock_destroy, mock_showinfo):
        """
        Tests AC 5.2: A player wins a point in 'Competitive' match (game continues).
        """
        test_ma = main.MainApplication(tk.Frame())
        test_ma.game_logic.game_board_dimension_variable.set(5)
        test_ma.game_logic.master = test_ma.game_board(5)
        
        # Given: A 'Competitive' (ranked) match is in progress
        test_ma.game_logic.config_match_type.set("ranked")
        
        # Given: An 'S' at (2,2) and an 'O' at (2,3)
        test_ma.game_logic.gameboard_tile_instance_dict[2][2].button_instance.config(text="S")
        test_ma.game_logic.gameboard_tile_instance_dict[2][3].button_instance.config(text="O")
        
        # Given: It is the Red player's turn
        test_ma.game_logic.current_player_number_variable.set(2)
        test_ma.game_logic.current_player_name_variable.set(test_ma.game_logic.player_dict[2].name)
        
        # Given: The Red player selects 'S'
        test_ma.game_logic.current_letter_variable.set("S")
        
        # When: The Red player places an 'S' at (2,4)
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[2][4]
        test_ma.game_logic.on_tile_click(tile_to_click)
        
        # Then: The game keeps going
        mock_showinfo.assert_not_called()
        mock_destroy.assert_not_called()
        
        # Then: The S-O-S tiles are colored
        red_color = test_ma.game_logic.player_dict[2].color
        self.assertEqual(test_ma.game_logic.gameboard_tile_instance_dict[2][2].button_instance.cget("bg"), red_color)
        self.assertEqual(test_ma.game_logic.gameboard_tile_instance_dict[2][3].button_instance.cget("bg"), red_color)
        self.assertEqual(test_ma.game_logic.gameboard_tile_instance_dict[2][4].button_instance.cget("bg"), red_color)
        
        # Then: 1 point is added to Red player's score
        self.assertEqual(test_ma.game_logic.player_dict[2].score, 1)
        
        # Then: It is still Red's turn (since they scored)
        self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), 2)

        test_ma.game_logic.master.destroy()

    def _fill_board_for_draw(self, test_ma):
        """Helper function to fill a 3x3 board for a draw."""
        # Fill 8 of 9 tiles in a non-scoring pattern
        board = test_ma.game_logic.gameboard_tile_instance_dict
        pattern = ['S', 'S', 'S', 'O', 'O', 'S', 'S', 'O']
        i = 0
        for y in range(3):
            for x in range(3):
                if y == 2 and x == 2: # Leave (2,2) empty
                    continue
                board[y][x].button_instance.config(text=pattern[i])
                i += 1
        # Manually set occupied count
        test_ma.game_logic.occupied_tile_count = 8

    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch.object(tk.Toplevel, 'destroy')
    def __test_ac_5_3(self, mock_destroy, mock_showinfo):
        """
        Tests AC 5.3: The game ends in a draw (Casual).
        """
        test_ma = main.MainApplication(tk.Frame())
        test_ma.game_logic.game_board_dimension_variable.set(3)
        test_ma.game_logic.master = test_ma.game_board(3)
        
        # Given: A 'Casual' match is in progress
        test_ma.game_logic.config_match_type.set("casual")
        
        # Given: The board is full except for one cell
        self._fill_board_for_draw(test_ma)
        self.assertEqual(test_ma.game_logic.player_dict[1].score, 0)
        self.assertEqual(test_ma.game_logic.player_dict[2].score, 0)

        # When: The final move is made, and it does not form an S-O-S
        # Player 1 places an 'O' at (2,2)
        test_ma.game_logic.current_letter_variable.set("O")
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[2][2]
        test_ma.game_logic.on_tile_click(tile_to_click)
        
        # Then: The game ends
        mock_destroy.assert_called_once()
        
        # Then: A message declares "The game is a draw"
        mock_showinfo.assert_called_once_with(parent=test_ma.game_logic.master, 
                                              title="Game Over!", 
                                              message="Tied! Nobody wins!")
        
        # Then: No points given
        self.assertEqual(test_ma.game_logic.player_dict[1].score, 0)
        self.assertEqual(test_ma.game_logic.player_dict[2].score, 0)
    
    def __test_ac_6_1(self):
        """Tests AC 6.1: Player makes a non-scoring move (General Game)."""
        test_ma = main.MainApplication(tk.Frame())
        test_ma.game_logic.game_board_dimension_variable.set(5)
        test_ma.game_logic.master = test_ma.game_board(5)
        
        # Given: A 'Ranked' (General) match
        test_ma.game_logic.config_match_type.set("ranked")
        
        # Given: It is the Red player's turn
        test_ma.game_logic.current_player_number_variable.set(2)
        test_ma.game_logic.current_player_name_variable.set(test_ma.game_logic.player_dict[2].name)
        test_ma.game_logic.current_letter_variable.set("S")
        
        # When: The player places a letter that does not form an S-O-S
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[1][1]
        test_ma.game_logic.on_tile_click(tile_to_click)
        
        # Then: The turn indicator switches to "Blue player's turn"
        self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), 1)
        self.assertEqual(test_ma.game_logic.current_player_name_variable.get(), "Blue One")
        
        # And: No score was added
        self.assertEqual(test_ma.game_logic.player_dict[2].score, 0)
        
        test_ma.game_logic.master.destroy()

    def __test_ac_6_2(self):
        """Tests AC 6.2: Player makes a scoring move (General Game)."""
        test_ma = main.MainApplication(tk.Frame())
        test_ma.game_logic.game_board_dimension_variable.set(5)
        test_ma.game_logic.master = test_ma.game_board(5)
        
        # Given: A 'Ranked' (General) match
        test_ma.game_logic.config_match_type.set("ranked")
        
        # Given: 'S' at (1,1) and 'S' at (3,3)
        test_ma.game_logic.gameboard_tile_instance_dict[1][1].button_instance.config(text="S")
        test_ma.game_logic.gameboard_tile_instance_dict[3][3].button_instance.config(text="S")
        
        # Given: It is the Red player's turn
        test_ma.game_logic.current_player_number_variable.set(2)
        test_ma.game_logic.current_player_name_variable.set(test_ma.game_logic.player_dict[2].name)
        
        # Given: Red player selects 'O'
        test_ma.game_logic.current_letter_variable.set("O")
        
        # When: The Red player places an 'O' at (2,2)
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[2][2]
        test_ma.game_logic.on_tile_click(tile_to_click)
        
        # Then: The Red player's score is incremented
        self.assertEqual(test_ma.game_logic.player_dict[2].score, 1)
        
        # Then: A red line connects the S-O-S (check colors)
        red_color = test_ma.game_logic.player_dict[2].color
        self.assertEqual(test_ma.game_logic.gameboard_tile_instance_dict[1][1].button_instance.cget("bg"), red_color)
        self.assertEqual(test_ma.game_logic.gameboard_tile_instance_dict[2][2].button_instance.cget("bg"), red_color)
        self.assertEqual(test_ma.game_logic.gameboard_tile_instance_dict[3][3].button_instance.cget("bg"), red_color)
        
        # Then: The turn stays on Red player’s turn
        self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), 2)
        self.assertEqual(test_ma.game_logic.current_player_name_variable.get(), "Red Two")
        
        test_ma.game_logic.master.destroy()

if __name__ == '__main__':
    unittest.main()
