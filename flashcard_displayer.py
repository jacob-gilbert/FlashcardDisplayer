import tkinter
import random
from collections import deque

ROWS = 18
COLS = 30
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class FlashCard:
    def __init__(self, word, definition):
        self.word = word
        self.definition = definition

    def get_word(self):
        return self.word
        
    def get_definition(self):
        return self.definition
    
    def print_card(self):
        return f"{self.word} - {self.definition}"

def load_words_and_defs():
    try:
        with open('flashcard_list.txt', 'r') as file:
            for line in file:
                split_word = line.split(":")
                flashcard = FlashCard(split_word[0].strip(), split_word[1].strip())
                flashcard_list.append(flashcard)
    except FileNotFoundError:
        print("The file was not found.")
    except IOError:
        print("An error occurred while reading the file.")

def to_definition():
    global canvas_text

    canvas.itemconfig(tagOrId=canvas_text, text=insert_newlines(curr_card.get_definition()))

def insert_newlines(paragraph, words_per_line=5):
    # Split the paragraph into a list of words
    words = paragraph.split()
    
    # Initialize an empty list to hold the new lines
    new_lines = []
    
    # Iterate over the words and add new lines after every `words_per_line` words
    for i in range(0, len(words), words_per_line):
        # Join the current slice of words and add it to the new_lines list
        new_lines.append(' '.join(words[i:i + words_per_line]))
    
    # Join all the lines with newline characters
    return '\n'.join(new_lines)

def to_word():
    global canvas_text
    canvas.itemconfig(tagOrId=canvas_text, text=curr_card.get_word())

def new_word():
    global curr_card, flashcard_list

    flashcard_list.append(curr_card) # return the flashcard to the end of the list
    curr_card = flashcard_list.popleft() # select a new card to study

    canvas.itemconfig(tagOrId=canvas_text, text=curr_card.get_word()) # display the new word

def new_definition():
    global curr_card, flashcard_list

    flashcard_list.append(curr_card) # return the flashcard to the end of the list
    curr_card = flashcard_list.popleft() # select a new card to study

    canvas.itemconfig(tagOrId=canvas_text, text=to_definition()) # display the new definition
    

# initialize flashcards
flashcard_list = deque()
load_words_and_defs()
random.shuffle(flashcard_list)
curr_card = flashcard_list.popleft()


# game window
window = tkinter.Tk()
window.title("Flashcard Displayer")
window.resizable(False, False) # user cannot change the size of the window

# create frame to hold the canvas where the word and definition will appear
frame_left = tkinter.Frame(window, bg='lightblue')
frame_left.grid(row=0, column=0, sticky='nsew')

canvas = tkinter.Canvas(frame_left, bg="white", width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                        borderwidth=0, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas_text = canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20",
                           text=curr_card.get_word(),
                           fill="black")

# create frame to place the buttons to change the word and definition
frame_right = tkinter.Frame(window, bg="lightgray")
frame_right.grid(row=0, column=1, sticky="nswe")

definition_button = tkinter.Button(frame_right, text="Definition", font=("Consolas"), background="red",
                        foreground="white", command=to_definition)
definition_button.grid(row=1, column=0, columnspan=3, sticky="nswe")

word_button = tkinter.Button(frame_right, text="Word", font=("Consolas"), background="red",
                        foreground="white", command=to_word)
word_button.grid(row=0, column=0, columnspan=3, sticky="nswe")

new_word_button = tkinter.Button(frame_right, text="New Word", font=("Consolas"), background="blue",
                        foreground="white", command=new_word)
new_word_button.grid(row=3, column=0, columnspan=3, sticky="nswe")

new_definition_button = tkinter.Button(frame_right, text="New Def", font=("Consolas"), background="blue",
                        foreground="white", command=new_definition)
new_definition_button.grid(row=4, column=0, columnspan=3, sticky="nswe")


window.update()


# center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight() - 75 # the -75 is specific to my screen

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

# format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")



window.mainloop()