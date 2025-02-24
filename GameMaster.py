import logging
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
                                # TEMPORARY FUNCTIONS

    def database_population_runner(self):
        self.WebControllerObject.initiate_the_browser()
        time.sleep(1)
        self.WebControllerObject.game_starter_no_link()
        time.sleep(1)
        while True:
            word = self.WordGuesserObject.get_only_the_word_parsed(self.WebControllerObject.check_word_status())
            self.WordGuesserObject.write_data(word)
            time.sleep(2)

########################################################################################################################

    def check_if_the_word_was_guessed(self):
       chat_text = self.WebControllerObject.extract_chat()
       string_to_search = self.WebControllerObject.player_name + " guessed the word"
       if string_to_search in chat_text:
           return True



    def game_runner(self):
        pass

