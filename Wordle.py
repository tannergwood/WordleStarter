# File: Wordle.py

"""
This module is the starter file for the Wordle assignment.
BE SURE TO UPDATE THIS COMMENT WHEN YOU WRITE THE CODE.
"""

# This is Nate's test comment

import random
from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS, CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR, UNKNOWN_COLOR, KEY_COLOR

# MAKE THE GAME END ONCE THERE ARE SIX GUESSES
def wordle():
    # SELECT A RANDOM WORD and MAKE IT UPPERCASE
    word = random.choice(FIVE_LETTER_WORDS).upper()
    print(word)

    def enter_action(s):

        # RETRIEVE WORD FROM WORDLE
        inputWord = ""
        for x in range(0, N_COLS):
            letter = WordleGWindow.get_square_letter(gw, WordleGWindow.get_current_row(gw), x)
            inputWord = inputWord + letter

        #MILESTONE 2 MAKE SURE THE WORD IS AN ENGLISH WORD
        if (inputWord.lower() in FIVE_LETTER_WORDS):

            # UPDATE KEYBOARD COLORS
            #for letter in inputWord :
                #gw.set_key_color(letter, )

            # TEST IF THE WORD IS CORRECT
            if (inputWord == word):
                #COLOR ALL LETTERS GREEN
                for x in range(0, N_COLS):
                    gw.set_square_color(WordleGWindow.get_current_row(gw), x, CORRECT_COLOR)
                    # UPDATE THE KEYBOARD COLORS
                    for letter in inputWord :
                        gw.set_key_color(letter, CORRECT_COLOR)
                gw.show_message("You Guessed the Word!")
            else:
                # COLOR THE LETTERS
                for x in range(0, N_COLS):
                    # SET LETTERS IN THE CORRECT POSITION TO GREEN
                    if (inputWord[x] == word[x]):
                        gw.set_square_color(WordleGWindow.get_current_row(gw), x, CORRECT_COLOR)
                        # ADD MATCHING COLOR TO KEYBOARD
                        gw.set_key_color(inputWord[x], CORRECT_COLOR)
                    # COLOR PRESENT LETTERS IN WRONG POSITION YELLOW
                    elif(inputWord[x] in word):
                        gw.set_square_color(WordleGWindow.get_current_row(gw), x, PRESENT_COLOR)
                        # ADD MATCHING COLOR TO KEYBOARD
                        gw.set_key_color(inputWord[x], PRESENT_COLOR)
                    # COLOR UNUSED LETTERS GREY
                    else:
                        gw.set_square_color(WordleGWindow.get_current_row(gw), x, MISSING_COLOR)
                        # ADD MATCHING COLOR TO KEYBOARD
                        gw.set_key_color(inputWord[x], MISSING_COLOR)

                # SELECT NEXT ROWS
                WordleGWindow.set_current_row(gw,WordleGWindow.get_current_row(gw) + 1)
        else:
            if inputWord == "     ":
                gw.show_message("Enter a word")
            else:
                gw.show_message("Not in word list")
                # CLEAR THE ROW REMAIN IN THE SAME ROW
                for x in range(0, N_COLS):
                    WordleGWindow.set_square_letter(gw, WordleGWindow.get_current_row(gw), x, "")
                WordleGWindow.set_current_row(gw, WordleGWindow.get_current_row(gw))


    gw = WordleGWindow()

    

    #LOOP THROUGH AND PLACE LETTERS FROM WORD INTO FIRST ROW OF WORDLE
    colLoop = N_COLS
    rowLoop = N_ROWS
    # for x in word:
    #     WordleGWindow.set_square_letter(gw, N_ROWS - rowLoop, N_COLS - colLoop, x)
    #     colLoop = colLoop - 1

    gw.add_enter_listener(enter_action)

# Startup code

if __name__ == "__main__":
    wordle()
