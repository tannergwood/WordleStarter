# File: Wordle.py

"""
SPENCER JACKLIN, WESTON EVANS, NATHAN JOHNSON, TANNER GREENWOOD
"""


import random
from WordleDictionary import FIVE_LETTER_WORDS, FIVE_LETTER_WORDS_ESP
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS, CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR, UNKNOWN_COLOR, KEY_COLOR, selected_language, selected_color_scheme

# MAKE THE GAME END ONCE THERE ARE SIX GUESSES
def wordle():

    # SET LANGUAGE PREFERENCES AND SELECT WORD TO GUESS
    if selected_language == "English":
        wordList = FIVE_LETTER_WORDS
        word = random.choice(wordList).upper()
        notinwordlist = "Not in word list"
        enteraword = "Enter a word"
        youwon = "Congrats! You guessed the word!"
        youlost = "Sorry, You Lost! The word was: "
    else :
        wordList = FIVE_LETTER_WORDS_ESP
        word = random.choice(wordList).upper()
        notinwordlist = "No en la lista de palabras"
        enteraword = "Poner una palabra"
        youwon = "¡Felicitaciones! Adivinaste la palabra!"
        youlost = "¡Perdón que perdiste! La palabra era: "

    # CHANGE MESSAGE COLOR BASED ON COLOR SCHEME
    if (selected_color_scheme == "Dark Scheme"):
        msgColor = "White"
    else:
        msgColor = "Black"

    # ALLOW FOR KEYBOARD TO TURN OFF AFTER WINNING/LOSING TO ENSURE NO MORE GUESSING
    def keyboard_enabler(WordleGWindow, condition):
        WordleGWindow.enabled = condition

    

    def enter_action(s):

        # RETRIEVE WORD FROM WORDLE
        inputWord = ""
        for x in range(0, N_COLS):
            letter = WordleGWindow.get_square_letter(gw, WordleGWindow.get_current_row(gw), x)
            inputWord = inputWord + letter

        # LIST TO KEEP TRACK OF DOUBLE LETTERS BEING USED UP
        doubleLetterList = []
        for letter in word :
            doubleLetterList += letter

        #MILESTONE 2 MAKE SURE THE WORD IS AN ENGLISH/SPANISH WORD
        if (inputWord.lower() in wordList):

            # TEST IF THE WORD IS CORRECT
            if (inputWord == word):
                #COLOR ALL LETTERS GREEN
                for x in range(0, N_COLS):
                    gw.set_square_color(WordleGWindow.get_current_row(gw), x, CORRECT_COLOR)
                    # UPDATE THE KEYBOARD COLORS
                    for letter in inputWord :
                        gw.set_key_color(letter, CORRECT_COLOR)
                gw.show_message(youwon, msgColor)
                keyboard_enabler(gw, False)
            else:
                # COLOR THE LETTERS
                for x in range(0, N_COLS):
                    # SET LETTERS IN THE CORRECT POSITION TO GREEN
                    if ((inputWord[x] == word[x]) & (inputWord[x] in doubleLetterList)):
                        gw.set_square_color(WordleGWindow.get_current_row(gw), x, CORRECT_COLOR)
                        # ADD MATCHING COLOR TO KEYBOARD
                        gw.set_key_color(inputWord[x], CORRECT_COLOR)
                        # REMOVE USED LETTER FROM THE DOUBLE LETTER LIST
                        doubleLetterList[x] = "?"
                # COLOR PRESENT LETTERS IN WRONG POSITION YELLOW
                for x in range(0, N_COLS):
                    if((inputWord[x] in word) & (inputWord[x] in doubleLetterList) & (inputWord[x] != word[x])):
                        gw.set_square_color(WordleGWindow.get_current_row(gw), x, PRESENT_COLOR)
                        # ADD MATCHING COLOR TO KEYBOARD
                        gw.set_key_color(inputWord[x], PRESENT_COLOR)
                        # REMOVE USED LETTER FROM THE DOUBLE LETTER LIST
                        letterIndex = doubleLetterList.index(inputWord[x])
                        doubleLetterList[letterIndex] = "?"
                # COLOR UNUSED LETTERS GREY
                for x in range(0, N_COLS):
                    if ((gw.get_square_color(WordleGWindow.get_current_row(gw), x) != CORRECT_COLOR) & (gw.get_square_color(WordleGWindow.get_current_row(gw), x) != PRESENT_COLOR)):
                        gw.set_square_color(WordleGWindow.get_current_row(gw), x, MISSING_COLOR)
                        # ADD MATCHING COLOR TO KEYBOARD
                        gw.set_key_color(inputWord[x], MISSING_COLOR)


                # IF 6TH ROW, END THE GAME, DISABLE KEYBOARD
                if WordleGWindow.get_current_row(gw) == 5:
                    lossMessage = youlost + word
                    gw.show_message(lossMessage, msgColor)
                    keyboard_enabler(gw, False)
                else:
                    # SELECT NEXT ROWS
                    WordleGWindow.set_current_row(gw,WordleGWindow.get_current_row(gw) + 1)
        else:
            # MAKE SURE THERE ARE NO BLANK WORDS ENTERED
            if inputWord == "     ":
                gw.show_message(enteraword, msgColor)
            else:
                gw.show_message(notinwordlist, msgColor)
                # REMAIN IN THE SAME ROW


    gw = WordleGWindow()

    
    #### MILESTONE 1 #######
    #LOOP THROUGH AND PLACE LETTERS FROM WORD INTO FIRST ROW OF WORDLE
    # colLoop = N_COLS
    # rowLoop = N_ROWS
    # for x in word:
    #     WordleGWindow.set_square_letter(gw, N_ROWS - rowLoop, N_COLS - colLoop, x)
    #     colLoop = colLoop - 1

    gw.add_enter_listener(enter_action)

# Startup code

if __name__ == "__main__":
    wordle()
