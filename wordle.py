import turtle as trtl
import string
import random

intersection_coords = []
x_coords = []
y_coords = []
lines = {}
typing_list = ["H", "E", "L", "L", "O"]

colors = {
    'background': '#121213',
    'foreground': '#818384',
    'yellow': '#b59f3b',
    'green': '#538d4e',
    'not in word': '#3a3a3c',
    'blank' : '#3a3a3c',
}

y_turtles = []


# turtles
letter_drawer = trtl.Turtle()
grid_drawer = trtl.Turtle()
misc_drawer = trtl.Turtle()

wn = trtl.Screen()
wn.bgcolor(colors['background'])




# for letter in list(string.ascii_letters()):
#     wn.onkeypress(lambda: , letter)

def setup_layout():
    misc_drawer._tracer(False)
    # misc_drawer.fillcolor('#EDF4EE')
    # misc_drawer.penup()
    # misc_drawer.goto(-200, 250)
    # misc_drawer.pendown()
    # misc_drawer.begin_fill()
    # misc_drawer.goto(200, 250)
    # misc_drawer.goto(200, -250)
    # misc_drawer.goto(-200, -250)
    # misc_drawer.goto(-200, 250)
    # misc_drawer.end_fill()

# Gavin
def draw_grid():
    global start_x_pos, start_y_pos, intersection_coords
    
    grid_drawer._tracer(True)
    
    textle = trtl.Turtle()
    textle.shape('square')
    textle.color(colors['green'])
    textle.shapesize(3.5)
    textle.penup()
    for coords in intersection_coords:
        textle.goto(coords[0]+37.5, coords[1]+37.5)
        textle.stamp()
    
    grid_drawer.speed(8)
    grid_drawer.pensize(6)
    for count in range(6):
        grid_drawer.penup()
        grid_drawer.goto(start_x_pos, start_y_pos + count * 75)
        grid_drawer.pendown()
        grid_drawer.forward(375)
        
        
        grid_drawer.right(90)
        grid_drawer.penup()
        grid_drawer.goto(start_x_pos + count * 75, -start_y_pos + 75)
        grid_drawer.pendown()
        grid_drawer.forward(375)
        grid_drawer.left(90)

def fetch_values():
    global start_x_pos, start_y_pos
    start_x_pos = -185
    start_y_pos = -150
    
    for y in range(5):
        for x in range(5):
            intersection_coords.append([(start_x_pos + x * 75), -(start_y_pos + y * 75)])
            if start_x_pos + x * 75 not in x_coords:
                x_coords.append(start_x_pos + x * 75)
        lines[y] = intersection_coords[-5:]
        y_coords.append((intersection_coords[-1])[1])
        
# Gavin
def choose_word():
    word_list_file = open("word_list.txt", "r")
    word_list = word_list_file.readlines()
    formatted_word_list = []
    for word in word_list:
        formatted_word_list.append(word.strip())
    word = random.choice(formatted_word_list)
    return(word)


setup_layout()
fetch_values()
draw_grid()
print(choose_word())
print(intersection_coords)
print(x_coords)
print(y_coords)
print(lines)

letter_drawer.penup()
i = 1
for y in y_coords:
    new_turtle = trtl.Turtle()
    new_turtle.penup()
    new_turtle.color('white')
    new_turtle.goto(x_coords[0] + 20, y)
    new_turtle.write(' '.join(typing_list), align="left",font=("Consolas", 52, "bold"))
    y_turtles.append(new_turtle)
    

# keep window open
wn.mainloop()