"""
This module tests the application using unittest.
"""

import unittest
import tkinter as tk
import main

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

        elif acceptance_criteria in ("2.1", "2.2","3.1", "3.2", "6.3"):
            print(f"AC {acceptance_criteria}: Manual test required.")

        elif acceptance_criteria in ("5.1", "5.2", "5.3", "6.1", "6.2", "7.1", "7.2"):
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
        self.assertEqual(tile_to_click.button_instance.cget("disabledforeground"), "blue")

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
        tile_to_click.button_instance.config(text="O", state=tk.DISABLED, disabledforeground="red")
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

if __name__ == '__main__':
    unittest.main()
