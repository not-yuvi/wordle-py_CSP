# Gavin Schwinghammer and Yuvraj Arora
# Description: This program is the game Wordle made using python and the turtle library. Wordle is a game where you get 6 tries at guessing a word and the word is 5 letters long. After pressing enter after every attempt, the game compares your word and gives a indicator.
#              Green means right spot of the letter. Yellow means wrong stop but the letter is in the word. Grey means the letter is not in the word.
# Date: 3/29/2024
# Bugs: Bugs fixed after extensive testing/ No bugs found


# ---imports---
import turtle as trtl
import string
import random
import os
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import time

# ----INITIALIZING VARIABLES----
# Lists
intersection_coords = []
x_coords = []
y_coords = []
lines = {}
typing_list = []
typed_list = []
chosen_word_list = []


# Win/Lose
lose = False
win = False


# 0 = not in word, 1 = yellow, 2 = green
check = ['0', '0', '0', '0', '0']

typing_line = 0

on_click_light = None
y_turtles = []

check_running = False

# CONSTANTS

colors = {
    'background': 'black',
    'foreground': '#121213',
    'yellow': '#b59f3b',
    'green': '#538d4e',
    'not in word': '#3a3a3c',
    'blank' : '#3a3a3c',
}
# turtles
grid_drawer = trtl.Turtle()
misc_drawer = trtl.Turtle()
theme_turtle = trtl.Turtle()
error_turtle = trtl.Turtle()

wn = trtl.Screen()
wn.bgcolor(colors['background'])

# https://blog.almamunhossen.com/what-is-dark-mode-and-how-to-turn-it-on
dark_img = os.path.join('data', 'dark.gif')
wn.register_shape(dark_img)

light_img = os.path.join('data', 'light.gif')
wn.register_shape(light_img)
# end citation


# https://www.freeiconspng.com/thumbs/white-arrow-png/curved-white-arrow-png-0.png
arrow_image = os.path.join('data', 'arrow.gif')
wn.register_shape(arrow_image)
# complete citation

cursor = trtl.Turtle()

# Sooth EaseIn line indicator - Yuvraj
def MoveCursorToLine():
    cursor.setheading(270)
    next_cor = cursor.ycor() - 75
    distance_left = 75
    while abs(distance_left) > 0.1:
        distance = abs(next_cor - cursor.ycor())
        distance_left = distance * 0.1
        cursor.forward(distance_left)

# changes the tile colors depending on how the letters match up with the correct word - Yuvraj
def StampCheck(color, index):
    global tile
    tile._tracer(False)
    location = lines[typing_line][index]
    location = [location[0]+37.5, location[1]+37.5]
    tile.goto(location)
    if color == '2':
        tile.color(colors['green'])
    elif color == '1':
        tile.color(colors['yellow'])
    else:
        tile.color(colors['not in word'])
    tile.stamp()
    tile.hideturtle()
    UpdateLine()
    tile._tracer(True)

# checks if the letters entered by the user are in the word and in the correct place
# changes the tile colors accordingly - Gavin
def CheckLetters(compare):
    global typing_line, typed_list, check_running

    # Check if CheckLetters is already running
    if check_running:
        return 

    # Set the flag to indicate that CheckLetters is running
    check_running = True
    try:
        if len(typing_list) == 5:
            if not CheckIfWord(''.join(typing_list)):
                return
            win_check = 0
            typed_list = typing_list.copy()
            chosen_word_list_copy = chosen_word_list.copy()

            used_indices = set()
            # checks if letter is in the correct place in the word
            for i in range(len(typed_list)):
                letter = typed_list[i]
                if letter == chosen_word_list_copy[i]:
                    check[i] = "2" 
                    StampCheck('2', i)
                    chosen_word_list_copy[i] = None
                    used_indices.add(i)
                    win_check += 1
            # checks if the letter is in the word and makes changes accordingly
            for i in range(len(typed_list)):
                letter = typed_list[i]
                if letter in chosen_word_list_copy and i not in used_indices:
                    check[i] = "1"
                    StampCheck('1', i)
                    used_indices.add(i)
                    chosen_word_list_copy[chosen_word_list_copy.index(letter)] = None
            # checks if letter is not in the word and makes changes accordingly
            for i in range(len(typed_list)):
                if check[i] == "0":
                    StampCheck('0', i)
            if compare:
                # checks if the user has won or lost
                if win_check == 5:
                    WinOrLose(True)
                elif typing_line == 5:
                    WinOrLose(False)
                else:
                    typing_line += 1
                    typing_list.clear()
                    MoveCursorToLine()
    finally:
        check_running = False

def Display_Error(error):
    error_turtle.hideturtle()
    error_turtle.clear()
    error_turtle.penup()
    error_turtle.color('#eb7575') # light red
    error_turtle.goto(0, (wn.window_height()/2) - 35)
    error_turtle.write(error, align="center", font=("Arial", 15, "normal"))

# uses Dictionary API to check if the word entered by the user is a real word - Yuvraj
def CheckIfWord(word):
    try:
        url = (f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        httprequest = Request(url, headers={"Accept": "application/json"})
        with urlopen(httprequest) as response:
            if response.status == 200:
                return True
            elif response.status == 404:
                Display_Error("API is down, using fallback list...")
    except HTTPError as e:
        word_list_file = open("word_list.txt", "r")
        word_list = word_list_file.readlines()
        if word.title() + "\n" in word_list:
            return True
        else:
            Display_Error("That's not a Word!")
            return False
# complete citation

# updates the line as the user enters in their guess - Yuvraj
def UpdateLine():
    global typing_line
    if typing_line <= 5:
        y_turtles[typing_line]._tracer(False)
        y_turtles[typing_line].clear()
        y_turtles[typing_line].write(' '.join(typing_list), align="left",font=("Consolas", 52, "bold"))
        y_turtles[typing_line]._tracer(True)
    else:
        typing_line = 5

# ----keypress handle functions----
# Append Val - adds typed letter to the grid for the user to see - Yuvraj
# Sub Val - removes last letter when the user hits the backspace key - Gavin
def AppendVal(letter):
    if len(typing_list) != 5:
        typing_list.append(letter.upper())
        UpdateLine()
def SubVal():
    if len(typing_list) != 0:
        typing_list.pop()
        UpdateLine()
        error_turtle.clear()

# sets up the ui before starting the game - (grid - Gavin) , (tiles - Yuvraj)
def SetUp():
    global intersection_coords, tile
    
    grid_drawer._tracer(True)
    
    start_x_pos = -190
    start_y_pos = -225

    grid_drawer.hideturtle()
    grid_drawer.color(colors['foreground'])
    grid_drawer.speed(10)
    grid_drawer.pensize(6)
    for count in range(7):
        grid_drawer.penup()
        grid_drawer.goto(start_x_pos, start_y_pos + (count * 75))
        grid_drawer.pendown()
        grid_drawer.forward(375)
        
    for count in range(6):
        grid_drawer.left(90)
        grid_drawer.penup()
        grid_drawer.goto(start_x_pos + (count * 75), start_y_pos)
        grid_drawer.pendown()
        grid_drawer.forward(450)
        grid_drawer.right(90)
    
    
    tile = trtl.Turtle()
    tile.speed(10)
    tile.shape('square')
    tile.color(colors['not in word'])
    tile.shapesize(3.5)
    tile.penup()
    for coords in intersection_coords:
        tile.goto(coords[0]+37.5, coords[1]+37.5)
        tile.stamp()
    tile.hideturtle()
    
    cursor.penup()
    cursor.goto(x_coords[0] - 75, lines[typing_line][0][1] + 37.5)
    cursor.shape(arrow_image)

    for y in y_coords:
    # Copilot(AI)[prompt: how to make 5 new turtles variables and add them to a list?]
        new_turtle = trtl.Turtle()
        new_turtle._tracer(False)
        new_turtle.penup()
        new_turtle.color('white')
        new_turtle.goto(x_coords[0] + 20, y)
        new_turtle.write(' ', align="left",font=("Consolas", 52, "bold"))
        y_turtles.append(new_turtle)
        new_turtle._tracer(True)
    for turtle in y_turtles:
        turtle.hideturtle()
    # complete citation
    theme_turtle.penup()
    ToggleThemeBtn(dark=True)

def ToggleThemeBtn(dark):
    global on_click_light
    theme_turtle.goto(wn.window_width()/2 - 75, wn.window_height()/2 - 75)
    theme_turtle.setheading(0)
    if dark:
        on_click_light = True
        theme_turtle.shape(dark_img)
    else:
        on_click_light = False
        theme_turtle.shape(light_img)
    theme_turtle.onclick(lambda x,y: ToggleTheme())
    
def ToggleTheme():
    global on_click_light
    if on_click_light:
        wn.bgcolor('white')
        ToggleThemeBtn(dark=False)
    else:
        wn.bgcolor(colors['background'])
        ToggleThemeBtn(dark=True)

# Gets values of intersection and the y and x coords of the tiles and populates lists accordingly - Yuvraj
def fetch_values():
    start_x_pos = -190
    start_y_pos = -150
    
    for y in range(6):
        for x in range(5):
            intersection_coords.append([(start_x_pos + x * 75), -(start_y_pos + y * 75)])
            if y == 0:
                x_coords.append(start_x_pos + x * 75)
        lines[y] = intersection_coords[-5:]
        y_coords.append((intersection_coords[-1])[1])
        
# uses File IO to randomly select a word from a .txt file with a lengthy selection of words - Gavin
def choose_word():
    global chosen_word_list
    word_list_file = open("word_list.txt", "r")
    word_list = word_list_file.readlines()
    formatted_word_list = []
    for word in word_list:
        formatted_word_list.append(word.strip())
    word = random.choice(formatted_word_list)
    chosen_word_list = list(word.upper())
    return(chosen_word_list)

# displays either a win or loose screen for the user - Gavin
def WinOrLose(win):
    misc_drawer._tracer(False)
    misc_drawer.hideturtle()
    height = 200
    width = 375
    corner_radius = 20
    fill_color = 'white'
    border_color = colors['background']
    misc_drawer.begin_fill()
    misc_drawer.penup()
    misc_drawer.goto(lines[4][4][0] + 75, lines[4][4][1] + 30)
    misc_drawer.pendown()

    misc_drawer.color(border_color)
    misc_drawer.pensize(6)
    misc_drawer.fillcolor(fill_color)

    # Draw the rounded corners - Yuvraj
    for _ in range(2):
        misc_drawer.circle(corner_radius, 90)
        misc_drawer.forward(height)
        misc_drawer.circle(corner_radius, 90)
        misc_drawer.forward(width)
    misc_drawer.end_fill()


    final_text = trtl.Turtle()
    sub_final_text = trtl.Turtle()

    final_text.hideturtle()
    sub_final_text.hideturtle()
    if win:
        final_text.color(colors['green'])
        final_text.write('YOU WIN!', align='center',  font = ("Consolas", 50, 'normal'))
        sub_final_text.penup()
        sub_final_text.goto(0, -45)
        sub_final_text.write(f'You guessed correctly in {typing_line + 1} attempts', align='center',  font = ("Consolas", 15, 'normal'))
    # Lose - Yuvraj
    else:
        final_text.color('red')
        final_text.write('YOU LOSE :(', align='center',  font = ("Consolas", 50, 'normal'))
        sub_final_text.penup()
        sub_final_text.goto(0, -45)
        sub_final_text.write(f'The word was {"".join(chosen_word_list)}', align='center',  font = ("Consolas", 15, 'normal'))
    

    
    
print(choose_word())
fetch_values()
SetUp()
# WinOrLose(True)
    
# ----EVENTS----
# keypresses detector - Yuvraj
for char in string.ascii_letters:
    wn.onkeypress(lambda c = char: AppendVal(c), char)
wn.onkeypress(lambda : SubVal(), 'BackSpace')
wn.onkeypress(lambda : CheckLetters(True), 'Return')
wn.listen()

# keep window open
wn.mainloop()
