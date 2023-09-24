# File: WordleGraphics.py

"""
This file implements the WordleGWindow class, which manages the
graphical display for the Wordle project.

SPENCER JACKLIN, WESTON EVANS, NATHAN JOHNSON, TANNER GREENWOOD

"""

import atexit
import time
import tkinter as tk

# Constants

N_ROWS = 6			# Number of rows
N_COLS = 5			# Number of columns

CORRECT_COLOR = "#66BB66"       # Light green for correct letters
PRESENT_COLOR = "#CCBB66"       # Brownish yellow for misplaced letters
MISSING_COLOR = "#999999"       # Gray for letters that don't appear
UNKNOWN_COLOR = "#FFFFFF"       # Undetermined letters are white
KEY_COLOR = "#DDDDDD"           # Keys are colored light gray

# Function to save the language and color scheme choices to variables and close the window
def save_choices_and_close():
    global selected_language
    global selected_color_scheme

    selected_language = language_var.get()
    selected_color_scheme = color_scheme_var.get()

    if selected_language and selected_color_scheme:
        root.destroy()  # Close the tkinter window
    else:
        error_label.config(text="Please select both language and color scheme.")


# Create the main tkinter window
root = tk.Tk()
root.title("Language and Color Scheme Selection")
root.geometry("400x500")

# Create variables to store the selected language and color scheme
selected_language = None
selected_color_scheme = None

# Create a label to display the selected language and color scheme
language_label = tk.Label(root, text="", font=("Arial", 12))
language_label.pack(pady=10)

color_scheme_label = tk.Label(root, text="", font=("Arial", 12))
color_scheme_label.pack(pady=10)

# Create radio buttons for language selection
language_frame = tk.Frame(root)
language_frame.pack(pady=10)

language_label = tk.Label(language_frame, text="Select Language:")
language_label.pack()

language_var = tk.StringVar()

english_radio = tk.Radiobutton(language_frame, text="English", variable=language_var, value="English")
english_radio.pack()

spanish_radio = tk.Radiobutton(language_frame, text="Spanish", variable=language_var, value="Spanish")
spanish_radio.pack()

# Create radio buttons for color scheme selection
color_scheme_frame = tk.Frame(root)
color_scheme_frame.pack(pady=10)

color_scheme_label = tk.Label(color_scheme_frame, text="Select Color Scheme:")
color_scheme_label.pack()

color_scheme_var = tk.StringVar()

original_radio = tk.Radiobutton(color_scheme_frame, text="Original", variable=color_scheme_var, value="Original")
original_radio.pack()

dark_scheme_radio = tk.Radiobutton(color_scheme_frame, text="Dark Scheme", variable=color_scheme_var, value="Dark Scheme")
dark_scheme_radio.pack()

# Create an error label to display validation errors
error_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
error_label.pack(pady=10)

# Create a button to save choices and close the window
save_button = tk.Button(root, text="Save Choices", command=save_choices_and_close)
save_button.pack(pady=20)

# Start the tkinter main loop
root.mainloop()



# SET COLOR MODE
if (selected_color_scheme == "Original"):
    CORRECT_COLOR = "#66BB66"       # Light green for correct letters
    PRESENT_COLOR = "#CCBB66"       # Brownish yellow for misplaced letters
    MISSING_COLOR = "#999999"       # Gray for letters that don't appear
    UNKNOWN_COLOR = "#FFFFFF"       # Undetermined letters are white
    KEY_COLOR = "#DDDDDD"           # Keys are colored light gray
    BG_COLOR = "White"              # Window background is white

if (selected_color_scheme == "Dark Scheme"):
    CORRECT_COLOR = "#B0E0E6"       # Light blue for correct letters
    PRESENT_COLOR = "#FBA100"       # Orange for misplaced letters
    MISSING_COLOR = "#757575"       # Gray for letters that don't appear
    UNKNOWN_COLOR = "#505050"       # Undetermined letters are gray
    KEY_COLOR = "Dark Grey"         # Keys are colored light gray
    BG_COLOR = "#505050"            # Window background is gray


CANVAS_WIDTH = 700		# Width of the tkinter canvas (pixels)
CANVAS_HEIGHT = 700		# Height of the tkinter canvas (pixels)

SQUARE_SIZE = 60		# Size of each square (pixels)
SQUARE_SEP = 5                  # Separation between squares (pixels)
TOP_MARGIN = 30    		# Top margin (pixels)
BOTTOM_MARGIN = 30    		# Bottom margin (pixels)
MESSAGE_SEP = 20                # Space between board and message center

SQUARE_FONT = ("Helvetica Neue", -44, "bold")
MESSAGE_FONT = ("Helvetica Neue", -20, "bold")
KEY_FONT = ("Helvetica Neue", -18)
ENTER_FONT = ("Helvetica Neue", -14)

KEY_WIDTH = 40
KEY_HEIGHT = 60
KEY_CORNER = 9
KEY_XSEP = 5
KEY_YSEP = 7

KEY_LABELS = [
    [ "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P" ],
    [ "A", "S", "D", "F", "G", "H", "J", "K", "L" ],
    [ "ENTER", "Z", "X", "C", "V", "B", "N", "M", "DELETE" ]
]

KEY_LABELS_ESP = [
    [ "Q", "W", "E", "R", "T", "U", "É", "I", "Í", "O", "Ó", "P" ],
    [ "A", "Á", "S", "D", "F", "G", "H", "J", "K", "L", "Ñ" ],
    [ "ENT", "Z", "X", "C", "Ç", "V", "B", "N", "M", "Ú",  "DEL"]
]

CLICK_MAX_DISTANCE = 2
CLICK_MAX_DELAY = 0.5

# Derived constants

SQUARE_DELTA = SQUARE_SIZE + SQUARE_SEP
BOARD_WIDTH = N_COLS * SQUARE_SIZE + (N_COLS - 1) * SQUARE_SEP
BOARD_HEIGHT = N_ROWS * SQUARE_SIZE + (N_ROWS - 1) * SQUARE_SEP
MESSAGE_X = CANVAS_WIDTH / 2
MESSAGE_Y = TOP_MARGIN + BOARD_HEIGHT + MESSAGE_SEP

class WordleGWindow:
    """This class creates the Wordle window."""
    enabled = True

    def __init__(self):
        """Creates the Wordle window."""

        def create_grid():
            return [
                [
                    WordleSquare(canvas, i, j) for j in range(N_COLS)
                ] for i in range(N_ROWS)
            ]
        
        
        def create_keyboard():
            # IF ENGLISH USE ENGLISH KEYBOARD, OTHERWISE USE SPANISH
            if selected_language == "English":
                keys = { }
                nk = len(KEY_LABELS[0])
                h = KEY_HEIGHT
                y0 = CANVAS_HEIGHT - BOTTOM_MARGIN - 3 * KEY_HEIGHT - 2 * KEY_YSEP
                for row in range(len(KEY_LABELS)):
                    y = y0 + row * (KEY_HEIGHT + KEY_YSEP)
                    x = (CANVAS_WIDTH - nk * KEY_WIDTH - (nk - 1) * KEY_XSEP) / 2
                    if row == 1:
                        x += (KEY_WIDTH + KEY_XSEP) / 2
                    for col in range(len(KEY_LABELS[row])):
                        label = KEY_LABELS[row][col]
                        w = KEY_WIDTH
                        if len(label) > 1:
                            w += (KEY_WIDTH + KEY_XSEP) / 2
                        keys[label] = WordleKey(self._canvas, x, y, w, h, label)
                        x += w + KEY_XSEP
                return keys
            else :
                keys = { }
                nk = len(KEY_LABELS_ESP[0])
                h = KEY_HEIGHT
                y0 = CANVAS_HEIGHT - BOTTOM_MARGIN - 3 * KEY_HEIGHT - 2 * KEY_YSEP
                for row in range(len(KEY_LABELS_ESP)):
                    y = y0 + row * (KEY_HEIGHT + KEY_YSEP)
                    x = (CANVAS_WIDTH - nk * KEY_WIDTH - (nk - 1) * KEY_XSEP) / 2
                    if row == 1:
                        x += (KEY_WIDTH + KEY_XSEP) / 2
                    for col in range(len(KEY_LABELS_ESP[row])):
                        label = KEY_LABELS_ESP[row][col]
                        w = KEY_WIDTH
                        if len(label) > 1:
                            w += (KEY_WIDTH + KEY_XSEP) / 2
                        keys[label] = WordleKey(self._canvas, x, y, w, h, label)
                        x += w + KEY_XSEP
                return keys

        def create_message():
            return WordleMessage(self._canvas,
                                 CANVAS_WIDTH / 2,
                                 MESSAGE_Y)

        def key_action(tke):
            #MAKE SURE THE KEYBOARD IS ENABLED, IF ITS NOT ENABLED, KEYS WONT WORK
            if not self.enabled:
                return
            else:
                if isinstance(tke, str):
                    ch = tke.upper()
                else:
                    ch = tke.char.upper()
                if ch == "\007" or ch == "\177" or ch == "DELETE" or ch == "DEL":
                    self.show_message("")
                    if self._row < N_ROWS and self._col > 0:
                        self._col -= 1
                        sq = self._grid[self._row][self._col]
                        sq.set_letter(" ")
                elif ch == "\r" or ch == "\n" or ch == "ENTER" or ch == "ENT":
                    self.show_message("")
                    s = ""
                    for col in range(N_COLS):
                        s += self._grid[self._row][col].get_letter();
                    for fn in self._enter_listeners:
                        fn(s)
                elif ch.isalpha():
                    self.show_message("")
                    if self._row < N_ROWS and self._col < N_COLS:
                        sq = self._grid[self._row][self._col]
                        sq.set_letter(ch)
                        self._col += 1

        def press_action(tke):
            self._down_x = tke.x
            self._down_y = tke.y
            self._down_time = time.time()

        def release_action(tke):
            if abs(self._down_x - tke.x) <= CLICK_MAX_DISTANCE:
                if abs(self._down_y - tke.y) <= CLICK_MAX_DISTANCE:
                    t = time.time()
                    if t - self._down_time < CLICK_MAX_DELAY:
                        key = find_key(tke.x, tke.y)
                        if key:
                            key_action(key._label)

        def find_key(x, y):
            for key in self._keys.values():
                kx, ky, kw, kh = key._bounds
                if x >= kx and x <= kx + kw and y >= ky and y <= ky + kh:
                    return key
            return None

        def delete_window():
            """Closes the window and exits from the event loop."""
            root.destroy()

        def start_event_loop():
            """Starts the tkinter event loop when the program exits."""
            root.mainloop()

        root = tk.Tk()
        root.title("Wordle")
        root.protocol("WM_DELETE_WINDOW", delete_window)
        self._root = root
        canvas = tk.Canvas(root,
                                bg=BG_COLOR,
                                width=CANVAS_WIDTH,
                                height=CANVAS_HEIGHT,
                                highlightthickness=0)
        canvas.pack()
        self._canvas = canvas
        self._grid = create_grid()
        self._message = create_message()
        self._keys = create_keyboard()
        self._enter_listeners = [ ]
        root.bind("<Key>", key_action)
        root.bind("<ButtonPress-1>", press_action)
        root.bind("<ButtonRelease-1>", release_action)
        self._row = 0
        self._col = 0
        atexit.register(start_event_loop)

    def get_square_letter(self, row, col):
        return self._grid[row][col].get_letter()

    def set_square_letter(self, row, col, ch):
        self._grid[row][col].set_letter(ch)

    def get_square_color(self, row, col):
        return self._grid[row][col].get_color()

    def set_square_color(self, row, col, color):
        self._grid[row][col].set_color(color)

    def get_key_color(self, ch):
        return self._keys[ch].get_color()

    def set_key_color(self, ch, color):
        self._keys[ch].set_color(color)

    def get_current_row(self):
        return self._row

    def set_current_row(self, row):
        self._row = row
        self._col = 0
        for col in range(N_COLS):
            self.set_square_letter(row, col, " ")
            self.set_square_color(row, col, UNKNOWN_COLOR)

    def add_enter_listener(self, fn):
        self._enter_listeners.append(fn)

    def show_message(self, msg, color="Black"):
        self._message.set_text(msg, color)


class WordleSquare:

    def __init__(self, canvas, row, col):
        x0 = (CANVAS_WIDTH - BOARD_WIDTH) / 2 + col * SQUARE_DELTA
        y0 = TOP_MARGIN + row * SQUARE_DELTA
        x1 = x0 + SQUARE_SIZE
        y1 = y0 + SQUARE_SIZE
        self._canvas = canvas
        self._ch = " "
        self._color = UNKNOWN_COLOR;
        self._frame = canvas.create_rectangle(x0, y0, x1, y1)
        self._text = canvas.create_text(x0 + SQUARE_SIZE / 2,
                                        y0 + SQUARE_SIZE / 2,
                                        text=self._ch,
                                        font=SQUARE_FONT)

    def get_letter(self):
        return self._ch

    def set_letter(self, ch):
        self._ch = ch
        self._canvas.itemconfigure(self._text, text=ch)

    def get_color(self):
        return self._color

    def set_color(self, color):
        color = color.upper()
        self._color = color
        fg = "White"
        if color == UNKNOWN_COLOR:
            fg = "Black"
        self._canvas.itemconfig(self._frame, fill=color)
        self._canvas.itemconfig(self._text, fill=fg)


class WordleKey:

    def __init__(self, canvas, x, y, width, height, label):
        self._canvas = canvas
        self._label = label
        self._bounds = [ x, y, width, height ]
        self._color = UNKNOWN_COLOR
        font = KEY_FONT
        if label == "ENTER":
            font = ENTER_FONT
        if label == "DELETE":
            label = "\u232B"
        points = [ x + KEY_CORNER, y,
                   x + KEY_CORNER, y,
                   x + width - KEY_CORNER, y,
                   x + width - KEY_CORNER, y,
                   x + width, y,
                   x + width, y + KEY_CORNER,
                   x + width, y + KEY_CORNER,
                   x + width, y + height - KEY_CORNER,
                   x + width, y + height - KEY_CORNER,
                   x + width, y + height,
                   x + width - KEY_CORNER, y + height,
                   x + width - KEY_CORNER, y + height,
                   x + KEY_CORNER, y + height,
                   x + KEY_CORNER, y + height,
                   x, y + height,
                   x, y + height - KEY_CORNER,
                   x, y + height - KEY_CORNER,
                   x, y + KEY_CORNER,
                   x, y + KEY_CORNER,
                   x, y]
        self._frame = canvas.create_polygon(points,
                                            fill=KEY_COLOR,
                                            outline=KEY_COLOR,
                                            smooth=True)
        self._text = canvas.create_text(x + width / 2,
                                        y + height / 2,
                                        text=label,
                                        font=font)

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color
        fg = "White"
        if color == UNKNOWN_COLOR:
            fg = "Black"
        self._canvas.itemconfig(self._frame, fill=color)
        self._canvas.itemconfig(self._text, fill=fg)


class WordleMessage:

    def __init__(self, canvas, x, y):
        self._canvas = canvas
        self._text = ""
        self._msg = canvas.create_text(x, y,
                                       text="",
                                       font=MESSAGE_FONT,
                                       anchor=tk.CENTER)

    def get_text(self):
        return self._text

    def set_text(self, text, color="Black"):
        self._text = text
        self._canvas.itemconfigure(self._msg, text=text, fill=color)
