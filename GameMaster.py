import time

from WebController import *
from WordGuesser import *


class GameMaster:
    """Class to control the game."""

    def __init__(self):
        """Initialize the GameMaster class."""
        self.data_path_file = "C:\\Temp\\skribbl\\data.txt"
        self.WebControllerObject = WebController()
        self.WordGuesserObject = WordGuesser()

########################################################################################################################

    def game_runner(self):
        self.WebControllerObject.initiate_the_browser()
        time.sleep(1)
        self.WebControllerObject.initiate_the_game()
        time.sleep(1)
        while True:
            word = self.WordGuesserObject.get_only_the_word_parsed(self.WebControllerObject.check_word_status())
            words_to_try_list = self.WordGuesserObject.find_matching_words(word)
            print(words_to_try_list)
            if 0 < len(words_to_try_list) < 7:
                self.WebControllerObject.enter_a_word(words_to_try_list)
            else:
                pass
# de facut sa se opreasca cand vede ca am ghicit
# ceva ai de ales mai bine din lista returnata de find_matching_words
# compararea cu baza de date reala din game si nu cu cea din fisier