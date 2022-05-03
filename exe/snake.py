# -*- coding: utf-8 -*-
import os, time, random
from threading import Thread

if os.getenv("OS") in ["Windows_NT","Linux"]:
    import msvcrt as m


# Начальные значения
x = 5
y = 3
game_thread = True
fruit_cord_x = 5
fruit_cord_y = 6
button_defult = "d"
score = 0
icon_player = "►"
tail = "o"
last2X = 0; last2Y = 0
lastX = 0; lastY = 0
elemX = [0 for i in range(100)]; elemY = [0 for i in range(100)]
 
def clear():
    for i in ["cls", "clear"]:
        os.system(i)
        break
 
 
def board(width: int = 40, height: int = 20, pos_player_x: int = x, pos_player_y: int = y):
    global score, fruit_cord_x, fruit_cord_y, game_thread, icon_player, last2X, lastX, lastY, last2Y, elemY, elemX
    clear()
    for i in range(height):
        for j in range(width):
            if pos_player_x == fruit_cord_x and pos_player_y == fruit_cord_y:
                fruit_cord_x = random.randint(2, width-1)
                fruit_cord_y = random.randint(2, height-1)
                score += 1
 
            for el in range(score):
                if pos_player_x == elemX[el] and pos_player_y == elemY[el]:
                    print(f"\nGAME OVER\nScore: {score}")
                    game_thread = False
                    exit()
 
            if not(x in range(width-39)) and not(y in range(height-1)) or not(x in range(width-1)) and not(y in range(height-19)):
                print(f"\nGAME OVER\nScore: {score}")
                game_thread = False
                exit()          
 
            if j == 0:
                print('#', end='')
            elif i == 0:
                print('#', end='')
            elif i == height-1:
                print('#', end='')
            elif j == width-1:
                print('#', end='')
            elif pos_player_x == j and pos_player_y == i:
                print(icon_player, end='')
            elif fruit_cord_x == j and fruit_cord_y == i:
                print("*", end='')
            else:
                pr = True
                for ls in range(score):
                    if elemX[ls] == j and elemY[ls] == i:
                        print(tail, end="")
                        pr = False
                if pr: print(' ', end='')
 
        print()
    # интерфейс
    print(f"X player: {pos_player_x} || Y player: {pos_player_y}")
    print(f"Score: {score}\n\n\t\tWASD / Стрелочки - перемещение\n\t\t\tESC - выйти")
    lastX = pos_player_x; lastY = pos_player_y
    if score > 0:
        for el in range(score):
            last2X = elemX[el]; last2Y = elemY[el]
            elemX[el] = lastX; elemY[el] = lastY
            lastX = last2X; lastY = last2Y
 
def button_move():  
    global button_defult
    while game_thread:
        button_defult = m.getch()[0]
 
def move(): 
    global x, y, game_thread, button_defult, icon_player
 
    while game_thread:
        if button_defult in [""," "]: button_defult = "d"
        elif button_defult in ["w", 119, 230, 72]: y -= 1; icon_player = "▲"
        elif button_defult in ["a", 97, 228, 75]: x -= 1; icon_player = "◄"
        elif button_defult in ["s", 115, 235, 80]: y += 1; icon_player = "▼"
        elif button_defult in ["d", 100, 162, 77]: x += 1; icon_player = "►"
 
        elif button_defult in ["exit", 27]:
            print("Вы покинули игру")
            game_thread = False
            exit()
 
        board(pos_player_x=x, pos_player_y=y)
 
        time.sleep(.2)
 
 
def main():
    board()
    Thread(target=move).start()
    Thread(target=button_move).start()
 
if __name__ == '__main__':
    clear() #clear
    main()

