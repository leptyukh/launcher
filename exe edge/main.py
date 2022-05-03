from statistics import mode
import eel 
import subprocess
import os
path_init_file = os.path.abspath('page')
print(path_init_file)

@eel.expose
def snake():
    os.startfile()

@eel.expose
def tetris():
    os.startfile('tetris.py')
@eel.expose
def zero():
    os.startfile('zero.py')
eel.init(path_init_file) 

@eel.expose
def sea():
    os.startfile('sea.py')   
eel.start('launch.html', size=(1920, 1080), mode='edge')

