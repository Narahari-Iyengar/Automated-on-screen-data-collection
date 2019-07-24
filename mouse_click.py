from pynput.mouse import Listener
import cv2
import numpy as np
from PIL import ImageGrab
from PIL import Image
import pyautogui as pyg
import pytesseract
import time
import imutils

cx,cy = 0,0
def mouse_click():
	def on_click(x,y,button,pressed):
		global cx,cy
		if pressed:
			cx = x
			cy = y
			print("The mouse was clicked at ({},{})".format(x,y))
			listener.stop()	
			
	with Listener(on_click = on_click) as listener:
		global cx,cy
		try:
			listener.join()
		except Exception:
			print("Error")
			listener.stop()	

def select_corner(box):
	print("\nClick on the top left corner of {}: {}_TLC".format(box,box))
	mouse_click()
	box_TLC = np.array([cx,cy])	
	print("{}_TLC = ({},{})".format(box,cx,cy))
	
	print("\nClick on top right corner of {}: {}_TRC".format(box,box))
	mouse_click()
	box_TRC = np.array([cx,cy])
	print("{}_TRC = ({},{})".format(box,cx,cy))
	
	print("\nClick on bottom right corner of {}: {}_BRC".format(box,box))
	mouse_click()
	box_BRC = np.array([cx,cy])	
	print("{}_BRC = ({},{})".format(box,cx,cy))
	
	print("\nClick on bottom left corner of {}: {}_BLC".format(box,box))
	mouse_click()
	box_BLC = np.array([cx,cy])
	print("{}_BLC = ({},{})".format(box,cx,cy))
	
	return box_TLC,box_TRC,box_BRC,box_BLC

def start_position():
	print("\nSelect the starting position")
	mouse_click()
	start_pos = [cx,cy]
	print("The starting position is ({},{})".format(cx,cy))
	return start_pos
	
def yes_or_no(question):
	while "the answer is invalid":
		reply = str( input(question+' (y/n): ')).lower().strip()

		if reply == 'y':
			return True
		elif reply == 'n':
			return False
		else:
			pass	

def save_file(matrix,name):
	np.savetxt(name+'.txt',matrix,delimiter = ',',fmt = '%.2f')
	print("File",name+".txt","has been saved")

def load_file(name):
	name = name+".txt"
	print(name)
	name = np.loadtxt(open(name,"rb"),delimiter=",",skiprows=0)
	return name

def get_image(x1,y1,x2,y2):
	printscreen_pil =  ImageGrab.grab(bbox=(x1,y1,x2,y2))
	printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8')\
	.reshape((printscreen_pil.size[1],printscreen_pil.size[0],3)) 
	# cv2.imshow("img",printscreen_numpy)
	return printscreen_numpy	

def format_string(str1):
	# str1 = (str1.split()[0])
	# str1 = str1.replace("[","")
	print(str1)
	str1 = ''.join(x for x in str1 if x.isdigit())
	if str1:
		str1 = float(str1)
		str1 = str1/10
	else:
		str1 = 0
	return str1

def go_to_next():
	next_image = load_file('next_image')
	x,y = next_image
	pyg.moveTo(x,y,1)
	pyg.click()

	yes_FLIR = load_file('yes_FLIR')
	x,y = yes_FLIR
	pyg.moveTo(x,y,1)
	pyg.click()

	time.sleep(1)

	normal_image = load_file('normal_image')
	x,y = normal_image
	pyg.moveTo(x,y,1)
	pyg.click()

	rotate_step1 = load_file('rotate_step1')
	x,y = rotate_step1
	pyg.moveTo(x,y,1)
	pyg.click()

	rotate_step2 = load_file('rotate_step2')
	x,y = rotate_step2
	pyg.moveTo(x,y,0.5)
	pyg.click()

	rotate_step1 = load_file('rotate_step1')
	x,y = rotate_step1
	pyg.moveTo(x,y,0.5)
	pyg.click()

	rotate_step2 = load_file('rotate_step2')
	x,y = rotate_step2
	pyg.moveTo(x,y,0.5)
	pyg.click()

	# rotate_step1 = load_file('rotate_step1')
	# x,y = rotate_step1
	# pyg.moveTo(x,y,0.5)
	# pyg.click()

	# rotate_step2 = load_file('rotate_step2')
	# x,y = rotate_step2
	# pyg.moveTo(x,y,0.5)
	# pyg.click()

	# rotate_step1 = load_file('rotate_step1')
	# x,y = rotate_step1
	# pyg.moveTo(x,y,0.5)
	# pyg.click()

	# rotate_step2 = load_file('rotate_step2')
	# x,y = rotate_step2
	# pyg.moveTo(x,y,0.5)
	# pyg.click()

	find_marker = load_file('find_marker_FLIR7293')
	x,y = find_marker
	pyg.moveTo(x,y,2)
	
	start_pos = load_file('start_pos_FLIR7293')
	x,y = start_pos
	pyg.dragTo(x,y,3)


def enhance_image(img):
	(thresh, bwimage) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
	return bwimage

def main():
	#Configuration for tesseract OCR
	config = ('-l eng --oem 1 --psm 7')
	# grid_box_reply = False
	# img_box_reply = False

	grid_box_reply = yes_or_no("Do you want to select corners of the grid?")
	if grid_box_reply == True:
		grid_TLC,grid_TRC,grid_BRC,grid_BLC = select_corner("grid")
		grid_box_matrix = np.array([grid_TLC,grid_TRC,grid_BRC,grid_BLC])

		grid_box_name = input("Enter the name of the file you want to save as: ")
		save_file(grid_box_matrix,grid_box_name)
		gx1,gy1 = grid_TLC
		gx2,gy2 = grid_TRC
		gx3,gy3 = grid_BRC
		gx4,gy4 = grid_BLC
	else:
		# grid_box_name = input("Enter the name of the file without extension: ")
		# grid_box_name = grid_box_name + ".txt"
		grid_box_name = 'grid_FLIR7293.txt'
		grid_box_matrix = np.loadtxt(open(grid_box_name,"rb"),delimiter=",",skiprows=0)
		grid_TLC = grid_box_matrix[0,:]
		grid_TRC = grid_box_matrix[1,:]
		grid_BRC = grid_box_matrix[2,:]
		grid_BLC = grid_box_matrix[3,:]
		gx1,gy1 = grid_TLC
		gx2,gy2 = grid_TRC
		gx3,gy3 = grid_BRC
		gx4,gy4 = grid_BLC
	
	img_box_reply = yes_or_no("\nDo you want to select corners of the image box?")
	if img_box_reply == True:
		img_box_TLC,img_box_TRC,img_box_BRC,img_box_BLC = select_corner("image_box")
		img_box_matrix = np.array([img_box_TLC,img_box_TRC,img_box_BRC,img_box_BLC])
		
		image_box_name = input("\nEnter the name of the file you want to save as: ")
		save_file(img_box_matrix,image_box_name)
		x1,y1 = img_box_TLC
		x2,y2 = img_box_TRC
		x3,y3 = img_box_BRC
		x4,y4 = img_box_BLC
	else:
		# image_box_name = input("Enter the name of the file without extension: ")
		# image_box_name = image_box_name +".txt"
		image_box_name = "image_FLIR6421.txt"
		image_box_matrix = np.loadtxt(open(image_box_name,"rb"),delimiter=",",skiprows=0)
		img_box_TLC = image_box_matrix[0,:]
		img_box_TRC = image_box_matrix[1,:]
		img_box_BRC = image_box_matrix[2,:]
		img_box_BLC = image_box_matrix[3,:]
		x1,y1 = img_box_TLC
		x2,y2 = img_box_TRC
		x3,y3 = img_box_BRC
		x4,y4 = img_box_BLC
	
	# img = get_image(x1,y1,x3,y3)
	# img = cv2.bitwise_not(img)
	# bwimage = enhance_image(img)
	# img = imutils.resize(img,width=45,height=100)
	# bwimage = imutils.resize(bwimage,width=45,height=100)
	# # cv2.imshow("inverted",img)
	# # cv2.imshow("b&w",bwimage)
	# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
	# O = pytesseract.image_to_string(img)
	# A = pytesseract.image_to_string(img,config=config)
	# B = pytesseract.image_to_string(bwimage,config=config)
	# format_string(O)
	# format_string(A)
	# format_string(B)
	# print("hello")

	# # name = input("What's the name of the file? ")
	# go_to_next()
	start_pos = start_position()
	
	file = 7293

	while not file == 7393:
		A = np.zeros([7,11])
		height , width = A.shape
		i = 0
		j = 0
		dx_horizontal = (gx2-gx1)/(width-1)
		dy_horizontal = (gy2-gy1)/(width-1)
		dx_vertical = (gx4-gx1)/(height-1)
		dy_vertical = (gy4-gy1)/(height-1)
		name = 'FLIR'+ str(file)+'_mat'
		
		while i < height:
			while j < width:
				# start = False
				# while start == False:
					# start = yes_or_no("\nAre you ready to collect data for segment#(%i,%i)?" %(i,j))
				
				time.sleep(2)	
				img = get_image(x1,y1,x3,y3)
				img = cv2.bitwise_not(img)
				# img = enhance_image(img)
				img = imutils.resize(img,width=45,height=100)
				pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
				str1 = pytesseract.image_to_string(img,config=config)
				print(str1)	
				A[i,j] = format_string(str1)

				correct = False
				temp_move = 0
				while not correct:
					if A[i,j]<15 or A[i,j] > 150:
						pyg.dragRel(1,0,1)
						img = get_image(x1,y1,x3,y3)
						img = cv2.bitwise_not(img)
						img = enhance_image(img)
						img = imutils.resize(img,width=45,height=100)
						pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
						str1 = pytesseract.image_to_string(img,config=config)
						print(str1)
						A[i,j] = format_string(str1)
						temp_move = temp_move+1
					else:
						correct = True
						pyg.dragRel(-temp_move,0,1)

				print(A)
			
				if i == 0 and j == 0:
					# name = input("What's the name of the file? ")
					save_file(A,name)
					j = j + 1
					pyg.dragRel(dx_horizontal,dy_horizontal,1)
					time.sleep(1)
				else:
					save_file(A,name)
					j = j + 1
					if not j == width:
						pyg.dragRel(dx_horizontal,dy_horizontal,1)
						# print(A)
						time.sleep(1)
						
				if j == width:
					j = 0
					i = i + 1
					if not i == height:
						pyg.dragTo(start_pos[0],start_pos[1],4)
						pyg.dragRel(i*dx_vertical,i*dy_vertical,2)
						time.sleep(1)
					else:
						break	
					
			if i == height:
				# pyg.dragTo(start_pos[0],start_pos[1],4)
				# print("\nThank you. Your job is done.")
				# break
				file = file + 2
				go_to_next()
				break

					
			
if __name__ == '__main__':
	main()
	
cv2.waitKey(0)	