# coding: UTF-8
import numpy as np
import random as rnd

ERROR = -2
GAMEOVER = -1
CONTINUE = 0
CLEAR = 1

dps = (
		(-1, -1), ( 0, -1), ( 1, -1),
		(-1,  0),           ( 1,  0),
		(-1,  1), ( 0,  1), ( 1,  1),
	)

class Cell(object):
	def __init__(self, mine):
		self.mine = mine
		self.flug = self.visible = False
		self.number = -1

	def val(self):
		if self.mine and self.visible and not self.flug:
			return GAMEOVER

		return CONTINUE

	def str(self, ignore = False):
		if not ignore and not self.visible:
			return "?"

		elif self.flug:
			return "F"

		elif self.mine:
			return "x"

		elif self.number == 0:
			return "."

		else:
			return str(self.number)

class MineSweeper(object):
	def __init__(self, H = 5, W = 5, maxOfMine = 5):
		self.H = H
		self.W = W
		self.numOfMines = maxOfMine
		self.maxMines   = maxOfMine
		self.numOfOpen  = 0
		cells = []
		for i in range(self.numOfMines):
			cells.append(Cell(True))
		for i in range(self.H * self.W - self.numOfMines):
			cells.append(Cell(False))

		rnd.shuffle(cells)
		self.board = np.array(cells).reshape( (self.H, self.W) )
		self.setNumber()

	def setNumber(self):
		for h in range(self.H):
			for w in range(self.W):
				self.board[h][w].number = self.countNumOfMines(w, h)

	def controller(self, op, x, y):
		if not self.innerPoint(x, y):
			return ERROR

		if op == "f" or op == "F":
			if self.board[y][x].flug:
				self.board[y][x].visible = False
				self.board[y][x].flug = False
				self.numOfMines += 1

			elif self.board[y][x].visible:
				pass

			else:
				self.board[y][x].visible = True
				self.board[y][x].flug = True
				self.numOfMines -= 1

			return CONTINUE

		elif op == "o" or op == "O":
			return GAMEOVER if not self.recursiveOpen(x, y, True) else self.clear()

		return ERROR

	def clear(self):
		if not self.numOfOpen == self.H * self.W - self.maxMines:
			return CONTINUE

		for h in range(self.H):
			for w in range(self.W):
				if self.board[h][w].val() == GAMEOVER:
					return GAMEOVER 

		return CLEAR

	def countNumOfMines(self, x, y):
		count = 0
		for dp in dps:
			(nx, ny) = (x + dp[0], y + dp[1])
			if not self.innerPoint(nx, ny):
				continue

			if self.board[ny][nx].mine:
				count += 1

			if self.board[ny][nx].flug:
				count -= 1

		return count

	def innerPoint(self, x, y):
		return 0 <= x < self.W and 0 <= y < self.H

	def recursiveOpen(self, x, y, first = False):
		if self.board[y][x].flug:
			return True

		if not first and self.board[y][x].visible:
			return True

		if self.board[y][x].mine:
			return False

		if not self.board[y][x].visible:
			self.numOfOpen += 1
		self.board[y][x].visible = True

		if self.countNumOfMines(x, y) == 0:
			for p in dps:
				(nx, ny) = (x + p[0], y + p[1])
				if not self.innerPoint(nx, ny):
					continue

				if not self.recursiveOpen(nx, ny):
					return False

		return True

	def printBoard(self, ignore = False):
		print 
		print u"地雷の数: 残り%d" % (self.numOfMines)
		print "   " + " ".join(map(lambda x : chr(ord("a") + x), range(self.W)))
		for (i, row) in enumerate(self.board):
			print "%2d " % (i + 1) + " ".join(map(lambda x : x.str(ignore), row))

		print 

class Game(object):
	def __init__(self):
		self.minesweeper = MineSweeper()

	def menu(self):
		print u"サイズを入力してください(26×26まで)"
		print u"例）5×5のフィールドに５個の地雷を埋める： 5 5 5"
		(H, W, mines) =  raw_input().strip().split(" ")[:3]

		while not self.checkSize(H, W, mines):
			print u"正しいサイズを入力してください"
			(H, W, mines) =  raw_input().strip().split(" ")[:3]

		self.minesweeper = MineSweeper(int(H), int(W), int(mines))
		self.play()

	def checkSize(self, H, W, mines):
		if not H.isdigit() or not W.isdigit() or not mines.isdigit():
			return False

		if 1 <= int(H) <= 26 and 1 <= int(W) <= 26:
			if not (1 <= int(mines) <= int(H) * int(W)):
				return False

		return True

	def play(self):
		state = CONTINUE
		print u"ゲーム開始！！"
		while (state == CONTINUE or state == ERROR):
			if state != ERROR:
				self.minesweeper.printBoard()
			
			print u"コマンドを入力してください"
			print u"例）1-aを開ける      ： o 1 a"
			print u"例）1-aをチェックする： f 1 a"

			(op, x, y) = raw_input().strip().split(" ")[:3]
			(x, y) = self.convertInput(x, y)

			state = self.minesweeper.controller(op, x, y)

			if state == ERROR:
				print u"入力が正しくありません"

		if state == CLEAR:
			print u"クリア！"

		else:
			print u"ゲームオーバー..."

		self.minesweeper.printBoard(True)

	def convertInput(self, x, y):
		if x.isdigit() and y.isalpha():
			return self.convertInput(y, x)

		if not x.isalpha() or not y.isdigit():
			return (-1, -1)
		
		return (ord(x) - ord("a"), int(y) - 1)



if __name__ == '__main__':
	Game().menu()
