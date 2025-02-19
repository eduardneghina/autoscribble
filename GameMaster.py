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

#need to handle the cases of the word like waiting and drawing

    def game_runner(self):
        self.WebControllerObject.initiate_the_browser()
        time.sleep(1)
        self.WebControllerObject.initiate_the_game()
        time.sleep(1)

        while True:
            word = self.WordGuesserObject.get_only_the_word_parsed(self.WebControllerObject.check_word_status())
            words_to_try_list = self.WordGuesserObject.find_matching_words(word)
            print(words_to_try_list)
            if 0 < len(words_to_try_list) < 5:
                while self.chat_checker() is not True:
                    self.WebControllerObject.enter_one_word(words_to_try_list[0])
                    logging.info(f"Word entered: {words_to_try_list[0]}")
                    time.sleep(1)
                else:
                    logging.info("The word has been guessed.")
                    logging.info("The word was : " + words_to_try_list[0])



    def chat_checker(self):
       chat_text = self.WebControllerObject.extract_chat()
       string_to_search = self.WebControllerObject.player_name + " guessed the word"
       if string_to_search in chat_text:
           return True