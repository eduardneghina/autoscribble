import logging
import time
from WebController import *
from WordGuesser import *
import sys


class GameMaster:
    """Class to control the game."""

    def __init__(self):
        """Initialize the GameMaster class."""
        # Determine the directory of the executable or script
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app
            # path into variable _MEIPASS'.
            script_dir = sys._MEIPASS
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to data.txt relative to the script directory
        self.data_path_file = os.path.join(script_dir, 'data.txt')
        self.WebControllerObject = WebController()
        self.WordGuesserObject = WordGuesser()

    def game_runner(self):
        game_status = self.WebControllerObject.check_word_status()
        while game_status is not None:
            if game_status == "WAITING":
                time.sleep(1)
                game_status = self.WebControllerObject.check_word_status()
            elif game_status.startswith("DRAW"):
                time.sleep(1)
                game_status = self.WebControllerObject.check_word_status()
                self.WordGuesserObject.write_data(game_status.removeprefix("DRAW ").strip())
            elif game_status.startswith("GUESS"):
                time.sleep(1)
                word_to_guess_raw = self.WordGuesserObject.get_only_the_word_parsed(game_status) # the return is GUESS THIS word
                word_to_guess = word_to_guess_raw.removeprefix("GUESS THIS").strip() # only the word
                print("The word to guess is: " + word_to_guess.removeprefix("GUESS ").strip())
                if '_' not in word_to_guess:
                    self.WordGuesserObject.write_data(word_to_guess.removeprefix("GUESS ").strip())
                words_list = self.WordGuesserObject.find_matching_words(word_to_guess.removeprefix("GUESS "))
                print("The words list is: " + str(words_list))
                if not words_list:
                    logging.info("No matching words found.")
                    game_status = self.WebControllerObject.check_word_status()
                elif len(words_list) < 4:
                    logging.info("Less than 4 matching words found.")
                    print(words_list)
                    self.WebControllerObject.enter_words_from_a_list(words_list)
                    game_status = self.WebControllerObject.check_word_status()
                    if self.check_if_the_word_was_guessed() == True:
                        logging.info("The word was guessed : " + word_to_guess.removeprefix("GUESS ").strip())
                elif len(words_list) >= 4:
                    logging.info("More than 4 matching words found - Keep searching")
                    game_status = self.WebControllerObject.check_word_status()


    def game_starter(self):
        self.WebControllerObject.initiate_the_browser()
        self.WebControllerObject.initiate_the_game()


    def check_if_the_word_was_guessed(self):
       chat_text = self.WebControllerObject.extract_chat()
       string_to_search = self.WebControllerObject.player_name + " guessed the word"
       if string_to_search in chat_text:
           return True
