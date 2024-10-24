import turtle
import colorsys
from settings import *


t = turtle.Turtle()
screen = turtle.Screen()

screen.setup(width, height)
screen.title("LOADING")
screen.bgpic("bg.png")

# turtle speed and pen width
t.speed(0)
t.width(7)

def loadingPage():

    a = 0
    h = 0
    t.hideturtle()


    for i in range(25):
        
        c = colorsys.hsv_to_rgb(h, 1, 1)
        
        t.color(c)
        
        t.up()
        t.seth(a)
        t.fd(-20)  
        t.down()
        t.fd(10)  
        t.up()
    
        a += -22.5 
        h += 0.02  

    turtle.bye()
    screen.mainloop()
loadingPage()