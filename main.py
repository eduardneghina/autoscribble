import os
import time
from WebController import *
from DataController import DataController

def main():
    WebControllerObject = WebController()
    WebControllerObject.initiate_the_browser()
    time.sleep(1)
    WebControllerObject.initiate_the_game()
    time.sleep(2)
    while True:
        print(WebControllerObject.get_the_word())
        time.sleep(10)
        WebControllerObject.enter_a_word()


if __name__ == "__main__":
    main()