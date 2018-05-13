import pyautogui, webbrowser, os, sys, time, math, random
from random import randint
import pyscreenshot as ImageGrab
from PIL import ImageChops
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'http://192.168.61.143:5000/login'
min_diff = 3
min_offset = 200

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


def searchCaptcha():
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
	coordx = sorted(coordinates_x)[0]
	coordy = sorted(coordinates_y)[0]
	return coordx,coordy


def openchrome(url):
	# Abrir pagina
	options = webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	options.add_argument("--incognito")
	options.add_argument("--disable-infobars")
	driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=options)
	if url is not None:
		driver.get(url)
	return driver


def check(coordx, coordy):
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

def main():
			w,h = pyautogui.size()
			print "Resolucion: ",w,"x",h			
			#listColors()
			
			done = False

			while done is False:
				# movimiento aleatorio
				move(randint(min_offset,(w-min_offset)), randint(min_offset,(h-min_offset)), 0.05, 50, 0)
				
				# Cargar browser
				# driver = openchrome(url)
				time.sleep(2)
				
				# moverse al captcha
				coordx, coordy = searchCaptcha()
				move(coordx,coordy,0.1,30,0)
				pyautogui.click()

				done = check(coordx, coordy)
				
				time.sleep(5)
				
				# driver.close()



if __name__ == "__main__":
	main()
