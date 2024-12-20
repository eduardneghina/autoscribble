import os
import re
import sys
import time
import json
import random
import ast
import tkinter as tk
import logging
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
        # Ensure the directory exists
        os.makedirs(self.db_path_directory, exist_ok=True)

        self.data_path_file = "C:\\Temp\\skribbl\\data.txt"
        # Ensure the data file is created
        with open(self.data_path_file, 'w') as f:
            pass

        self.info_path_file = "C:\\Temp\\skribbl\\logs.txt"
        # Ensure the log file is created
        with open(self.info_path_file, 'w') as f:
            f.write("\n" + "=" * 50 + " New Session " + "=" * 50 + "\n")
            pass

        # Configure logging to file
        file_handler = logging.FileHandler(self.info_path_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Add console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Get the root logger and set its level
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Set the console encoding to utf-8 to avoid encoding issues for romanian characters
        sys.stdout.reconfigure(encoding='utf-8')

#########################################################################################################################

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

    def initiate_the_game(self):
        """Initiate the game by navigating to the provided link."""
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

    def get_input(self):
        """Get the game link from user input."""
        link_inserted = input("Enter a link: ")
        return link_inserted

    def get_name(self):
        """Get the player name from user input."""
        inserted_name = input("Enter a name: ")
        logging.info(f"{inserted_name} name inserted")
        return inserted_name

    def insert_name(self):
        """Insert the player name into the game."""
        name = self.get_name()
        self.driver.find_element(By.CLASS_NAME, 'input-name').send_keys(str(name))

    def press_click_on_play(self):
        """Press the play button to start the game."""
        element = self.driver.find_element(By.CLASS_NAME, 'button-play')
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

    def get_the_word(self):
        """Retrieve the current game word."""
        try:
            element = self.driver.find_element(By.ID, 'game-word')
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            logging.info(f"The word is: {element.text}")
            return element.text
        except ElementNotInteractableException:
            logging.error("Element not interactable")
            return None

    def enter_a_word(self):
        """Enter a word in the game."""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            element = self.driver.find_element(By.XPATH, '//*[@id="game-chat"]/form/input')
            element.send_keys(RandomWords().random_word())
            element.send_keys(Keys.RETURN)
        except ElementNotInteractableException:
            logging.error("Element not interactable")