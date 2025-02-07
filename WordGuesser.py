import logging
import time
import re

class WordGuesser:
    def __init__(self):
        self.data_path_file = "C:\\Temp\\skribbl\\data.txt"

    def word_char_parser(self, word_from_webcontroller_object):
        """Parse the word and log if it has changed."""
        try:
            # Get the word from the web controller
            word_raw = str(word_from_webcontroller_object.check_word_status())
            only_chars_word = re.sub('\d+', '', word_raw)
            self.write_data(only_chars_word)
            self.find_matching_word(only_chars_word)
        except Exception as e:
            logging.error(f"Failed to parse the word: {e}")

    def word_number_parser(self, word_from_webcontroller_object):
        """Continuously check the word and return only the numbers of chars"""
        while True:
            try:
                # Get the word from the web controller
                word_raw = str(word_from_webcontroller_object.check_word_status())
                only_numbers_word = re.sub('\D+', '', word_raw)
                time.sleep(1)
            except Exception as e:
                logging.error(f"Failed to parse the word: {e}")


    def write_data(self, word_to_write_in_database):
        """Write the data/words to a database file."""
        try:
            # Check if the word contains no underscores and is not already in the file
            if '_' not in word_to_write_in_database:
                with open(self.data_path_file, 'r') as file:
                    words = file.read().splitlines()
                if word_to_write_in_database not in words:
                    with open(self.data_path_file, 'a') as file:
                        file.write(word_to_write_in_database + '\n')
                        logging.info(f"New word added: {word_to_write_in_database}")
                        time.sleep(3)
                else:
                    logging.info(f"Word already exists in database: {word_to_write_in_database}")
        except Exception as e:
            logging.error(f"Failed to write data: {e}")

    def read_all_words_from_database(self):
        """Read all the words from the database file."""
        try:
            with open(self.data_path_file, 'r') as f:
                word_list = [word.strip().lower() for word in f.readlines()]
            return word_list
        except FileNotFoundError:
            print(f"File {self.data_path_file} not found.")

    def find_matching_word(self, word_to_guess):
        """Find the best matching word from the database."""
        words = self.read_all_words_from_database()
        pattern = re.compile('^' + word_to_guess.replace('_', '.') + '$')

        # Initialize an empty list to store matches
        matches = []

        for word in words:
            if pattern.match(word):
                # Append each match to the list
                matches.append(word)

        return matches