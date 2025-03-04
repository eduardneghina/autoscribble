from WebController import *
from WordGuesser import *
from GameMaster import *
import time

def main():
    GameMasterObject = GameMaster()
    GameMasterObject.game_starter()
    GameMasterObject.game_runner()

if __name__ == '__main__':
    main()