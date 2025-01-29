import logging
import time
import re

class WordGuesser:
    def __init__(self):
        pass

    def word_parser(self, word_from_webcontroller):
        """Continuously check the word and log if it has changed."""
        while True:
            try:
                # Get the word from the web controller
                word_raw = str(word_from_webcontroller.check_word_status())
                print(word_raw)
                time.sleep(1)
            except Exception as e:
                logging.error(f"Failed to parse the word: {e}")