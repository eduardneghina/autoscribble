

class DataController:
    """Class to control data interactions."""

    def __init__(self):
        pass

    def check_word_status(self):
        """Continuously check the word status and perform actions based on the word."""
        while True:
            try:
                word = self.get_the_word()
                if word == "WAITING":
                    logging.info("The game is in waiting mode.")
                    #
                elif word == "DRAW THIS":
                    logging.info("It's your turn to draw.")
                    #
                else:
                    logging.info(f"The current word is: {word}")
                    #
            except NoSuchElementException:
                logging.error("Failed to retrieve the word.")
            time.sleep(1)  # Adjust the sleep time as needed to control the checking frequency