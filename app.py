import turtle as trtl
import string


y_positions = [150, 75, 0, -75, -150]

# turtles
letter_drawer = trtl.Turtle()
grid_drawer = trtl.Turtle()

wn = trtl.Screen()


letter_drawer.penup()
for pos in y_positions:
    letter_drawer.goto(-160, pos)
    letter_drawer.write('H E L L O', align="left",font=("Consolas", 50, "normal"))
letter_drawer.write('H E L I O', align="left",font=("Consolas", 50, "normal"))

# for letter in list(string.ascii_letters()):
#     wn.onkeypress(lambda: , letter)

# Gavin
def draw_grid():
    grid_drawer.penup()
    grid_drawer.goto(-160, 225)
    grid_drawer.pendown()
    grid_drawer.forward(200)
    for lines in y_positions:
        grid_drawer.penup()
        grid_drawer.goto(-160, lines)
        grid_drawer.pendown()
        grid_drawer.forward(200)



draw_grid()
wn.mainloop()
