import logging
import time
import re




class WordGuesser:
    """Class for guessing the word mechanism."""
    def __init__(self):
        self.data_path_file = "C:\\Temp\\skribbl\\data.txt"

########################################################################################################################

    def write_data(self, word_to_write_in_database):
        """Write the data to a file."""
        try:
            if '_' not in word_to_write_in_database:
                with open(self.data_path_file, 'r', encoding='utf-8') as file:
                    words = file.read().splitlines()
                if word_to_write_in_database not in words:
                    with open(self.data_path_file, 'a', encoding='utf-8') as file:
                        file.write(word_to_write_in_database + '\n')
                        logging.info(f"New word added: {word_to_write_in_database}")
                        time.sleep(3)
                else:
                    logging.info(f"Word already exists in database: {word_to_write_in_database}")
        except Exception as e:
            logging.error(f"Failed to write data: {e}")



    def get_only_the_word_parsed(self, raw_word_from_webcontroller):
        """Parse the word and log if it has changed."""
        try:
            # Get the word from the web controller
            word_raw = str(raw_word_from_webcontroller)
            if word_raw is not None:
                only_chars_word = re.sub('\d+', '', word_raw)
                return only_chars_word
        except Exception as e:
            logging.error(f"Failed to parse the word: {e}")



    def get_only_the_lenght_of_words(self, raw_word_from_webcontroller):
        """Check the word and return only the numbers of chars"""
        try:
            # Get the word from the web controller
            word_raw = str(raw_word_from_webcontroller)
            only_numbers_word = re.sub('\D+', '', word_raw)
            return only_numbers_word
        except Exception as e:
            logging.error(f"Failed to parse the word: {e}")



    def read_all_words_from_database(self):
        """Read all the words from the database file."""
        try:
            with open(self.data_path_file, 'r') as f:
                word_list = [word.strip().lower() for word in f.readlines()]
            return word_list
        except FileNotFoundError:
            print(f"File {self.data_path_file} not found.")



    def find_matching_words(self, word_to_guess_raw):
        """Find the best matching word from the database."""
        words = self.read_all_words_from_database()
        word_parsed = self.get_only_the_word_parsed(word_to_guess_raw)
        pattern = re.compile('^' + word_parsed.replace('_', '.') + '$')
        # Initialize an empty list to store matches
        matches = []
        for word in words:
            if pattern.match(word):
                # Append each match to the list
                matches.append(word)

        return matches