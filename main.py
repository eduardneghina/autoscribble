from WebController import *
from WordGuesser import *
import time



def main():
    WebControllerObject = WebController()
    WebControllerObject.initiate_the_browser()
    time.sleep(1)
    WebControllerObject.initiate_the_game()
    time.sleep(1)

if __name__ == "__main__":
    main()