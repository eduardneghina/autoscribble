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
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException



class WebController:
    """Class to control web interactions using Selenium."""

    def __init__(self):
        """Initialize the WebController class."""
        self.player_name = None

        self.db_path_directory = "C:\\Temp\\skribbl"
        os.makedirs(self.db_path_directory, exist_ok=True)

        self.data_path_file = "C:\\Temp\\skribbl\\data.txt"
        with open(self.data_path_file, 'a') as f:
            pass

        self.info_path_file = "C:\\Temp\\skribbl\\logs.txt"
        with open(self.info_path_file, 'a') as f:
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

    def initiate_the_browser(self):
        """Initiate the browser with Brave or Chrome."""
        try:
            browser_path= r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            options = Options()
            options.binary_location = browser_path
            options.add_argument("--incognito")
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
                time.sleep(1)
                logging.info("The game is initiated")
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
            self.player_name = input("Enter a name: ")
            logging.info(f"{self.player_name} name inserted")
            return self.player_name
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
        """Retrieve the current game word/mode"""
        try:
            element = self.driver.find_element(By.ID, 'game-word')
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element.text
        except ElementNotInteractableException:
            logging.error("Element not interactable")
            return None
        except Exception as e:
            logging.error(f"Failed to get the word: {e}")

    def extract_chat (self):
        try:
            chat = self.driver.find_element(By.ID, 'game-chat')
            return chat.text
        except Exception as e:
            logging.error(f"Failed to extract chat: {e}")



    def enter_one_word(self, word):
        """Enter a word in the game."""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            element = self.driver.find_element(By.XPATH, '//*[@id="game-chat"]/form/input')
            element.send_keys(word)
            element.send_keys(Keys.RETURN)
            #time.sleep(1)  # Adjust the sleep time as needed between entering words
            self.driver.execute_script("window.scrollTo(0, 0);")
        except ElementNotInteractableException:
            logging.error("Element not interactable")
        except Exception as e:
            logging.error(f"Failed to enter a word: {e}")



    def enter_words_from_a_list(self, words_list):
        """Enter words from the given list one by one in the game."""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            element = self.driver.find_element(By.XPATH, '//*[@id="game-chat"]/form/input')
            for word in words_list:
                element.send_keys(word)
                element.send_keys(Keys.RETURN)
                time.sleep(1)  # Adjust the sleep time as needed between entering words
                self.driver.execute_script("window.scrollTo(0, 0);")
        except ElementNotInteractableException:
            logging.error("Element not interactable")
        except Exception as e:
            logging.error(f"Failed to enter a word: {e}")



    def check_word_status(self):
        """Check the word status and perform actions based on the word."""
        current_status = self.get_the_word()
        if current_status == "WAITING":
            logging.info("The game is in waiting mode.")
            return "WAITING"
        elif current_status.startswith("DRAW THIS"):
            logging.info("The game is now in draw mode.")
            word_to_draw = current_status.removeprefix("DRAW THIS").strip()
            logging.info(f"The word to draw is: {word_to_draw}")
            return "DRAW " + word_to_draw
        elif current_status.startswith("GUESS THIS"):
            logging.info("The game is in guessing mode.")
            word_to_guess_raw = current_status.removeprefix("GUESS THIS")
            word_to_guess = word_to_guess_raw.replace("\n", "")
            return word_to_guess
        return None


    def game_starter_no_link(self):
        #temporary function for database population
        self.driver.get("https://skribbl.io/?TPC5Qthp")
        self.driver.find_element(By.CLASS_NAME, 'fc-primary-button').click()
        self.insert_name()
        time.sleep(1)
        self.select_language()
        time.sleep(1)
        self.press_click_on_play()
        time.sleep(1)

    def select_language(self):
        self.driver.find_element(By.XPATH, '//*[@id="home"]/div[2]/div[2]/div[1]/select').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="home"]/div[2]/div[2]/div[1]/select/option[21]').click()
        time.sleep(1)