import os
import time
from WebController import *
from DataController import *

def main():

    WebControllerObject = WebController()
    print(WebControllerObject.initiate_the_browser())
    print("00000000000000000000")
    print(WebControllerObject.initiate_the_game())


if __name__ == "__main__":
    main()