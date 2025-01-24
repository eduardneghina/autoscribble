import os
import re
import sys
import time
import json
import random
import ast
import tkinter as tk
import logging

from cffi.cffi_opcode import PRIM_INT
from random_words import RandomWords
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from DataController import *

########################################################################################################################

class WebController:
    """Class to control web interactions using Selenium."""

    def __init__(self):
        """Initialize the WebController class."""
        self.db_path_directory = "C:\\Temp\\skribbl"
        os.makedirs(self.db_path_directory, exist_ok=True)

        self.data_path_file = "C:\\Temp\\skribbl\\data.txt"
        with open(self.data_path_file, 'w') as f:
            pass

        self.info_path_file = "C:\\Temp\\skribbl\\logs.txt"
        with open(self.info_path_file, 'w') as f:
            f.write("\n" + "=" * 50 + " New Session " + "=" * 50 + "\n")

        file_handler = logging.FileHandler(self.info_path_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        sys.stdout.reconfigure(encoding='utf-8')

########################################################################################################################

    def initiate_the_browser(self):
        """Initiate the browser with Brave or Chrome."""
        try:
            BROWSER_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            options = Options()
            options.binary_location = BROWSER_PATH
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
        except FileNotFoundError:
            logging.warning("Brave browser not detected, Chrome will be executed")
            logging.warning("Brave/Chrome browser is mandatory to be installed on the OS at default location")
            try:
                self.driver = webdriver.Chrome()
            except Exception as e:
                logging.error(f"Chrome browser could not be found - WebController - __init__ failed: {e}")
            else:
                logging.info("Chrome is active")
                self.driver.maximize_window()
        except Exception as e:
            logging.error(f"Failed to initiate the browser: {e}")

    def initiate_the_game(self):
        """Initiate the game by navigating to the provided link."""
        try:
            self.driver.get(self.get_input())
            logging.info("Browsing to the link with success")
            try:
                self.driver.find_element(By.CLASS_NAME, 'fc-primary-button').click()
            except Exception:
                logging.warning("Consent cookie button not found - pass")
            finally:
                time.sleep(1)
                self.insert_name()
                time.sleep(1)
                self.press_click_on_play()
                logging.info("The game is initiated")
                return True
        except Exception as e:
            logging.error(f"Failed to initiate the game: {e}")

    def get_input(self):
        """Get the game link from user input."""
        try:
            link_inserted = input("Enter a link: ")
            return link_inserted
        except Exception as e:
            logging.error(f"Failed to get input: {e}")

    def get_name(self):
        """Get the player name from user input."""
        try:
            inserted_name = input("Enter a name: ")
            logging.info(f"{inserted_name} name inserted")
            return inserted_name
        except Exception as e:
            logging.error(f"Failed to get name: {e}")

    def insert_name(self):
        """Insert the player name into the game."""
        try:
            name = self.get_name()
            self.driver.find_element(By.CLASS_NAME, 'input-name').send_keys(str(name))
        except Exception as e:
            logging.error(f"Failed to insert name: {e}")

    def press_click_on_play(self):
        """Press the play button to start the game."""
        try:
            element = self.driver.find_element(By.CLASS_NAME, 'button-play')
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click().perform()
        except Exception as e:
            logging.error(f"Failed to press click on play: {e}")

    def get_the_word(self):
        """Retrieve the current game word."""
        try:
            element = self.driver.find_element(By.ID, 'game-word')
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            #logging.info(f"The word is: {element.text}") # too many lines in logs
            return element.text
        except ElementNotInteractableException:
            logging.error("Element not interactable")
            return None
        except Exception as e:
            logging.error(f"Failed to get the word: {e}")



    def enter_a_word(self):
        """Enter a word in the game."""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            element = self.driver.find_element(By.XPATH, '//*[@id="game-chat"]/form/input')
            element.send_keys(RandomWords().random_word())
            element.send_keys(Keys.RETURN)
        except ElementNotInteractableException:
            logging.error("Element not interactable")
        except Exception as e:
            logging.error(f"Failed to enter a word: {e}")

    def check_word_status(self):
        """Continuously check the word status and perform actions based on the word."""
        while True:
            current_word = self.get_the_word()
            if current_word == "WAITING":
                logging.info("The game is in waiting mode.")
                # Wait until the word changes from 'WAITING' to something else
                while current_word == "WAITING":
                    time.sleep(1)
                    current_word = self.get_the_word()
                # logging.info(f"The word has changed to: {current_word}")
            elif current_word.startswith("DRAW THIS"):
                logging.info("The game is now in draw mode.")
                while current_word.startswith("DRAW THIS"):
                    time.sleep(1)
                    current_word = self.get_the_word()
            elif current_word.startswith("GUESS THIS"):
                logging.info("The game is in guess mode.")
                word_to_guess_raw = current_word.removeprefix("GUESS THIS")
                print(word_to_guess_raw)
                # Perform actions for other words
            time.sleep(1)  # Adjust the sleep time as needed to control the checking frequency