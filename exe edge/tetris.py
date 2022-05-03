
import ctypes 
import time
import copy
import random
import msvcrt
 
class COORD(ctypes.Structure):  #define a structure in python to use C api
	 _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)] 
	 def __init__(self,x,y):
		 self.X = x
		 self.Y = y
 
global STD_OUTPUT_HANDLE
STD_OUTPUT_HANDLE= -11
 
global std_out_handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
 
COLUMN_T = 16
ROW_T = 30
INIT_POS = COORD(12,1)   #absolute pos 
DEGREE_OF_DIFFICULTY = 25   #the smaller the harder
 
global DIAMOND
DIAMOND = {"BLOCKS":"█" , "BLANK":" " , "BOUNDARY":"▓" , "PREVIEW":"○" ,"PERISH":"☺"}
 
global BOX 
BOX = [[DIAMOND["BLANK"]for _ in range(COLUMN_T)]for _ in range(ROW_T)]
 
global BASE_BLOCK
BASE_BLOCK = {
			  "Z" :[COORD(0,0),COORD(-1,0),COORD(0,1),COORD(1,1)],
			  "rZ":[COORD(0,0),COORD(1,0),COORD(0,1),COORD(-1,1)],
			  "O" :[COORD(0,0),COORD(1,0),COORD(0,1),COORD(1,1)],
			  "L" :[COORD(0,0),COORD(0,1),COORD(0,2),COORD(1,2)],
			  "rL":[COORD(0,0),COORD(0,1),COORD(0,2),COORD(-1,2)],
			  "I" :[COORD(0,0),COORD(0,1),COORD(0,2),COORD(0,3)],
			  "T" :[COORD(0,0),COORD(-1,0),COORD(1,0),COORD(0,1)]
			}
 
def fill_pos(coord,char):
	tmp_coord = COORD(coord.X * 2 + INIT_POS.X,coord.Y + INIT_POS.Y)    #trans relative pos to absolute pos
	ctypes.windll.kernel32.SetConsoleCursorPosition(std_out_handle,tmp_coord)
	print(char)
 
def move_down(BLOCK):
	if ismove(BLOCK,"down"):		
		perish_block(BLOCK)
		generate_block(BLOCK,"down")
	else:
		perish_line()
		check_lose()
		if GAME_FLAG == "ON GAME":     
			creat_block()
 
def move_left(BLOCK):
	if ismove(BLOCK,"left"):
		perish_block(BLOCK)
		generate_block(BLOCK,"left")
		preview(BLOCK)
		generate_block(BLOCK)
		
def move_right(BLOCK):
	if ismove(BLOCK,"right"):		
		perish_block(BLOCK)
		generate_block(BLOCK,"right")
		preview(BLOCK)
		generate_block(BLOCK)
		
def isin(BLOCK,one_block):
	in_flag = False
	for each_block_coord in BLOCK:
		if each_block_coord.X == one_block.X and \
		   each_block_coord.Y == one_block.Y:
			in_flag = True
			break
	return in_flag
 
def ismove(BLOCK,DIRECTION = "original",BE_SPINED_BLOCK = None):
	move_flag = True
	if DIRECTION == "down":
		for each_block_coord in BLOCK:
			tmp_block = COORD(each_block_coord.X,each_block_coord.Y + 1)
			if not isin(BLOCK,tmp_block):
				if BOX[each_block_coord.Y + 1][each_block_coord.X] == DIAMOND["BLOCKS"] or \
				   BOX[each_block_coord.Y + 1][each_block_coord.X] == DIAMOND["BOUNDARY"]:
					move_flag = False
					break			
	elif DIRECTION == "left":
		for each_block_coord in BLOCK:
			tmp_block = COORD(each_block_coord.X - 1,each_block_coord.Y)
			if not isin(BLOCK,tmp_block):
				if BOX[each_block_coord.Y][each_block_coord.X - 1] == DIAMOND["BLOCKS"] or \
				   BOX[each_block_coord.Y][each_block_coord.X - 1] == DIAMOND["BOUNDARY"]:
					move_flag = False
					break				
	elif DIRECTION == "right":
		for each_block_coord in BLOCK:
			tmp_block = COORD(each_block_coord.X + 1,each_block_coord.Y)
			if not isin(BLOCK,tmp_block):
				if BOX[each_block_coord.Y][each_block_coord.X + 1] == DIAMOND["BLOCKS"] or \
				   BOX[each_block_coord.Y][each_block_coord.X + 1] == DIAMOND["BOUNDARY"]:
					move_flag = False
					break
	elif DIRECTION == "spin":
		for each_block_coord in BLOCK:
			tmp_block = COORD(each_block_coord.X,each_block_coord.Y)
			if not isin(BE_SPINED_BLOCK,tmp_block):
				if each_block_coord.X >= len(BOX[each_block_coord.Y]) or \
				   each_block_coord.X < 0 or \
				   BOX[each_block_coord.Y][each_block_coord.X] == DIAMOND["BLOCKS"] or \
				   BOX[each_block_coord.Y][each_block_coord.X] == DIAMOND["BOUNDARY"]:
					move_flag = False
					break
	else:
		for each_block_coord in BLOCK:
			if each_block_coord.X >= len(BOX[each_block_coord.Y]) or \
			   each_block_coord.X < 0 or \
			   BOX[each_block_coord.Y][each_block_coord.X] == DIAMOND["BLOCKS"] or \
			   BOX[each_block_coord.Y][each_block_coord.X] == DIAMOND["BOUNDARY"]:
				move_flag = False
				break
	return move_flag
 
def generate_block(BLOCK,DIRECTION = "original",DIAMOND = DIAMOND["BLOCKS"]):
	for each_block_coord in BLOCK:
		if DIRECTION == "down":
			each_block_coord.Y += 1
		elif DIRECTION == "left":
			each_block_coord.X -= 1	
		elif DIRECTION == "right":
			each_block_coord.X += 1
		BOX[each_block_coord.Y][each_block_coord.X] = DIAMOND
		if each_block_coord.Y >= 3:
			fill_pos(each_block_coord,DIAMOND)
		
def perish_block(BLOCK):
	for each_block_coord in BLOCK:
		BOX[each_block_coord.Y][each_block_coord.X] = DIAMOND["BLANK"]
		if each_block_coord.Y >= 3:
			fill_pos(each_block_coord,DIAMOND["BLANK"])
 
def preview(BLOCK):
	global PREVIEW_BLOCK
	perish_block(PREVIEW_BLOCK)
	move_flag = True
	for i in range(1,len(BOX)):
		for each_block_coord in BLOCK:
			tmp_block = COORD(each_block_coord.X,each_block_coord.Y + i)
			if not isin(BLOCK,tmp_block):
				if BOX[each_block_coord.Y + i][each_block_coord.X] == DIAMOND["BLOCKS"] or \
				   BOX[each_block_coord.Y + i][each_block_coord.X] == DIAMOND["BOUNDARY"]:
					j = i - 1
					move_flag = False
					PREVIEW_BLOCK = copy.deepcopy(BLOCK)
					for each_block_coord in PREVIEW_BLOCK:
						each_block_coord.Y += j
						BOX[each_block_coord.Y][each_block_coord.X] = DIAMOND["PREVIEW"]
						if each_block_coord.Y > 3:
							fill_pos(each_block_coord,DIAMOND["PREVIEW"])
					break
		if not move_flag:
			break
 
def perish_line():
	global GAME_SCORE
	offset = 0
	for y in range(1,len(BOX)-1-2):   
		if DIAMOND["BLANK"] not in BOX[len(BOX)-y+offset-1]:
			for x in range(1,len( BOX[len(BOX)-y+offset-1])-1 ):
				generate_block([COORD(x,len(BOX)-(y-offset)-1)],DIRECTION = "original",DIAMOND = DIAMOND["PERISH"])
				time.sleep(0.006)
				perish_block([COORD(x,len(BOX)-(y-offset)-1)])
				time.sleep(0.003)
			GAME_SCORE += 10
			fill_pos(COORD(25,18),"GAME SCORE: " + str(GAME_SCORE))
			offset += 1
		for _y in range(1+y-offset,len(BOX)-2): 
			if DIAMOND["BLOCKS"] not in BOX[_y]:
				continue
			else:
				line = []
				for _x in range(1,len( BOX[len(BOX)-_y])-1 ):					
					if BOX[_y][_x] == DIAMOND["BLOCKS"]:
						line.append(COORD(_x,_y))
				if ismove(line,"down"):
					perish_block(line)
					generate_block(line,"down")
					time.sleep(0.015)
 
def spin_pos(BLOCK,offset = (0,0)):
	max_y = max(BLOCK,key = lambda b:b.Y).Y	
	min_x = min(BLOCK,key = lambda b:b.X).X
	for each_block_coord in BLOCK:
		x_tmp = each_block_coord.X
		each_block_coord.X = -(each_block_coord.Y - BLOCK[0].Y) + BLOCK[0].X
		each_block_coord.Y = (x_tmp - BLOCK[0].X) + BLOCK[0].Y
	min_x_n = min(BLOCK,key = lambda b:b.X).X	
	max_y_n = max(BLOCK,key = lambda b:b.Y).Y
	for each_block_coord in BLOCK:
		each_block_coord.X += ((min_x - min_x_n) + offset[0])
		each_block_coord.Y += ((max_y - max_y_n) + offset[1])
 
def isspin(BLOCK):
	offset = 0
	spin_flag = True
	SPIN_BLOCK = copy.deepcopy(BLOCK)
	spin_pos(SPIN_BLOCK)
	if not ismove(SPIN_BLOCK,DIRECTION = "spin",BE_SPINED_BLOCK = BLOCK): 
		for each_block_coord in BLOCK:
			BOX[each_block_coord.Y][each_block_coord.X] = DIAMOND["BLANK"]
		while not ismove(SPIN_BLOCK):
			if ismove(SPIN_BLOCK,DIRECTION = "left"):
				offset -= 1
				for each_block_coord in SPIN_BLOCK:
					each_block_coord.X -= 1
			else:
				spin_flag = False
				break
		for each_block_coord in BLOCK:
			BOX[each_block_coord.Y][each_block_coord.X] = DIAMOND["BLOCKS"] 		
	return (spin_flag,offset)
 
	
def spin(BLOCK):
	if isspin(BLOCK)[0]:
		offset = isspin(BLOCK)[1]
		perish_block(BLOCK)
		spin_pos(BLOCK,(offset,0))
		preview(BLOCK)
		generate_block(BLOCK)
	else:
		pass
 
def check_lose():
	global GAME_FLAG
	if DIAMOND["BLOCKS"] in BOX[2] or DIAMOND["PREVIEW"] in BOX[2]:   
		generate_block(BLOCK)          
		GAME_FLAG = "FAIL   "
		fill_pos(COORD(25,16),"GAME STATUS: " + GAME_FLAG)
		
def drop(BLOCK):
	perish_block(BLOCK)
	generate_block(PREVIEW_BLOCK)
	perish_line()
	check_lose()
	if GAME_FLAG == "ON GAME":      
		creat_block()
 
def creat_next_block():
	global NEXT_BLOCK
	for each_block_coord in NEXT_BLOCK:
		fill_pos(each_block_coord,DIAMOND["BLANK"])
	NEXT_BLOCK = copy.deepcopy(BASE_BLOCK[list(BASE_BLOCK.keys())[random.randint(0,len(BASE_BLOCK)-1)]])
	for k in range(0,random.randint(0,4)):
		spin_pos(NEXT_BLOCK)
	min_x = min(NEXT_BLOCK,key = lambda b:b.X).X	
	max_y = max(NEXT_BLOCK,key = lambda b:b.Y).Y
	for each_block_coord in NEXT_BLOCK:
		each_block_coord.X += (COLUMN_T + 12 - min_x)
		each_block_coord.Y += (10 - max_y)
		fill_pos(each_block_coord,DIAMOND["BLOCKS"])
 
def creat_block():
	global BLOCK
	global NEXT_BLOCK
	global PREVIEW_BLOCK
	BLOCK = copy.deepcopy(NEXT_BLOCK)
	creat_next_block()
	PREVIEW_BLOCK = []
	max_y = max(BLOCK,key = lambda b:b.Y).Y
	min_x = min(BLOCK,key = lambda b:b.X).X
	for each_block_coord in BLOCK:
		each_block_coord.X += (int(COLUMN_T/2)-1 - min_x)
		each_block_coord.Y += (3 - max_y)
	generate_block(BLOCK)
	preview(BLOCK)
 
def init():
	global GAME_SCORE
	GAME_SCORE = 0
	
	global GAME_FLAG
	GAME_FLAG = "ON GAME"       
	
	global times
	times = 0
	
	for r in range(0,ROW_T):
		if r < 2:
			BOX[r][0] = DIAMOND["BOUNDARY"]
			BOX[r][COLUMN_T - 1] = DIAMOND["BOUNDARY"]
			for c in range(1,COLUMN_T - 1):
				fill_pos(COORD(c,r),DIAMOND["BLANK"])
				BOX[r][c] = DIAMOND["BLANK"]
		elif r == 2:    # 2 is the top bound of the box on screen
			for c in range(COLUMN_T):
				fill_pos(COORD(c,r),DIAMOND["BOUNDARY"])
			for c in range(1,COLUMN_T - 1):
				BOX[r][c] = DIAMOND["BLANK"]
		elif r > 2 and r < ROW_T - 1:
			BOX[r][0] = DIAMOND["BOUNDARY"]
			fill_pos(COORD(0,r),DIAMOND["BOUNDARY"])
			BOX[r][COLUMN_T - 1] = DIAMOND["BOUNDARY"]
			fill_pos(COORD(COLUMN_T - 1,r),DIAMOND["BOUNDARY"])
			for c in range(1,COLUMN_T - 1):
				fill_pos(COORD(c,r),DIAMOND["BLANK"])
				BOX[r][c] = DIAMOND["BLANK"]
		elif r == ROW_T - 1:
			for c in range(COLUMN_T):
				BOX[r][c] = DIAMOND["BOUNDARY"]
				fill_pos(COORD(c,r),DIAMOND["BOUNDARY"])
	
	fill_pos(COORD(25,3),"NEXT BLOCK:")
	for r in range(10):
		for c in range(8):
			fill_pos(COORD(26+c,4+r),DIAMOND["BLANK"])
	
	fill_pos(COORD(25,16),"GAME STATUS: " + GAME_FLAG)
	fill_pos(COORD(25,18),DIAMOND["BLANK"]*20)
	fill_pos(COORD(25,18),"GAME SCORE: " + str(GAME_SCORE))
	fill_pos(COORD(25,22),"← → ↓ TO MOVE  ↑ TO SPIN")
	fill_pos(COORD(25,24),"SPACE TO PAUSE")
	fill_pos(COORD(25,26),"ENTER TO RESTART")
	fill_pos(COORD(25,28),"ESC TO EXIT")
			
	global NEXT_BLOCK
	NEXT_BLOCK = copy.deepcopy(BASE_BLOCK[list(BASE_BLOCK.keys())[random.randint(0,len(BASE_BLOCK)-1)]])
	for k in range(0,random.randint(0,3)):
		spin_pos(NEXT_BLOCK)
	min_x = min(NEXT_BLOCK,key = lambda b:b.X).X	
	max_y = max(NEXT_BLOCK,key = lambda b:b.Y).Y
	for each_block_coord in NEXT_BLOCK:
		each_block_coord.X += (COLUMN_T + 12 - min_x)
		each_block_coord.Y += (10 - max_y)
	
def kbfunc(): 				
   x = msvcrt.kbhit()
   if x: 
      ret = ord(msvcrt.getch()) 
   else: 
      ret = None 
   return ret
			
def main():
	global times
	global GAME_FLAG
	init()
	creat_block()
	
	while True: 
		if  GAME_FLAG == "ON GAME":      
			times+=1
			time.sleep(.01)
			if times == DEGREE_OF_DIFFICULTY:
				move_down(BLOCK)
				times = 0
	
			r = kbfunc()
			if r == 75:
				move_left(BLOCK)
			elif r == 77:
				move_right(BLOCK)
			elif r == 80:
				drop(BLOCK)
			elif r == 72:
				spin(BLOCK)
			elif r == 27:
				exit()
			elif r == 32:
				GAME_FLAG = "PAUSE  "       
				fill_pos(COORD(25,16),"GAME STATUS: " + GAME_FLAG)
			elif r == 13:
				init()
				creat_block()
		elif GAME_FLAG == "PAUSE  ":
			r = kbfunc()
			if r == 32:
				GAME_FLAG = "ON GAME"
				fill_pos(COORD(25,16),"GAME STATUS: " + GAME_FLAG)
			elif r == 13:
				init()
				creat_block()
			elif r == 27:
				exit()	
		else:
			r = kbfunc()
			if r == 13:
				init()
				creat_block()
			elif r == 27:
				exit()	
 
if __name__ == "__main__":
	main()