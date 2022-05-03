import eel 
import os
path_init_file = os.path.abspath('page')
print(path_init_file)
@eel.expose
def snake():
    os.startfile('')

@eel.expose
def tetris():
    os.startfile('')
@eel.expose
def zero():
    os.startfile('')
eel.init(path_init_file) 

@eel.expose
def sea():
    os.startfile('')
eel.start('launch.html', size=(1920, 1080))

