import tkinter
import random
from collections import deque

ROWS = 18
COLS = 30
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

# FlashCard class contains a word and a definition
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

# load the words and definitions into the different word lists from the .txt file
def load_words_and_defs():
    try:
        with open('flashcard_list.txt', 'r') as file:
            known = False
            needs_more_work = False
            for line in file: # split the words up into the respective categories of knowledge level
                #print(line)
                if line == "\n":
                    continue
                if line == "Not Known:\n":
                    known = False
                    needs_more_work = False
                    continue
                elif line == "Known:\n":
                    known = True
                    needs_more_work = False
                    continue
                elif line == "Needs More Work:\n":
                    needs_more_work = True
                    known = False
                    continue

                if known == True:
                    split_word = line.split(":")
                    flashcard = FlashCard(split_word[0].strip(), split_word[1].strip())
                    known_list.append(flashcard)
                elif needs_more_work == True:
                    split_word = line.split(":")
                    flashcard = FlashCard(split_word[0].strip(), split_word[1].strip())
                    needs_more_work_list.append(flashcard)
                else: # if there is no label for where the word should go just put in the not known list
                    split_word = line.split(":")
                    flashcard = FlashCard(split_word[0].strip(), split_word[1].strip())
                    not_known_list.append(flashcard)

    except FileNotFoundError:
        print("The file was not found.")
    except IOError:
        print("An error occurred while reading the file.")

# flip the flashcard to the side that displays the defintion
def to_definition():
    global canvas_text

    if curr_card == None:
        return

    canvas.itemconfig(tagOrId=canvas_text, text=insert_newlines(curr_card.get_definition()))

# used for displaying the definition on the screen in a way that doesn't cut any part off of the screen
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

# flip the flashcard to the side that displays the word
def to_word():
    global canvas_text

    if curr_card == None:
        return
    
    canvas.itemconfig(tagOrId=canvas_text, text=curr_card.get_word())

# display a different word
def new_word():
    global curr_card, curr_list

    if curr_card == None:
        return

    curr_list.append(curr_card) # return the flashcard to the end of the list
    curr_card = curr_list.popleft() # select a new card to study

    canvas.itemconfig(tagOrId=canvas_text, text=curr_card.get_word()) # display the new word

# display a definition for a different word
def new_definition():
    global curr_card, curr_list

    if curr_card == None:
        return

    curr_list.append(curr_card) # return the flashcard to the end of the list
    curr_card = curr_list.popleft() # select a new card to study

    canvas.itemconfig(tagOrId=canvas_text, text=to_definition()) # display the new definition

# switch to the not known word list
def switch_list_not_known():
    global curr_list, not_known_bool, known_bool, needs_more_work_bool, curr_card

    if not_known_bool:
        return
    else:
        if curr_card != None:
            curr_list.append(curr_card)
        curr_list = not_known_list
        known_bool = False
        needs_more_work_bool = False
        not_known_bool = True

        if isEmpty(curr_list):
            curr_card = None
            canvas.itemconfig(tagOrId=canvas_text, text="Current List Is Empty Select a New One") # display that the list is empty
            return
        curr_card = curr_list.popleft() # select a new card to study from the new list
        canvas.itemconfig(tagOrId=canvas_text, text=curr_card.get_word()) # display the new word

# switch to the known word list
def switch_list_known():
    global curr_list, not_known_bool, known_bool, needs_more_work_bool, curr_card

    if known_bool:
        return
    else:
        if curr_card != None:
            curr_list.append(curr_card)
        curr_list = known_list
        known_bool = True
        needs_more_work_bool = False
        not_known_bool = False

        if isEmpty(curr_list):
            curr_card = None
            canvas.itemconfig(tagOrId=canvas_text, text="Current List Is Empty Select a New One") # display that the list is empty
            return
        curr_card = curr_list.popleft() # select a new card to study from the new list
        canvas.itemconfig(tagOrId=canvas_text, text=curr_card.get_word()) # display the new word

# switch to the needs more work word list
def switch_list_needs_more_work():
    global curr_list, not_known_bool, known_bool, needs_more_work_bool, curr_card

    if needs_more_work_bool:
        return
    else:
        if curr_card != None:
            curr_list.append(curr_card)
        curr_list = needs_more_work_list
        known_bool = False
        needs_more_work_bool = True
        not_known_bool = False

        if isEmpty(curr_list):
            curr_card = None
            canvas.itemconfig(tagOrId=canvas_text, text="Current List Is Empty Select a New One") # display that the list is empty
            return
        curr_card = curr_list.popleft() # select a new card to study from the new list
        canvas.itemconfig(tagOrId=canvas_text, text=curr_card.get_word()) # display the new word

# check if a list is empty
def isEmpty(lst):
    return len(lst) == 0

# shuffles every word list
def shuffle_lists():
    if curr_card == None:
        canvas.itemconfig(tagOrId=canvas_text, text="Cannot Shuffle Empty List")
    random.shuffle(curr_list)
    random.shuffle(not_known_list)
    random.shuffle(known_list)
    random.shuffle(needs_more_work_list)
    new_word()

# save the flashcard data to a .txt file to save progress
def save_data(filename):
    global curr_list

    curr_list.append(curr_card) # add the displayed card back to the list before saving and closing the program

    try:
        with open(filename, 'w') as file:
            file.write("Not Known: \n")
            for card in not_known_list:
                file.write(f"{card.get_word()} : {card.get_definition()}\n")
            file.write("\n")
            
            file.write("Needs More Work: \n")
            for card in known_list:
                file.write(f"{card.get_word()} : {card.get_definition()}\n")
            file.write("\n")
            
            file.write("Known: \n")
            for card in needs_more_work_list:
                file.write(f"{card.get_word()} : {card.get_definition()}\n")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

# what to do when the window closes
def on_close():
    save_data('flashcard_list.txt')
    window.destroy()

# adds the current card to the not known flashcard list and then displays the next card in the current list
def add_not_known():
    global not_known_list, curr_card

    if curr_card == None:
        return

    not_known_list.append(curr_card)
    
    if not isEmpty(curr_list):
        curr_card = curr_list.popleft() # select a new card to study
        canvas.itemconfig(tagOrId=canvas_text, text=curr_card.get_word()) # display the new word
    else:
        curr_card = None
        canvas.itemconfig(tagOrId=canvas_text, text="Current List Is Empty Select a New One") # display that the list is empty

# adds the current card to the known flashcard list and then displays the next card in the current list
def add_known():
    global known_list, curr_card

    if curr_card == None:
        return

    known_list.append(curr_card)
    
    if not isEmpty(curr_list):
        curr_card = curr_list.popleft() # select a new card to study
        canvas.itemconfig(tagOrId=canvas_text, text=curr_card.get_word()) # display the new word
    else:
        curr_card = None
        canvas.itemconfig(tagOrId=canvas_text, text="Current List Is Empty Select a New One") # display that the list is empty

# adds the current card to the needs more work flashcard list and then displays the next card in the current list
def add_needs_more_work():
    global needs_more_work_list, curr_card

    if curr_card == None:
        return

    needs_more_work_list.append(curr_card)
    
    if not isEmpty(curr_list):
        curr_card = curr_list.popleft() # select a new card to study
        canvas.itemconfig(tagOrId=canvas_text, text=curr_card.get_word()) # display the new word
    else:
        curr_card = None
        canvas.itemconfig(tagOrId=canvas_text, text="Current List Is Empty Select a New One") # display that the list is empty
    

# initialize flashcards
not_known_list = deque()
known_list = deque()
needs_more_work_list = deque()

load_words_and_defs()

# shuffle all the lists
random.shuffle(not_known_list)
random.shuffle(known_list)
random.shuffle(needs_more_work_list)

curr_list = not_known_list
curr_card = curr_list.popleft()

# keep track of which list is being studied
not_known_bool = True
known_bool = False
needs_more_work_bool = False


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

new_definition_button = tkinter.Button(frame_right, text="New Definition", font=("Consolas"), background="blue",
                        foreground="white", command=new_definition)
new_definition_button.grid(row=4, column=0, columnspan=3, sticky="nswe")

# create buttons to change which word list is being studied
not_known_button = tkinter.Button(frame_right, text="Not Known Words", font=("Consolas"), background="green",
                        foreground="white", command=switch_list_not_known)
not_known_button.grid(row=5, column=0, columnspan=3, sticky="nswe")

known_button = tkinter.Button(frame_right, text="Known Words", font=("Consolas"), background="green",
                        foreground="white", command=switch_list_known)
known_button.grid(row=7, column=0, columnspan=3, sticky="nswe")

needs_more_work_button = tkinter.Button(frame_right, text="More Work Words", font=("Consolas"), background="green",
                        foreground="white", command=switch_list_needs_more_work)
needs_more_work_button.grid(row=6, column=0, columnspan=3, sticky="nswe")

# create a button to shuffle all the lists
shuffle_button = tkinter.Button(frame_right, text="Shuffle Words", font=("Consolas"), background="purple",
                        foreground="white", command=shuffle_lists)
shuffle_button.grid(row=8, column=0, columnspan=3, sticky="nswe")

# create buttons to add flashcards to different knowledge level lists
add_not_known_button = tkinter.Button(frame_right, text="Add Not Known", font=("Consolas"), background="black",
                        foreground="white", command=add_not_known)
add_not_known_button.grid(row=9, column=0, columnspan=3, sticky="nswe")

add_needs_more_work_button = tkinter.Button(frame_right, text="Add Needs More", font=("Consolas"), background="black",
                        foreground="white", command=add_needs_more_work)
add_needs_more_work_button.grid(row=10, column=0, columnspan=3, sticky="nswe")

add_known_button = tkinter.Button(frame_right, text="Add Known", font=("Consolas"), background="black",
                        foreground="white", command=add_known)
add_known_button.grid(row=11, column=0, columnspan=3, sticky="nswe")

# Bind the window close event --> when the window closes the flashcards will be saved to a .txt file
window.protocol("WM_DELETE_WINDOW", on_close)

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