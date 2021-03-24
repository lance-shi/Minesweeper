from tkinter import *

class Image:
	def __init__(self):
		self.plain = PhotoImage(file = "images/tile_plain.gif")
		self.sunny = PhotoImage(file = "images/smiley.png")
		self.clicked = PhotoImage(file = "images/tile_clicked.gif")
		self.mine = PhotoImage(file = "images/tile_mine.gif")
		self.flag = PhotoImage(file = "images/tile_flag.gif")
		self.wrong = PhotoImage(file = "images/tile_wrong.gif")
		self.numbers = []

		for i in range(1, 9):
			self.numbers.append(PhotoImage(file = "images/tile_"+str(i)+".gif"))