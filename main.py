from WebController import *
from GameMaster import *
from WordGuesser import *
import time



def main():

   # WebControllerObject = WebController()
   # WebControllerObject.initiate_the_browser()
    #WebControllerObject.initiate_the_game()
    #time.sleep(3)
    #print(WebControllerObject.check_word_status())

    GameMasterObject = GameMaster()
    GameMasterObject.game_runner()


if __name__ == "__main__":
    main()