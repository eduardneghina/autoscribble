from WebController import *
from WordGuesser import *
import time



def main():
    WebControllerObject = WebController()
    WebControllerObject.initiate_the_browser()
    time.sleep(1)
    WebControllerObject.initiate_the_game()
    time.sleep(1)

    WordGuesserObject = WordGuesser()
    WordGuesserObject.write_data(WordGuesserObject.word_char_parser(WebControllerObject))
    print("ajung aici ?")





if __name__ == "__main__":
    main()