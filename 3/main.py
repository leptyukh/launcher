import eel 
import os

@eel.expose
def snake():
    os.startfile('snake.py')

@eel.expose
def tetris():
    os.startfile('tetris.py')
@eel.expose

def zero():
    os.startfile('zero.py')
eel.init('page') 

@eel.expose
def sea():
    os.startfile('sea.py')   
eel.start('launch.html', size=(1920, 1080))

