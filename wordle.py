import turtle as trtl
import string
import random

import requests

intersection_coords = []
x_coords = []
y_coords = []
lines = {}

typing_list = []
typed_list = []
chosen_word_list = []

# 0 = not in word, 1 = yellow, 2 = green
check = ['0', '0', '0', '0', '0']

typing_line = 0

colors = {
    'background': '#121213',
    'foreground': '#818384',
    'yellow': '#b59f3b',
    'green': '#538d4e',
    'not in word': '#3a3a3c',
    'blank' : '#3a3a3c',
}

y_turtles = []

check_finished = False

# turtles
letter_drawer = trtl.Turtle()
grid_drawer = trtl.Turtle()
misc_drawer = trtl.Turtle()

wn = trtl.Screen()
wn.bgcolor(colors['background'])

def StampCheck(color, letter):
    global tile
    if color == '1':
        location = lines[typing_line][typed_list.index(letter)]
    else:
        location = lines[typing_line][typed_list_copy.index(letter)]
    location = [location[0]+37.5, location[1]+37.5]
    tile.goto(location)
    if color == '2':
        tile.color(colors['green'])
    elif color == '1':
        tile.color(colors['yellow'])
    else:
        tile.color(colors['not in word'])
    tile.stamp()
    tile.goto(1000, 1000)
    UpdateLine()

def CheckLetters():
    global typing_line, typed_list, typed_list_copy, check_finished
    if len(typing_list) == 5 and check_finished:
        if not CheckIfWord():
            return
        typed_list = typing_list.copy()
        typed_list_copy = typed_list.copy()
        for letter in typed_list_copy:
            index = typed_list_copy.index(letter)
            if letter == chosen_word_list[index]:
                check[index] = "2"
                StampCheck('2', letter)
            elif letter in chosen_word_list and letter != chosen_word_list[index]:
                check[index] = "1"
                StampCheck('1', letter)
            else:
                check[index] = "0"
                StampCheck('0', letter)
            typed_list_copy[index] = '_'
        typing_line += 1
        typing_list.clear()
    check_finished = True

def CheckIfWord():
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{''.join(typing_list)}")
    if response.status_code == 404:
        return False
    else:
        return True
    
def UpdateLine():
    y_turtles[typing_line].clear()
    y_turtles[typing_line].write(' '.join(typing_list), align="left",font=("Consolas", 52, "bold"))

def AppendVal(letter):
    if len(typing_list) != 5:
        typing_list.append(letter.upper())
        UpdateLine()
def SubVal():
    if len(typing_list) != 0:
        typing_list.pop()
        print(typing_list)
        UpdateLine()

def SetupLayout():
    misc_drawer._tracer(False)

# Gavin & Father Yuvraj
def DrawGrid():
    global intersection_coords, tile
    
    grid_drawer._tracer(True)
    
    start_x_pos = -185
    start_y_pos = -225

    
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

def fetch_values():
    start_x_pos = -185
    start_y_pos = -150
    
    for y in range(6):
        for x in range(5):
            intersection_coords.append([(start_x_pos + x * 75), -(start_y_pos + y * 75)])
            if y == 0:
                x_coords.append(start_x_pos + x * 75)
        lines[y] = intersection_coords[-5:]
        y_coords.append((intersection_coords[-1])[1])
        
# Gavin
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


SetupLayout()
fetch_values()
DrawGrid()
print(choose_word())
print(intersection_coords)
print(x_coords)
print(y_coords)
print(lines)

letter_drawer.penup()
i = 1
for y in y_coords:
    #Cite = Copilot(AI)[prompt: how to make 5 new turtles variables and add them to a list?]
    new_turtle = trtl.Turtle()
    new_turtle.penup()
    new_turtle.color('white')
    new_turtle.goto(x_coords[0] + 20, y)
    new_turtle.write(' ', align="left",font=("Consolas", 52, "bold"))
    y_turtles.append(new_turtle)
    
for char in string.ascii_letters:
    wn.onkeypress(lambda c = char: AppendVal(c), char)
wn.onkeypress(lambda : SubVal(), 'BackSpace')
wn.onkeypress(lambda : CheckLetters(), 'Return')
wn.listen()

# keep window open
wn.mainloop()