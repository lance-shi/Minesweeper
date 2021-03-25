from tkinter import *
from tkinter import messagebox
from image import *
from tile import *

class Minesweeper:
	def __init__(self):
		self.SIZE_X = 9
		self.SIZE_Y = 9
		self.MINE_NUMBER = 10
		self.root = Tk()
		self.root.title("Minesweeper")
		self.images = Image()

		self.frame = Frame(self.root)
		self.frame.pack()

		self.labels = {
			"time": Label(self.frame, text = "00:00:00"),
			"mines": Label(self.frame, text = "Mines: 0"),
			"flags": Label(self.frame, text = "Flags: 0")
		}
		restartImage = self.images.sunny
		self.restartBtn = Button(self.frame, image=restartImage, height=20, width=20, command=self.restartGame)
		self.restartBtn.grid(row = 0, column = 4)

		self.labels["time"].grid(row = 1, column = 0, columnspan = self.SIZE_Y) # top full width
		self.labels["mines"].grid(row = self.SIZE_X+2, column = 0, columnspan = int(self.SIZE_Y/2)) # bottom left
		self.labels["flags"].grid(row = self.SIZE_X+2, column = int(self.SIZE_Y/2)-1, columnspan = int(self.SIZE_Y/2)) # bottom right

		self.setup()

		self.root.mainloop()

	def setup(self):
		self.tiles = Tiles(self.root, self.frame, self.images, self.labels, self.SIZE_X, self.SIZE_Y, self.MINE_NUMBER)

	def restartGame(self):
		self.tiles.setup()

def main():
	mainApp = Minesweeper()

if __name__ == "__main__":
	main()
