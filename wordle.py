---imports---
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
lose = False
win = False

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

check_finished = True

# turtles
letter_drawer = trtl.Turtle()
grid_drawer = trtl.Turtle()
misc_drawer = trtl.Turtle()

wn = trtl.Screen()
wn.bgcolor(colors['background'])

# changes teh tile colors depending on how the letters match up with the correct word
def StampCheck(color, index):
    global tile
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

# checks if the letters entered by the user are in the word and in the correct place
# changes the tile colors accordingly
def CheckLetters():
    global typing_line, typed_list, check_finished
    if len(typing_list) == 5 and check_finished:
        if not CheckIfWord():
            return
        win_check = 0
        typed_list = typing_list.copy()
        chosen_word_list_copy = chosen_word_list.copy()
        used_indices = set()  # To keep track of already matched indices
        for i in range(len(typed_list)):
            letter = typed_list[i]
            if letter == chosen_word_list_copy[i]:
                check[i] = "2"  # Correct letter in correct position
                StampCheck('2', i)
                chosen_word_list_copy[i] = None  # Mark this letter as used
                used_indices.add(i)
                win_check += 1
        
        for i in range(len(typed_list)):
            letter = typed_list[i]
            if letter in chosen_word_list_copy and i not in used_indices:
                check[i] = "1"  # Correct letter in wrong position
                StampCheck('1', i)
                used_indices.add(i)
                chosen_word_list_copy[chosen_word_list_copy.index(letter)] = None  # Mark this letter as used

        for i in range(len(typed_list)):
            if check[i] == "0":
                StampCheck('0', i)  # Letter not in the word
        if win_check == 5:
            WinOrLose(True)

        if typing_line == 5:
            WinOrLose(False)
        else:
            typing_line += 1  # Move typing line position outside the loop
            typing_list.clear()
            check_finished = True

# uses Dictionary API to check if the word entered by the user is a real word
def CheckIfWord():
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{''.join(typing_list)}")
    if response.status_code == 404:
        return False
    elif response.status_code == 200:
        return True
    else:
        return True
        print('WARNING: Resource might be down')
        
# updates the line as the user enters in their guess
def UpdateLine():
    global typing_line
    if typing_line <=5:
        y_turtles[typing_line]._tracer(False)
        y_turtles[typing_line].clear()
        y_turtles[typing_line].write(' '.join(typing_list), align="left",font=("Consolas", 52, "bold"))
        y_turtles[typing_line]._tracer(True)
    else:
        typing_line = 5

# ----keypress handle functions----
# Append Val - adds typed letter to the grid for the user to see
# Sub Val - removes last letter when the user hits the backspace key
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
# draws the grid in which the letters are placed
def DrawGrid():
    global intersection_coords, tile
    
    grid_drawer._tracer(True)
    
    start_x_pos = -190
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
    start_x_pos = -190
    start_y_pos = -150
    
    for y in range(6):
        for x in range(5):
            intersection_coords.append([(start_x_pos + x * 75), -(start_y_pos + y * 75)])
            if y == 0:
                x_coords.append(start_x_pos + x * 75)
        lines[y] = intersection_coords[-5:]
        y_coords.append((intersection_coords[-1])[1])
        
# Gavin
# uses File IO to randomly select a word from a .txt file with a lengthy selection of words
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

# displays either a win or loose screen for the user
def WinOrLose(win):
    height = 225
    width = 300
    corner_radius = 20
    fill_color = 'white'
    border_color = 'black'
    misc_drawer.begin_fill()
    misc_drawer.penup()
    misc_drawer.goto(lines[3][4][0], lines[3][4][1])
    misc_drawer.pendown()

    misc_drawer.color(border_color)
    misc_drawer.pensize(6)
    misc_drawer.fillcolor(fill_color)

    # Draw the rounded corners
    for _ in range(2):
        misc_drawer.circle(corner_radius, 90)
        misc_drawer.forward(height)
        misc_drawer.circle(corner_radius, 90)
        misc_drawer.forward(width)
    misc_drawer.end_fill()
    


SetupLayout()
fetch_values()
DrawGrid()
# WinOrLose(True)
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
    new_turtle._tracer(False)
    new_turtle.penup()
    new_turtle.color('white')
    new_turtle.goto(x_coords[0] + 20, y)
    new_turtle.write(' ', align="left",font=("Consolas", 52, "bold"))
    y_turtles.append(new_turtle)
    new_turtle._tracer(True)
for turtle in y_turtles:
    turtle.hideturtle()
    
for char in string.ascii_letters:
    wn.onkeypress(lambda c = char: AppendVal(c), char)
wn.onkeypress(lambda : SubVal(), 'BackSpace')
wn.onkeypress(lambda : CheckLetters(), 'Return')
wn.listen()

# keep window open
wn.mainloop()
