from tkinter import *
from tkinter import messagebox
from image import *
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime

class Tile:
	def __init__(self, frame, images, x, y, defaultState):
		self.id = str(x) + "_" + str(y)
		self.isMine = False
		self.state = defaultState
		self.coords = {
			"x": x,
			"y": y
		}
		self.frame = frame
		gfx = images.plain
		self.button = Button(self.frame, image = gfx, height=20, width=20)
		self.mines = 0

class Tiles:
	def __init__(self, root, frame, images, labels, sizeX, sizeY, mineNumber):
		self.STATE_DEFAULT = 0
		self.STATE_CLICKED = 1
		self.STATE_FLAGGED = 2

		self.BTN_CLICK = "<Button-1>"
		self.BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

		self.root = root
		self.frame = frame
		self.images = images
		self.sizeX = sizeX
		self.sizeY = sizeY
		self.mineNumber = mineNumber
		self.labels = labels

		self.setup()   

	def setup(self):
		self.flagCount = 0
		self.clickedCount = 0
		self.startTime = None
		self.gameEnded = False

		self.tiles = []
		for x in range(0, self.sizeX):
			for y in range(0, self.sizeY):
				if y == 0:
					self.tiles.append([])
				currentTile = Tile(self.frame, self.images, x, y, self.STATE_DEFAULT)
				currentTile.button.bind(self.BTN_CLICK, self.onClickWrapper(x, y))
				currentTile.button.bind(self.BTN_FLAG, self.onRightClickWrapper(x, y))
				currentTile.button.grid( row = x+2, column = y )
				self.tiles[x].append(currentTile)

		mineList = random.sample(range(self.sizeX * self.sizeY), self.mineNumber)
		for mine in mineList:
			x = mine // self.sizeX
			y = mine % self.sizeX
			self.tiles[x][y].isMine = True

		for x in range(0, self.sizeX):
			for y in range(0, self.sizeY):
				minesCount = 0
				for n in self.getNeighbors(x, y):
					minesCount += 1 if n.isMine else 0
				self.tiles[x][y].mines = minesCount

		self.refreshLabels()

	def refreshLabels(self):
		self.labels["flags"].config(text = "Flags: " + str(self.flagCount))
		self.labels["mines"].config(text = "Mines: " + str(self.mineNumber))

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
			if n["x"] >= 0 and n["x"] < self.sizeX and n["y"] >= 0 and n["y"] < self.sizeY:
				neighbors.append(self.tiles[n["x"]][n["y"]])
		return neighbors

	def onClickWrapper(self, x, y):
		return lambda Button: self.onClick(self.tiles[x][y])

	def onRightClickWrapper(self, x, y):
		return lambda Button: self.onRightClick(self.tiles[x][y])

	def onClick(self, tile):
		if self.startTime == None:
			self.startTime = datetime.now()
			self.updateTimer()

		if tile.state != self.STATE_DEFAULT:
			return

		if tile.isMine == True:
			self.gameOver(False)
			return

		if tile.mines == 0:
			tile.button.config(image = self.images.clicked)
			self.clearSurroundingTiles(tile.id)
		else:
			tile.button.config(image=self.images.numbers[tile.mines - 1])
		
		if tile.state != self.STATE_CLICKED:
			tile.state == self.STATE_CLICKED
			self.clickedCount += 1
		if self.clickedCount >= (self.sizeX * self.sizeY) - self.mineNumber:
			self.gameOver(True)

	def onRightClick(self, tile):
		if self.startTime == None:
			self.startTime = datetime.now()
			self.updateTimer()

		if tile.state == self.STATE_DEFAULT:
			tile.button.config(image = self.images.flag)
			tile.state = self.STATE_FLAGGED
			self.flagCount += 1
		elif tile.state == self.STATE_FLAGGED:
			tile.button.config(image = self.images.plain)
			tile.state = self.STATE_DEFAULT
			self.flagCount -= 1
		self.refreshLabels()

	def gameOver(self, won):
		self.gameEnded = True
		for x in range(0, self.sizeX):
			for y in range(0, self.sizeY):
				currentTile = self.tiles[x][y]
				if currentTile.isMine == False and currentTile.state == self.STATE_FLAGGED:
					currentTile.button.config(image = self.images.wrong)
				if currentTile.isMine == True and currentTile.state != self.STATE_FLAGGED:
					currentTile.button.config(image = self.images.mine)

		msg = "You Win! Play again?" if won else "You Lose! Play again?"
		res = messagebox.askyesno("Game Over", msg)
		if res:
			self.setup()
		else:
			self.root.quit()

	def clearSurroundingTiles(self, id):
		queue = deque([id])

		while len(queue) != 0:
			key = queue.popleft()
			parts = key.split("_")
			x = int(parts[0])
			y = int(parts[1])

			for tile in self.getNeighbors(x, y):
				self.clearTile(tile, queue)

	def clearTile(self, tile, queue):
		if tile.state != self.STATE_DEFAULT:
			return

		if tile.mines == 0:
			tile.button.config(image = self.images.clicked)
			queue.append(tile.id)
		else: 
			tile.button.config(image = self.images.numbers[tile.mines-1])

		tile.state = self.STATE_CLICKED
		self.clickedCount += 1 
	# either ways will work But I am wondering is this same logic as simply clicked? 

	def updateTimer(self):
		if self.startTime != None and self.gameEnded == False:
			delta = datetime.now() - self.startTime
			ts = str(delta).split('.')[0] # drop ms
			if delta.total_seconds() < 36000:
				ts = "0" + ts # zero-pad
			self.labels["time"].config(text = ts)
			self.frame.after(100, self.updateTimer)


