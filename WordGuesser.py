import logging
import time
import re

class WordGuesser:
    def __init__(self):
        pass

    def word_char_parser(self, word_from_webcontroller_object):
        """Continuously check the word and log if it has changed."""
        while True:
            try:
                # Get the word from the web controller
                word_raw = str(word_from_webcontroller_object.check_word_status())
                only_chars_word = re.sub('\d+', '', word_raw)
                return only_chars_word
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
                return only_numbers_word
                time.sleep(1)
            except Exception as e:
                logging.error(f"Failed to parse the word: {e}")