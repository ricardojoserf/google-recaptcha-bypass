import os, sys, time, argparse, pyautogui
from random import randint
import pyscreenshot as ImageGrab
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

min_diff = 3
min_offset = 200
w,h = pyautogui.size()

	
def finish():
	sys.exit()


def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-u', '--url', required=True, action='store', help='Option')
  my_args = parser.parse_args()
  return my_args


def move(obj_x,obj_y,t,mov_val,delay):
	time.sleep(delay)
	init_t = t
	init_mov_val = mov_val

	while 1:
		w,h = pyautogui.position()
		mov_val = int(mov_val)
		# X
		if (abs(w-obj_x) < min_diff):
			randx = 0
		else:
			if(w<obj_x):
				randx = abs(randint(0,mov_val))
			else:
				randx = -1 * abs(randint(0,mov_val))
		# Y
		if (abs(h-obj_y) < min_diff):
			randy = 0
			if randx == 0:
				# pyautogui.click()
				break
		else:
			if(h<obj_y):
				randy = abs(randint(0,mov_val))
			else:
				randy = -1 * abs(randint(0,mov_val))
		pyautogui.moveRel(randx,randy,t)
		
		if t > 0.001:
			t *= 0.97
			mov_val *= 0.97
		else:
			t = init_t
			mov_val = init_mov_val
			break

'''
def listColors():
	image = ImageGrab.grab()
	w,h = pyautogui.size()
	print w,"x",h
	total = []
	types = {}
	offset = 100
	y = offset
	count = 0	
	while y < (h-offset):
		y += 1
		line_colors = []
		for x in range(0,w-1):
			color = image.getpixel((x, y))
			total.append(color)
			line_colors.append(color)
			if color not in types:
				types[color] = 0
			else:	
				types[color] += 1
	
	for item in sorted(types.items(), key=lambda x: x[1]):
		print item
	print "len(total)", len(total)
	print "len(types)", len(types)


def checkMoved(coordx, coordy):
	my_position = pyautogui.position()
	diffx = abs ( my_position[0] - coordx)
	diffy = abs ( my_position[1] - coordy)
	# print diffx,diffy
	if abs(diffx) > 100 or abs(diffy) > 100:
		move(coordx, coordy, 0.1, 30, 0)
		# print diffx,diffy
		pyautogui.click()
	else:
		return True	
'''


def checkGreen():
	image = ImageGrab.grab()
	verde = (0, 158, 85)
	w,h = pyautogui.size()
	count = 0

	for y in range(0,h-1):
	    for x in range(0,w-1):
	        color = image.getpixel((x, y))
	        if color == verde:
	        	count +=1
	
	return (count>50)


def colorLocate():
	image = ImageGrab.grab()
	w,h = pyautogui.size()
	offset = 100
	y = offset
	coordinates_x = []
	coordinates_y = []	

	while y < (h-offset):
		y += 1
		line_colors = []
		for x in range(0,w-1):
			color = image.getpixel((x, y))
			line_colors.append(color)
		# Gris y azul de flecha
		# Sale 77 veces
		srch_clr_1 = (155,155,155)
		# Sale 23 veces
		srch_clr_2 = (167,195,231)
		# Todas las coordenadas con uno de esos dos colores
		if srch_clr_1 in line_colors and srch_clr_2 in line_colors:		
			for x in range(0,w-1):
				color = image.getpixel((x, y))
				if color == srch_clr_2:
					if x not in coordinates_x:
						coordinates_x.append(x)
					if y not in coordinates_y:
						coordinates_y.append(y)
	
	coordx = int ( sum(coordinates_x)/len(coordinates_x)  )
	coordy = int ( sum(coordinates_y)/len(coordinates_y)  )
	return (coordx, coordy)


def openchrome(url):
	options = webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	options.add_argument("--incognito")
	options.add_argument("--disable-infobars")
	driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=options)
	if url is not None:
		driver.get(url)
	return driver


def randomMovement(n):
	for i in range(0,n):
		move(randint(min_offset,(w-min_offset)), randint(min_offset,(h-min_offset)), 0.05, 50, 0)

'''
def imageLocate():
	loc = pyautogui.locateOnScreen('Scripts\mouse\captura.png')
	margin = 10

	if loc is None:
		print "Captcha not detected"
		finish()

	top_left = loc[0]
	top_right = (loc[0]+loc[2])
	top_top = loc[1]
	top_bottom = (loc[1]+loc[3])
	
	x = randint(top_left + margin, top_right - margin)
	y = randint(top_top + margin, top_bottom - margin)
	coords = (x,y)

	return coords
'''

def prepareElements(n):
	texts=[]
	positions = []

	for it in range(1,(int(n)+1)):
		text = raw_input("Text for element "+str(it)+": ")
		texts.append(text)
		
	for it in range(1,(int(n)+1)):
		t = raw_input("Put cursor over element "+str(it)+" and press Enter")
		positions.append(pyautogui.position())
	
	return texts, positions


def main():
	args = get_args()
	url = args.url

	### CLICKABLE ELEMENTS ###
	driver = openchrome(url)
	number_inputs_pre = raw_input("Number of elements before captcha: ")
	pre_texts, pre_positions = prepareElements(number_inputs_pre)
	number_inputs_post = raw_input("Number of elements after captcha: ")
	post_texts, post_positions = prepareElements(number_inputs_post)
	driver.close()
	### CLICKABLE ELEMENTS ###
	
	done = False

	while done is False:
		print "Initializing..."

		### RANDOM ###
		randomMovement(1)
		### RANDOM ###
		
		driver = openchrome(url)
		time.sleep(2)

		### PRE ELEMENTS ###
		for ind in range(0,len(pre_positions)):
			pos =  pre_positions[ind]
			txt = pre_texts[ind]
			move(pos[0],pos[1],0.1,30,0)
			pyautogui.click()
			pyautogui.typewrite(txt)
			time.sleep(1)
		### PRE ELEMENTS ###

		### CAPTCHA ###
		coords = colorLocate()
		#coords = imageLocate()
		while ( (abs(pyautogui.position()[0] - coords[0])>100) or (abs(pyautogui.position()[1] - coords[1])>100) ):
			move(coords[0],coords[1],0.1,30,0)
		pyautogui.click()
		time.sleep(2)
		done = checkGreen()
		### CAPTCHA ###

		### RANDOM ###
		randomMovement(1)
		### RANDOM ###

		### POST ELEMENTS ###
		for ind in range(0,len(post_positions)):
			pos =  post_positions[ind]
			txt = post_texts[ind]
			pyautogui.moveTo(pos[0],pos[1])
			pyautogui.click()
			pyautogui.typewrite(txt)
			time.sleep(1)
		### POST ELEMENTS ###

		time.sleep(5)
		if driver.current_url != url:
			print "EXITO"
			finish()
		driver.close()


if __name__ == "__main__":
	main()