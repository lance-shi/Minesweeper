from tkinter import *
from tkinter import messagebox
import platform
import random

SIZE_X = 9
SIZE_Y = 9
MINE_NUMBER = 10

STATE_DEFAULT = 0
STATE_CLICKED = 1
STATE_FLAGGED = 2

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

class Minesweeper:
	def __init__(self):
		self.root = Tk()
		self.root.title("Minesweeper")
		self.images = {
			"plain": PhotoImage(file = "images/tile_plain.gif"),
			"sunny": PhotoImage(file = "images/smiley.png"),
			"clicked": PhotoImage(file = "images/tile_clicked.gif"),
			"mine": PhotoImage(file = "images/tile_mine.gif"),
			"flag": PhotoImage(file = "images/tile_flag.gif"),
			"wrong": PhotoImage(file = "images/tile_wrong.gif"),
			"numbers": []
		}
		for i in range(1, 9):
			self.images["numbers"].append(PhotoImage(file = "images/tile_"+str(i)+".gif"))

		self.frame = Frame(self.root)
		self.frame.pack()

		self.labels = {
			"time": Label(self.frame, text = "00:00:00"),
			"mines": Label(self.frame, text = "Mines: 0"),
			"flags": Label(self.frame, text = "Flags: 0")
		}
		restartImage = self.images["sunny"]
		self.restartBtn = Button(self.frame, image=restartImage, height=20, width=20)
		self.restartBtn.grid(row = 0, column = 4)

		self.labels["time"].grid(row = 1, column = 0, columnspan = SIZE_Y) # top full width
		self.labels["mines"].grid(row = SIZE_X+2, column = 0, columnspan = int(SIZE_Y/2)) # bottom left
		self.labels["flags"].grid(row = SIZE_X+2, column = int(SIZE_Y/2)-1, columnspan = int(SIZE_Y/2)) # bottom right

		self.restart()

		self.root.mainloop()

	def restart(self):
		self.setup()

	def setup(self):
		self.tiles = dict({})
		self.mines = MINE_NUMBER
		for x in range(0, SIZE_X):
			for y in range(0, SIZE_Y):
				if y == 0:
					self.tiles[x] = {}

				id = str(x) + "_" + str(y)
				isMine = False
				gfx = self.images["plain"]

				tile = {
					"id": id,
					"isMine": isMine,
					"state": STATE_DEFAULT,
					"coords": {
						"x": x,
						"y": y
					},
					"button": Button(self.frame, image = gfx, height=20, width=20),
					"mines": 0 # calculated after grid is built
				}

				tile["button"].grid( row = x+2, column = y ) # offset by 1 row for timer

				self.tiles[x][y] = tile

		mineList = random.sample(range(81), 10)
		for mine in mineList:
			x = mine // 9
			y = mine % 9
			self.tiles[x][y]["isMine"] = True

	def getNeighbors(self, x, y):
		neighbors = []
		coords = [
			{"x": x-1,  "y": y-1},  #top right
			{"x": x-1,  "y": y},    #top middle
			{"x": x-1,  "y": y+1},  #top left
			{"x": x,    "y": y-1},  #left
			{"x": x,    "y": y+1},  #right
			{"x": x+1,  "y": y-1},  #bottom right
			{"x": x+1,  "y": y},    #bottom middle
			{"x": x+1,  "y": y+1},  #bottom left
		]
		for n in coords:
			try:
				neighbors.append(self.tiles[n["x"]][n["y"]])
			except KeyError:
				pass
		return neighbors

def main():
	mainApp = Minesweeper()

if __name__ = "__main__":
	main()
