"""
This module tests the application using unittest.
"""

import unittest
import tkinter as tk
import main
from game_logic import ComputerPlayer, Player
from unittest import mock

class TestFunctions(unittest.TestCase):
    """
        Class for testing application functions against Acceptance Criteria (AC).
    """
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

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
                   "7.1","7.2",
                   "8.1","8.2","8.3",
                   "9.1"]
        for ac in ac_list:
            with self.subTest(ac=ac):
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
        elif acceptance_criteria == "8.1":
            self.__test_ac_8_1()
        elif acceptance_criteria == "8.2":
            self.__test_ac_8_2()
        elif acceptance_criteria == "8.3":
            self.__test_ac_8_3()
        elif acceptance_criteria == "9.1":
            self.__test_ac_9_1()
        elif acceptance_criteria in ("2.1", "2.2","3.1", "3.2", "6.3"):
            print(f"AC {acceptance_criteria}: Manual test required.")
        elif acceptance_criteria in ("7.1", "7.2"):
            print(f"AC {acceptance_criteria}: Feature not complete.")
        else:
            print(f"AC {acceptance_criteria} not found")

    def __test_ac_1_1(self):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.game_board_dimension_variable.set(10)
        self.assertTrue(test_ma.game_logic.dimension_validate(),
                         "10 should be between the allowed dimension range.")

    def __test_ac_1_2(self):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.game_board_dimension_variable.set(2)
        self.assertFalse(test_ma.game_logic.dimension_validate(),
                         "2 should be smaller than the minimum allowed int: 3.")

    def __test_ac_1_3(self):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.game_board_dimension_variable.set(16)
        self.assertFalse(test_ma.game_logic.dimension_validate(),
                         "16 should be larger than the maximum allowed int: 15.")

    def __test_ac_4_1(self):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.game_board_dimension_variable.set(8)
        test_ma.game_logic.board_dimension = 8
        test_ma.game_logic.board_size = 64 
        
        test_ma.game_logic.create_players()
        
        win = test_ma.game_board(8)
        
        try:
            self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), 1)
            tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[2][2]
            test_ma.game_logic.on_tile_click(tile_to_click)
            
            self.assertEqual(tile_to_click.button_instance.cget("text"), "S")
            self.assertEqual(tile_to_click.button_instance.cget("state"), tk.DISABLED)
            self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), 2)
        finally:
            win.destroy()

    def __test_ac_4_2(self):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.game_board_dimension_variable.set(8)
        test_ma.game_logic.board_dimension = 8
        test_ma.game_logic.board_size = 64 
        
        test_ma.game_logic.create_players()

        win = test_ma.game_board(8)

        try:
            tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[3][3]
            tile_to_click.button_instance.config(text="O", state=tk.DISABLED, bg="#e94444")
            tile_to_click.owner = test_ma.game_logic.player_dict[2]

            original_text = tile_to_click.button_instance.cget("text")
            original_player_num = test_ma.game_logic.current_player_number_variable.get()

            test_ma.game_logic.on_tile_click(tile_to_click)

            self.assertEqual(tile_to_click.button_instance.cget("text"), original_text)
            self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), original_player_num)
        finally:
            win.destroy()

    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch.object(tk.Toplevel, 'destroy')
    def __test_ac_5_1(self, mock_destroy, mock_showinfo):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.game_board_dimension_variable.set(5)
        test_ma.game_logic.board_dimension = 5 
        test_ma.game_logic.board_size = 25 
        
        test_ma.game_logic.create_players()
        
        win = test_ma.game_board(5)
        test_ma.gui.master = win 

        test_ma.game_logic.config_match_type.set("Simple")
        
        test_ma.game_logic.gameboard_tile_instance_dict[2][2].button_instance.config(text="S")
        test_ma.game_logic.gameboard_tile_instance_dict[2][3].button_instance.config(text="O")
        
        test_ma.game_logic.current_player_number_variable.set(2)
        test_ma.game_logic.current_player_name_variable.set(test_ma.game_logic.player_dict[2].name)
        test_ma.game_logic.current_letter_variable.set("S")
        
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[2][4]
        test_ma.game_logic.on_tile_click(tile_to_click)
        
        mock_showinfo.assert_called_once()
        mock_destroy.assert_called_once()
        
        win.destroy()

    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch.object(tk.Toplevel, 'destroy')
    def __test_ac_5_2(self, mock_destroy, mock_showinfo):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.game_board_dimension_variable.set(5)
        test_ma.game_logic.board_dimension = 5
        test_ma.game_logic.board_size = 25 
        
        test_ma.game_logic.create_players()
        
        win = test_ma.game_board(5)
        test_ma.gui.master = win
        
        test_ma.game_logic.config_match_type.set("General")
        
        test_ma.game_logic.gameboard_tile_instance_dict[2][2].button_instance.config(text="S")
        test_ma.game_logic.gameboard_tile_instance_dict[2][3].button_instance.config(text="O")
        
        test_ma.game_logic.current_player_number_variable.set(2)
        test_ma.game_logic.current_player_name_variable.set(test_ma.game_logic.player_dict[2].name)
        test_ma.game_logic.current_letter_variable.set("S")
        
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[2][4]
        test_ma.game_logic.on_tile_click(tile_to_click)
        
        self.assertEqual(test_ma.game_logic.player_dict[2].score, 1)
        mock_destroy.assert_not_called()
        
        win.destroy()

    def _fill_board_for_draw(self, test_ma):
        board = test_ma.game_logic.gameboard_tile_instance_dict
        pattern = ['S', 'S', 'S', 'O', 'O', 'S', 'S', 'O']
        i = 0
        for y in range(3):
            for x in range(3):
                if y == 2 and x == 2:
                    continue
                board[y][x].button_instance.config(text=pattern[i])
                i += 1
        test_ma.game_logic.occupied_tile_count = 8

    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch.object(tk.Toplevel, 'destroy')
    def __test_ac_5_3(self, mock_destroy, mock_showinfo):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.game_board_dimension_variable.set(3)
        test_ma.game_logic.board_dimension = 3
        test_ma.game_logic.board_size = 9
        
        test_ma.game_logic.create_players()
        
        win = test_ma.game_board(3)
        test_ma.gui.master = win 
        
        test_ma.game_logic.config_match_type.set("Simple")
        
        self._fill_board_for_draw(test_ma)
        
        test_ma.game_logic.current_letter_variable.set("O")
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[2][2]
        test_ma.game_logic.on_tile_click(tile_to_click)
        
        mock_destroy.assert_called_once()
        mock_showinfo.assert_called_once()
        
        win.destroy()
    
    def __test_ac_6_1(self):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.game_board_dimension_variable.set(5)
        test_ma.game_logic.board_dimension = 5
        test_ma.game_logic.board_size = 25 
        
        test_ma.game_logic.create_players()
        
        win = test_ma.game_board(5)
        
        test_ma.game_logic.config_match_type.set("General")
        test_ma.game_logic.current_player_number_variable.set(2)
        test_ma.game_logic.current_player_name_variable.set(test_ma.game_logic.player_dict[2].name)
        test_ma.game_logic.current_letter_variable.set("S")
        
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[1][1]
        test_ma.game_logic.on_tile_click(tile_to_click)
        
        self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), 1)
        win.destroy()

    def __test_ac_6_2(self):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.game_board_dimension_variable.set(5)
        test_ma.game_logic.board_dimension = 5
        test_ma.game_logic.board_size = 25 
        
        test_ma.game_logic.create_players()
        
        win = test_ma.game_board(5)
        
        test_ma.game_logic.config_match_type.set("General")
        test_ma.game_logic.gameboard_tile_instance_dict[1][1].button_instance.config(text="S")
        test_ma.game_logic.gameboard_tile_instance_dict[3][3].button_instance.config(text="S")
        
        test_ma.game_logic.current_player_number_variable.set(2)
        test_ma.game_logic.current_player_name_variable.set(test_ma.game_logic.player_dict[2].name)
        test_ma.game_logic.current_letter_variable.set("O")
        
        tile_to_click = test_ma.game_logic.gameboard_tile_instance_dict[2][2]
        test_ma.game_logic.on_tile_click(tile_to_click)
        
        self.assertEqual(test_ma.game_logic.player_dict[2].score, 1)
        win.destroy()

    def __test_ac_8_1(self):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.config_blue_player_type.set("Human")
        test_ma.game_logic.config_red_player_type.set("Computer")
        
        test_ma.game_logic.create_players()
        
        self.assertIsInstance(test_ma.game_logic.player_dict[1], Player)
        self.assertNotIsInstance(test_ma.game_logic.player_dict[1], ComputerPlayer)
        self.assertIsInstance(test_ma.game_logic.player_dict[2], ComputerPlayer)

    def __test_ac_8_2(self):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.config_blue_player_type.set("Human")
        test_ma.game_logic.config_red_player_type.set("Computer")
        
        test_ma.game_logic.create_players()
        
        test_ma.game_logic.game_board_dimension_variable.set(5)
        test_ma.game_logic.board_dimension = 5
        test_ma.game_logic.board_size = 25 
        
        win = test_ma.game_board(5)
        try:
            self.assertEqual(test_ma.game_logic.config_red_player_type.get(), "Computer")
            self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), 1)
        finally:
            win.destroy()

    def __test_ac_8_3(self):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.config_blue_player_type.set("Human")
        test_ma.game_logic.config_red_player_type.set("Computer")
        
        test_ma.game_logic.create_players()
        
        test_ma.game_logic.game_board_dimension_variable.set(4)
        test_ma.game_logic.board_dimension = 4
        test_ma.game_logic.board_size = 16 
        
        win = test_ma.game_board(4)
        test_ma.gui.master = win

        try:
            captured_callbacks = []
            def mock_after(delay, callback=None):
                if callback:
                    captured_callbacks.append(callback)
                return "id"

            with mock.patch.object(win, 'after', side_effect=mock_after):
                tile_human = test_ma.game_logic.gameboard_tile_instance_dict[0][0]
                test_ma.game_logic.on_tile_click(tile_human)
                
                self.assertEqual(test_ma.game_logic.current_player_number_variable.get(), 2)
                self.assertTrue(len(captured_callbacks) > 0, "Computer did not schedule a move via .after()")
                
                computer_move_lambda = captured_callbacks[0]
                computer_move_lambda()
                
                self.assertEqual(test_ma.game_logic.occupied_tile_count, 2)
        finally:
            win.destroy()

    def __test_ac_9_1(self):
        test_ma = main.MainApplication(self.root)
        test_ma.game_logic.config_blue_player_type.set("Computer")
        test_ma.game_logic.config_red_player_type.set("Computer")
        
        test_ma.game_logic.create_players()
        
        self.assertIsInstance(test_ma.game_logic.player_dict[1], ComputerPlayer)
        self.assertIsInstance(test_ma.game_logic.player_dict[2], ComputerPlayer)
        self.assertNotEqual(test_ma.game_logic.player_dict[1], test_ma.game_logic.player_dict[2])

if __name__ == '__main__':
    unittest.main()