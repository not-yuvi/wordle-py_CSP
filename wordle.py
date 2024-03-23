import turtle as trtl
import string
import random

centered_coords = []
typing_list = ["H", "E", "L", "L", "O"]

# turtles
letter_drawer = trtl.Turtle()
grid_drawer = trtl.Turtle()
misc_drawer = trtl.Turtle()

wn = trtl.Screen()
wn.bgcolor('#404140')




# for letter in list(string.ascii_letters()):
#     wn.onkeypress(lambda: , letter)

def setup_layout():
    misc_drawer._tracer(False)
    misc_drawer.fillcolor('#EDF4EE')
    misc_drawer.penup()
    misc_drawer.goto(-200, 250)
    misc_drawer.pendown()
    misc_drawer.begin_fill()
    misc_drawer.goto(200, 250)
    misc_drawer.goto(200, -250)
    misc_drawer.goto(-200, -250)
    misc_drawer.goto(-200, 250)
    misc_drawer.end_fill()

# Gavin
def draw_grid():
    start_x_pos = -185
    start_y_pos = -150
    grid_drawer._tracer(True)
    grid_drawer.speed(8)
    grid_drawer.pensize(5)
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
        
    for x in range(5):
        for y in range(5):
            centered_coords.append([start_x_pos + x * 75, start_y_pos + y * 75])
        
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
draw_grid()
print(choose_word())
print(centered_coords)

textle = trtl.Turtle()
textle.shape('square')
textle.color('yellow')
textle.shapesize(3)
textle.penup()
for coords in centered_coords:
    textle.goto(coords[0]+37.5, coords[1]+37.5)
    textle.stamp()

letter_drawer.penup()
y_coords = centered_coords[0:5]
for pos in y_coords:
    letter_drawer.color('#404140')
    letter_drawer.goto(-165, pos[1])
    letter_drawer.write(' '.join(typing_list), align="left",font=("Consolas", 52, "bold"))

# keep window open
wn.mainloop()