import turtle as trtl
import string
import random


y_positions = [150, 75, 0, -75, -150]

# turtles
letter_drawer = trtl.Turtle()
grid_drawer = trtl.Turtle()

wn = trtl.Screen()


letter_drawer.penup()
for pos in y_positions:
    letter_drawer.goto(-160, pos)
    letter_drawer.write('H E L L O', align="left",font=("Consolas", 50, "normal"))


# for letter in list(string.ascii_letters()):
#     wn.onkeypress(lambda: , letter)


# Gavin
def draw_grid():
    grid_drawer._tracer(False)
    grid_drawer.pensize(5)
    i = 0
    for lines in y_positions:
        grid_drawer.penup()
        grid_drawer.goto(-175, lines + 75)
        grid_drawer.pendown()
        grid_drawer.forward(362.5)
    
    grid_drawer.penup()
    grid_drawer.goto(-175, -150)
    grid_drawer.pendown()
    grid_drawer.forward(362.5)

    grid_drawer.right(90)
    for lines in range(7):
        grid_drawer.penup()
        grid_drawer.goto(-175 + i, 225)
        grid_drawer.pendown()
        grid_drawer.forward(375)
        i += 72.5
# Gavin
def choose_word():
    word_list_file = open("word_list.txt", "r")
    word_list = word_list_file.readlines()
    formatted_word_list = []
    for word in word_list:
        formatted_word_list.append(word.strip())
    word = random.choice(formatted_word_list)
    return(word)



draw_grid()
print(choose_word())

# keep window open
wn.mainloop()