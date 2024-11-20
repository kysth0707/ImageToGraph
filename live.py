from rgbchecker import RGBChecker
import cv2 as cv
from img2graph import convertImg
import numpy as np
# from arduinosender import ArduinoSender

from tkinter import *
import keyboard
from sys import platform
import time


SHOW_IMG_SHAPE = (600, 600)

# https://stackoverflow.com/questions/57742442/how-to-get-the-height-of-a-tkinter-window-title-bar
class BarHeight(Tk):
	def __init__(self):
		super().__init__()
		super().withdraw()
		Frame(self).update_idletasks()
		self.geometry('350x200+100+100')
		self.update_idletasks()

		offset_y = 0
		if platform in ('win32', 'darwin'):
			import ctypes
			try: # >= win 8.1
				ctypes.windll.shcore.SetProcessDpiAwareness(2)
			except: # win 8.0 or less
				ctypes.windll.user32.SetProcessDPIAware()
		offset_y = int(self.geometry().rsplit('+', 1)[-1])

		bar_height = self.winfo_rooty() - offset_y
		print(f'Height: {bar_height}\nPlatform: {platform}')
		self.destroy()
		return bar_height

# RGBCheckers = []
# RGBCheckerThreads = []

# def Checker(index, ScreenWidth, ScreenHeight, DotCount, ScreenPos, BarHeight):
# 	return RGBCheckers[index].GetPixelColorsByPIL(ScreenWidth, ScreenHeight, DotCount, ScreenPos, BarHeight)

class SelectorGUI(BarHeight, RGBChecker):
	root = None
	ExitFlag = False
	DotCount = 0
	Title = ""

	Dots = None

	ScreenPos = (0, 0)
	BarHeight = None
	ScreenWidth = 0
	ScreenHeight = 0

	# RGBCheckerLastTime = 0
	# RGBCheckerRepeatNum = 0

	def __init__(self, Width, Height, Title, DotCount) -> None:
		self.BarHeight = super().__init__()

		self.DotCount = DotCount
		
		self.ScreenWidth = Width
		self.ScreenHeight = Height
		self.Title = Title
		
		self.root = Tk()
		self.root.title(f"{self.Title} / {self.ScreenWidth} x {self.ScreenHeight}")
		self.root.geometry(f"{Width}x{Height}")
		self.root.resizable(True, True)

		# https://stackoverflow.com/questions/19080499/transparent-background-in-a-tkinter-window
		# 투명 배경
		self.root.image = PhotoImage(file='TransparentImage.png')
		label = Label(self.root, image = self.root.image, bg='white')
		self.root.geometry(f"{Width}x{Height}")
		self.root.wm_attributes("-topmost", True)
		self.root.wm_attributes("-transparentcolor", "white")
		label.pack()
		# =========================

		self.root.protocol("WM_DELETE_WINDOW", self.onClose)
		self.root.bind("<Configure>", self.onResize)
		

	def isAlive(self):
		if self.ExitFlag == True:
			return False
		else:
			return True

	def getDots(self):
		return self.Dots


	def onClose(self):
		self.ExitFlag = True
		self.root.destroy()

	def onResize(self, e):
		# if keyboard.is_pressed("left shift"):
		if self.ScreenWidth != self.root.winfo_width():
			# Width changed
			self.root.geometry(f"{self.root.winfo_width()}x{self.root.winfo_width()}")
			# self.root.resizable(True, True)

		elif self.ScreenHeight != self.root.winfo_height():
			# Height changed
			self.root.geometry(f"{self.root.winfo_height()}x{self.root.winfo_height()}")
			# self.root.resizable(True, True)

		elif self.ScreenWidth != self.root.winfo_width() and self.ScreenHeight != self.root.winfo_height():
			# Width / Height changed
			self.root.geometry(f"{self.root.winfo_height()}x{self.root.winfo_height()}")
			# self.root.resizable(True, True)

		self.ScreenWidth, self.ScreenHeight = self.root.winfo_width(), self.root.winfo_height()
		#self.root.title(f"{self.Title} / {self.ScreenWidth} x {self.ScreenHeight}")
		# return

	def update(self):
		lastTime = time.time()
		TempValue = self.root.winfo_geometry().split('+')
		self.ScreenPos = (int(TempValue[1]), int(TempValue[2]))
		
		self.Dots = super().GetPixelColorsByPIL(self.ScreenWidth, self.ScreenHeight, self.DotCount, self.ScreenPos, self.BarHeight)
		originalImg = self.Dots.copy().astype(np.uint8)
		showImg = originalImg.copy()
		graphImg = np.zeros(showImg.shape)
		
		# print(convertImg(originalImg))
		for graphDots in convertImg(originalImg):
			startPos = graphDots[0]
			for pos in graphDots[1:]:

				cv.line(showImg, startPos, pos, (255, 255, 255), 1)
				cv.line(graphImg, startPos, pos, (255, 255, 255), 1)
				startPos = pos

		cv.imshow('graph + image', cv.resize(showImg, SHOW_IMG_SHAPE)[:,:,::-1])
		cv.imshow('graph', cv.resize(graphImg, SHOW_IMG_SHAPE))

		self.root.title(f"{self.Title} / {self.ScreenWidth} x {self.ScreenHeight} / {round(1/(time.time() - lastTime), 2)} fps")
		
		self.root.update()


MyGUI = SelectorGUI(600, 600, "선택 창", 512)

while True:
	if not MyGUI.isAlive():
		break
	MyGUI.update()