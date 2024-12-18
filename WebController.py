import os
import re
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
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from DataController import *

logging.basicConfig(level=logging.INFO)

########################################################################################################################

class WebController:
    """Class to control web interactions using Selenium."""

    def __init__(self):
        self.db_path_directory = "C:\\Temp\\skribbl"
        self.db_path_file = "C:\\Temp\\skribbl\\data.txt"
        self.last_value = None

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
        element = self.driver.find_element(By.ID, 'game-word')
        logging.info(f"The word is: {element.text}")
        return element.text