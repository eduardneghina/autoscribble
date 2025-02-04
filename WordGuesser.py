import logging
import time
import re

class WordGuesser:
    def __init__(self):
        self.data_path_file = "C:\\Temp\\skribbl\\data.txt"

    def word_char_parser(self, word_from_webcontroller_object):
        """Continuously check the word and log if it has changed."""
        while True:
            try:
                # Get the word from the web controller
                word_raw = str(word_from_webcontroller_object.check_word_status())
                only_chars_word = re.sub('\d+', '', word_raw)
                self.write_data(only_chars_word)
                time.sleep(1)
            except Exception as e:
                logging.error(f"Failed to parse the word: {e}")

    def word_number_parser(self, word_from_webcontroller_object):
        """Continuously check the word and log if it has changed."""
        while True:
            try:
                # Get the word from the web controller
                word_raw = str(word_from_webcontroller_object.check_word_status())
                only_numbers_word = re.sub('\D+', '', word_raw)
                time.sleep(1)
            except Exception as e:
                logging.error(f"Failed to parse the word: {e}")


    def write_data(self, word_to_write_in_database):
        """Write the data to a file."""
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