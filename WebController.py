import os
import re
import time
import json
from random_words import RandomWords
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
#from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from DataController import *
import random
import ast
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class WebController:
    def __init__(self):

        self.db_path_directory = "C:\\Temp\\skribbl"
        self.db_path_file = "C:\\Temp\\skribbl\\data.txt"
        self.last_value = None

    def initiate_the_browser(self):
        try:
            #C:\Program Files\BraveSoftware\Brave-Browser\Application
            BROWSER_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            options = Options()
            options.binary_location = BROWSER_PATH
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
        except:
            print("Brave browser not detected, Chrome will pe executed")
            print("Brave/Chrome browser is mandatory to be installed on the OS at default location")
            try:
                self.driver = webdriver.Chrome()
            except:
                # N-am nici o idee cum sa fac handle la asta in a real way
                print("Chrome browser could not be found - WebController - __init__ failed")
            else:
                print("Chrome is active")
                self.driver.maximize_window()

    def initiate_the_game(self):
        self.driver.get(self.get_input())
        print("Browsing to the link with success")
        try:
            self.driver.find_element(By.CLASS_NAME, 'fc-primary-button').click()
        except:
            print("Consent cookie button not found - pass")
            pass
        else:
            pass
        finally:
            self.insert_name()
            time.sleep(1)
            self.press_click_on_play()
            print("The game is initiated")
            return True

    def get_input(self):
        link_inserted = input("Enter a link: ")
        return link_inserted

    def get_name(self):
        inserted_name = input("Enter a name: ")
        print(f"{inserted_name} name inserted")
        return inserted_name

    def insert_name(self):
        name = self.get_name()
        self.driver.find_element(By.CLASS_NAME, 'input-name').send_keys(str(name))

    def press_click_on_play(self):
        element = self.driver.find_element(By.CLASS_NAME, 'button-play')
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()


    def get_the_word(self):
        element = self.driver.find_element(By.ID, 'game-word')
        print("The word is :")
        print(element.text)
        return element.text



