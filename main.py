from WebController import *
from GameMaster import *
from WordGuesser import *
import time

WebControllerObject = WebController()
WebControllerObject.initiate_the_browser()
WebControllerObject.initiate_the_game()
WordGuesserObject = WordGuesser()
while True:
    print("sa vedem ce scoate get_only_the_word_parsed ")
    print("================================================'")
    print(WordGuesserObject.get_only_the_word_parsed(WebControllerObject.check_word_status()))
    print("================================================'")
    print("sa vedem ce scoate get_only_the_lenght_of_words ")
    print("================================================'")
    print(WordGuesserObject.get_only_the_lenght_of_words(WebControllerObject.check_word_status()))
    print("================================================'")
    print("done")
    time.sleep(3)

