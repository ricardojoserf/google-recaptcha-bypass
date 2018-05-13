import pyautogui, webbrowser, os, sys, time, math, random
from random import randint
import pyscreenshot as ImageGrab
from PIL import ImageChops
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'http://192.168.61.143:5000/login'
min_diff = 3
min_offset = 100
default_delay_app = 10
 # concurrencia = 21
azul_claro = (78, 142, 245)

def printPos(n):
	print "Final position " + str(n) + ": ",pyautogui.position()


def move(obj_x,obj_y,t,mov_val,delay):

	time.sleep(delay)

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
				pyautogui.click()
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
			break



def check1color(color__):
	image = ImageGrab.grab()
	w,h = pyautogui.size()
	count = 0

	for y in range(0,h-1):
	    for x in range(0,w-1):
	        color = image.getpixel((x, y))
	        if color == color__:
	        	count +=1
	return count


def checkColors():
	image = ImageGrab.grab()
	w,h = pyautogui.size()
	print w,"x",h
	
	total = []
	for y in range(0,h-1):
		print y
		for x in range(0,w-1):
			color = image.getpixel((x, y))
			total.append(color)

	my_dict = {i:total.count(i) for i in total}

	print total
	print my_dict

	return total


def openchrome():
	# Abrir pagina
	options = webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	options.add_argument("--incognito")
	options.add_argument("--disable-infobars")
	driver = webdriver.Chrome('C:/chromedriver.exe', chrome_options=options)
	driver.get(url)
	return driver


def main():
			driver = openchrome()
			time.sleep(1)
			#color__ = (28, 61, 172)
			#count = check1color(color__)
			checkColors()
			


if __name__ == "__main__":
	main()
