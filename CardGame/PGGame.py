# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 09:20:17 2021

Game.py

@author: onodera
"""

import sys
import pygame
from pygame.locals import *
from PGCard import Card, Type
import random

class Button:
	def __init__(self, pos, size, color, textcolor, command, text, width, height):
		self.x = pos[0]
		self.y = pos[1]
		self.color = color
		self.command = command
		self.font = pygame.font.SysFont(None, size)
		self.text = self.font.render(text, True, textcolor)
		self.button = Rect(pos, (width, height))
		self.button_bottom = Rect(pos, (self.button.width, self.button.height + 5))
	def update(self, event):
		self.button.top = self.y
		if self.button.collidepoint(event.pos):
			self.button.top += 2
			self.command()
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.button)
		pygame.draw.rect(screen, (0, 0, 0), self.button, 1)
		screen.blit(self.text, (self.x + (self.button.width - self.text.get_width()) / 2, self.y + (self.button.height - self.text.get_height()) / 2))

class Game:
	"""
		ゲームクラス（抽象クラス）
	"""
	def __init__(self, title='', width=450, height=300):
		"""
		コンストラクタ

		Parameters
		----------
		title : string, 省略可能
			フレームのタイトル. 省略時: ''
		width : int, 省略可能
			フレームの幅. 省略時: 450
		height : int, 省略可能
			フレームの高さ. 省略時: 300

		Returns
		-------
		None.

		"""
		self.game = None
		pygame.display.set_caption(title)
		self.screen = pygame.display.set_mode((width, height))
		self.button = []
		self.button.append(Button((0, 0), 16, (192, 192, 192), (0, 0, 0), self.restartFunc, 'Restart', width, 20))
		self.button.append(Button((0, 20), 16, (192, 192, 192), (0, 0, 0), self.menuFunc, 'Menu', width, 20))
		self.init()
		self.paint()
	def restartFunc(self):
		"""
		リスタートボタン押下時の処理関数

		Returns
		-------
		None.

		"""
		self.init()
		self.paint()
	def menuFunc(self):
		"""
		メニューボタン押下時の処理関数

		Returns
		-------
		None.

		"""
		self.game = MasterFrame()
	def pop(self):
		"""
		山札から１枚取り出す

		Returns
		-------
		Card
			山札から取り除いたカード.

		"""
		return self.yamafuda.pop(0)
	def exist(self):
		"""
		山札に残り札があるか否かを返す

		Returns
		-------
		bool
			山札に残り札がある(True).

		"""
		return len(self.yamafuda) > 0
	def paint(self):
		"""
		描画する（抽象メソッド）

		Parameters
		----------
		None.
		
		Returns
		-------
		None.

		"""
		pass
	def init(self):
		"""
		ゲームの初期化（山札のシャッフル）

		Returns
		-------
		None.

		"""
		self.yamafuda = []
		for i in range(52):
			self.yamafuda.append(Card.getByid(i))
		random.shuffle(self.yamafuda)
	def click(self, x, y):
		"""
		マウスクリックイベント処理（抽象メソッド）

		Parameters
		----------
		x : int
			マウスクリック座標x.
		y : int
			マウスクリック座標y.

		Returns
		-------
		None.

		"""
		pass
	
	def mouse(self, event):
		"""
		マウスクリック時のイベント処理関数

		Parameters
		----------
		event : TYPE
			DESCRIPTION.

		Returns
		-------
		None.

		"""
		self.click(event.pos[0], event.pos[1]-40)
		self.paint()
	
	def play(self):
		clock = pygame.time.Clock()
		while True:
			clock.tick(30)
			self.screen.fill((255, 255, 255))
			for event in pygame.event.get():
				if event.type == QUIT:
					return None
				if event.type == MOUSEBUTTONDOWN:
					self.mouse(event)
					for button in self.button:
						button.update(event)
			for button in self.button:
				button.draw(self.screen)
			self.paint()
			if self.game != None:
				return self.game
			pygame.display.update()
			
	def blit(self, screen, x, y):
		self.screen.blit(screen, (x, y+40))
		
	def drawRect(self, color, rect, width=None):
		if width is None:
			pygame.draw.rect(self.screen, color, Rect(rect.left, rect.top+40, rect.width, rect.height))
		else:
			pygame.draw.rect(self.screen, color, Rect(rect.left, rect.top+40, rect.width, rect.height), width)
	
class MonteCarlo(Game):
	"""
		モンテカルロクラス（ゲームクラスを継承）
	"""
	def __init__(self):
		"""
		コンストラクタ

		Parameters
		----------

		Returns
		-------
		None.

		"""
		super(MonteCarlo, self).__init__("MonteCarlo", 440, 690)
	def init(self):
		"""
		ゲームの初期化

		Returns
		-------
		None.

		"""
		super(MonteCarlo, self).init()
		self.bafuda = []
		for i in range(25):
			self.bafuda.append(self.pop())
		self.selected = -1
	def click(self, x, y):
		"""
		マウスクリックイベント処理

		Parameters
		----------
		x : int
			マウスクリック座標x.
		y : TYPE
			マウスクリック座標y.

		Returns
		-------
		None.

		"""
		CardWidth, CardHeight = Card.Dimensions(0)
		if x >= 15 and x < 15 + CardWidth * 5 and \
			y >= 10 and y < 10 + CardHeight * 5:
			cx = (x - 15) // CardWidth
			cy = (y - 10) // CardHeight
			i = cy * 5 + cx
			if i >= len(self.bafuda):
				return
			if self.selected >= 0:
				sx = self.selected % 5
				sy = self.selected // 5
				if self.selected != i and \
					abs(cx - sx) <= 1 and abs(cy - sy) <= 1 and \
					self.bafuda[i].getNumber() == self.bafuda[self.selected].getNumber():
					c = self.bafuda[i]
					s = self.bafuda[self.selected]
					self.bafuda.remove(c)
					self.bafuda.remove(s)
					if self.exist():
						self.bafuda.append(self.pop())
					if self.exist():
						self.bafuda.append(self.pop())
				self.selected = -1
			else:
				self.selected = i
					
	def paint(self):
		"""
		場札を描画する

		Parameters
		----------
		screen 描画スクリーン

		Returns
		-------
		None.

		"""
		if len(self.bafuda) == 0:
			font = pygame.font.SysFont(None, 48)
			text = font.render("Congratulations!!", True, (0,0,0))
			self.blit(text, 70, 350)
		else:
			CardWidth, CardHeight = Card.Dimensions(0)
			for i in range(len(self.bafuda)):
				x = (i % 5) * CardWidth + 15
				y = (i // 5) * CardHeight + 10
				self.blit(self.bafuda[i].getImage(0), x, y)
				if i == self.selected:
					self.drawRect((255, 0, 0), Rect((x, y), (CardWidth, CardHeight)), 1)

class Golf(Game):
	"""
		ゴルフクラス（ゲームクラスを継承）
	"""
	def __init__(self):
		"""
		コンストラクタ

		Parameters
		----------

		Returns
		-------
		None.

		"""
		super(Golf, self).__init__("Golf", 600, 830)
	class Node:
		"""
			場札管理クラス
		"""
		def __init__(self, nodes=None, card=Card.NONE, i=-1, x=-1, y=-1):
			"""
			コンストラクタ

			Parameters
			----------
			nodes : Node[], 省略可能
				場札リスト. 省略時: None
			card : Card, 省略可能
				場札のカード. 省略時: Card.NONE（裏面）
			i : int, 省略可能
				場札番号（描画位置）. 省略時: -1
			x : int, 省略可能
				描画位置x. 省略時: -1
			y : int, 省略可能
				描画位置y. 省略時: -1

			Returns
			-------
			None.

			"""
			CardWidth, CardHeight = Card.Dimensions(0)
			if nodes is None:
				self.next = None
				self.left = x
				self.top = y
			else:
				if i < 7:
					self.next = None
				else:
					self.next = nodes[i-7] 
				self.left = (i % 7) * CardWidth + 13 
				self.top = (i // 7) * CardHeight + 20			   
			self.right = self.left + CardWidth
			self.bottom = self.top + CardHeight
			self.card = card
		def intersect(self, x, y):
			"""
			場札がマウスクリック座標に合致しているか否かを返す

			Parameters
			----------
			x : int
				マウスクリック座標x
			y : int
				マウスクリック座標y

			Returns
			-------
			bool
				マウスクリック座標に場札が合致している(True)

			"""
			return x >= self.left and x < self.right and \
				y >= self.top and y < self.bottom
		def paint(self, game):
			"""
			場札を描画する

			Parameters
			----------
			screen 描画スクリーン

			Returns
			-------
			None.

			"""
			game.blit(self.card.getImage(0), self.left, self.top)
		def getCard(self):
			"""
			場札のカードを返す

			Returns
			-------
			Card
				場札のカード

			"""
			return self.card
		def getNext(self):
			"""
			場札の次の有効な場札を返す

			Returns
			-------
			Node
				次の場札（なければNONE）

			"""
			return self.next
		def __str__(self):
			"""
			場札のカード名称を返す

			Returns
			-------
			string
				場札のカード名称

			"""
			return str(self.card)
		
	def init(self):
		"""
		ゲームの初期化

		Returns
		-------
		None.

		"""
		super(Golf, self).init()
		self.bafuda = []
		self.torifuda = []
		for i in range(35):
			if i < 28:
				self.bafuda.append(Golf.Node(self.bafuda, self.pop(), i))
			else:
				self.torifuda.append(Golf.Node(self.bafuda, self.pop(), i))
		self.torifuda.append(Golf.Node(x=13, y=635))
		self.daifuda = None
		
	def click(self, x, y):
		"""
		マウスクリック時の処理

		Parameters
		----------
		x : int
			マウスクリック座標x
		y : int
			マウスクリック座標y

		Returns
		-------
		None.

		"""
		select = None
		for node in self.torifuda:
			if node.intersect(x, y):
				select = node
				break
		if select is None:
			return
		if select.getCard() == Card.NONE:
			self.daifuda = self.pop()
			if not self.exist():
				self.torifuda.remove(select)
		elif self.daifuda is not None and \
			abs(select.getCard().getNumber() - self.daifuda.getNumber()) == 1 or \
			abs(select.getCard().getNumber() - self.daifuda.getNumber()) == 12:
			self.torifuda.remove(select)
			next = select.getNext()
			if next is not None:
				self.torifuda.append(next)
				self.bafuda.remove(next)
			self.daifuda = select.getCard()

	def paint(self):
		"""
		描画関数

		Parameters
		----------
		None.

		Returns
		-------
		None.

		"""
		for node in self.bafuda + self.torifuda:
			node.paint(self)
		if self.daifuda is not None:
			self.blit(self.daifuda.getImage(0), 177, 635)
		if len(self.torifuda) == 0 or \
			(len(self.torifuda) == 1 and self.torifuda[0].getCard() == Card.NONE):
			font = pygame.font.SysFont(None, 48)
			text = font.render("Congratulations!!", True, (0, 0, 0))
			self.blit(text, 150, 350)
			
class Pyramid(Game):
	"""
		ピラミッドクラス（ゲームクラスを継承）
	"""
	class Node:
		"""
			場札管理クラス
		"""
		def __init__(self, parent, child, card, x, y):
			"""
			コンストラクタ

			Parameters
			----------
			parent : Node
				親札（隠している場札）
			child : int
				子札（隠されている場札）の数
			card : Card
				場札のカード
			x : int
				場札の座標x
			y : int
				場札の座標y

			Returns
			-------
			None.

			"""
			CardWidth, CardHeight = Card.Dimensions(0)
			self.parent = parent
			self.child = child
			self.card = card
			self.left = x
			self.right = x + CardWidth
			self.top = y
			self.bottom = y + CardHeight
		def getCard(self):
			"""
			場札のカードを返す

			Returns
			-------
			Card
				場札のカード

			"""
			return self.card
		def isShow(self):
			"""
			表示するか否か（子札で隠されているかいなか）を返す

			Returns
			-------
			bool
				表示する（子札で隠されていない）:True

			"""
			return self.child == 0
		def rmChild(self):
			"""
			隠している子札の数を減らす

			Returns
			-------
			None.

			"""
			self.child -= 1
		def getParent(self):
			"""
			隠している親札を返す

			Returns
			-------
			Node
				親札（隠している場札、なければNone）

			"""
			return self.parent
		def intersect(self, x, y):
			"""
			場札がマウスクリック座標に合致しているか否かを返す

			Parameters
			----------
			x : int
				マウスクリック座標x
			y : int
				マウスクリック座標y

			Returns
			-------
			bool
				マウスクリック座標に場札が合致している(True)

			"""
			return self.left <= x and x < self.right and \
				self.top <= y and y < self.bottom
	inittbl = (
		(-1, -1, 2, 259, 20), (0, -1, 2, 218, 80), (0, -1, 2, 300, 80), (1, -1, 2, 177, 140),
		(1, 2, 2, 259, 140), (2, -1, 2, 341, 140), (3, -1, 2, 136, 200), (3, 4, 2, 218, 200),
		(4, 5, 2, 300, 200), (5, -1, 2, 382, 200), (6, -1, 2, 95, 260), (6, 7, 2, 177, 260),
		(7, 8, 2, 259, 260), (8, 9, 2, 341, 260), (9, -1, 2, 423, 260), (10, -1, 2, 54, 320),
		(10, 11, 2, 136, 320), (11, 12, 2, 218, 320), (12, 13, 2, 300, 320), (13, 14, 2, 382, 320),
		(14, -1, 2, 464, 320), (15, -1, 0, 13, 380), (15, 16, 0, 95, 380), (16, 17, 0, 177, 380),
		(17, 18, 0, 259, 380), (18, 19, 0, 341, 380), (19, 20, 0, 423, 380), (20, -1, 0, 505, 380))
	def __init__(self):
		"""
		コンストラクタ

		Parameters
		----------
		Returns
		-------
		None.

		"""
		super(Pyramid, self).__init__("Pyramid", 630, 720)
	def init(self):
		"""
		ゲームの初期化

		Returns
		-------
		None.

		"""
		super(Pyramid, self).init()
		self.sutefuda = []
		self.bafuda = []
		self.misefuda = []
		for i in range(len(Pyramid.inittbl)):
			parent = []
			for j in range(2):
				k = Pyramid.inittbl[i][j]
				if k < 0:
					break
				parent.append(self.bafuda[k])
			node = Pyramid.Node(parent, Pyramid.inittbl[i][2], self.pop(), Pyramid.inittbl[i][3], Pyramid.inittbl[i][4])
			if Pyramid.inittbl[i][2] == 0:
				self.misefuda.append(node)
			else:
				self.bafuda.append(node)
		self.lastNode = self.bafuda[0]
		self.misefuda.append(Pyramid.Node(None, 0, Card.NONE, 177, 520))
		self.selected = None
	def rmNode(self, select):
		"""
		指定した場札を削除する

		Parameters
		----------
		select : Node
			指定した場札.

		Returns
		-------
		None.

		"""
		if select.getParent() is None:
			self.sutefuda.remove(select.getCard())
			self.misefuda.remove(select)
			if len(self.sutefuda) > 0:
				self.misefuda.append(Pyramid.Node(None, 0, self.sutefuda[0], 341, 520))
		else:
			self.misefuda.remove(select)
			for node in select.getParent():
				node.rmChild()
				if node.isShow():
					self.misefuda.append(node)
					self.bafuda.remove(node)
	def click(self, x, y):
		"""
		マウスクリック時の処理関数

		Parameters
		----------
		x : int
			マウスクリック座標x
		y : int
			マウスクリック座標y

		Returns
		-------
		None.

		"""
		select = None
		for node in self.misefuda:
			if node.intersect(x, y):
				select = node
				break
		if select is None:
			return
		if select.getCard() == Card.NONE:
			if len(self.sutefuda) > 0:
				node = [n for n in self.misefuda if n.getCard() == self.sutefuda[0]][0]
				self.misefuda.remove(node)
			card = self.pop()
			self.misefuda.append(Pyramid.Node(None, 0, card, 341, 520))
			self.sutefuda.insert(0, card)
			if not self.exist():
				self.misefuda.remove(select)
			self.selected = None
		elif select.getCard().getNumber() == 13:
			self.rmNode(select)
		elif self.selected is not None:
			if select.getCard().getNumber() + self.selected.getCard().getNumber() == 13:
				self.rmNode(select)
				self.rmNode(self.selected)
			self.selected = None
		else:
			self.selected = select
			
	def paint(self):
		"""
		描画関数

		Parameters
		----------
		None.

		Returns
		-------
		None.

		"""
		if self.lastNode not in self.bafuda + self.misefuda:
			font = pygame.font.SysFont(None, 48)
			text = font.render("Congratulations!!", True, (0, 0, 0))
			self.blit(text, 150, 350)
			return
		for node in self.bafuda:
			self.blit(Card.NONE.getImage(0), node.left, node.top)
		for node in self.misefuda:
			self.blit(node.getCard().getImage(0), node.left, node.top)
			if node == self.selected:
				self.drawRect((255, 0, 0), Rect(node.left, node.top, node.right-node.left, node.bottom-node.top), 1)
	  
class Couple(Game):
	"""
		カップルクラス（ゲームクラスを継承）
	"""
	def __init__(self):
		"""
		コンストラクタ

		Parameters
		----------

		Returns
		-------
		None.

		"""
		super(Couple, self).__init__("Couple", 375, 1000)
	def init(self):
		"""
		ゲームの初期化

		Returns
		-------
		None.

		"""
		super(Couple, self).init()
		self.bafuda = []
		self.select = -1
		self.message = None
	def click(self, x, y):
		"""
		マウスクリック時の処理関数

		Parameters
		----------
		x : int
			マウスクリック座標x
		y : int
			マウスクリック座標y

		Returns
		-------
		None.

		"""
		if self.exist() and x >= 280 and x < 341 and y >= 10 and y < 100:
			self.select = -1
			card = self.pop()
			self.bafuda.append(card)
		elif x >= 20 and x < 264 and y >= 10:
			i = ((y - 10) // 90) * 4 + (x - 20) // 61
			if i >= 0 and i < len(self.bafuda):
				if self.select < 0:
					self.select = i
				elif self.select != i:
					diffx = abs((self.select % 4) - (i % 4))
					diffy = abs((self.select // 4) - (i // 4))
					if diffx <= 1 and diffy <= 1 and \
						self.bafuda[i].getNumber() == self.bafuda[self.select].getNumber():
						c0, c1 = self.bafuda[i], self.bafuda[self.select]
						self.bafuda.remove(c0)
						self.bafuda.remove(c1)
						self.select = -1
					else:
						self.select = i
				else:
					self.select = -1
			else:
				if not self.exist():
					if len(self.bafuda) == 0:
						self.message = "Congratulations!!"
					else:
						self.message = "Game Over!!"
				self.select = -1
		else:
			if not self.exist():
				if len(self.bafuda) == 0:
					self.message = "Congratulations!!"
				else:
					self.message = "Game Over!!"
			self.select = -1
	def paint(self):
		"""
		描画処理関数

		Parameters
		----------
		None.

		Returns
		-------
		None.

		"""
		if self.exist():
			self.blit(Card.NONE.getImage(1), 280, 10)
		for i in range(len(self.bafuda)):
			y = (i // 4) * 90 + 10
			x = (i % 4) * 61 + 20
			self.blit(self.bafuda[i].getImage(1), x, y)
		if self.select >= 0:
			y = (self.select // 4) * 90 + 10
			x = (self.select % 4) * 61 + 20
			self.drawRect((255, 0, 0), Rect(x, y, 61, 90), 1)
		if self.message is not None:
			y = ((len(self.bafuda) + 3) // 4) * 90 + 40
			font = pygame.font.SysFont(None, 48)
			text = font.render(self.message, True, (0, 0, 0))
			self.blit(text, 70, 350)

class FourLeafClover(Game):
	"""
		四葉のクローバークラス（ゲームクラスを継承）
	"""
	def __init__(self):
		"""
		コンストラクタ

		Parameters
		----------

		Returns
		-------
		None.

		"""
		super(FourLeafClover, self).__init__("Four Leaf Clover", 358, 570)
	def init(self):
		"""
		ゲームの初期化

		Returns
		-------
		None.

		"""
		self.yamafuda = []
		for i in range(52):
			card = Card.getByid(i)
			if card.getNumber() != 10:
				self.yamafuda.append(card)
		random.shuffle(self.yamafuda)
		self.bafuda = [None] * 16
		for i in range(16):
			self.bafuda[i] = self.pop()
		self.selected = []
		self.selectedType = Type.NONE
		self.selectedSum = 0
	def click(self, x, y):
		"""
		マウスクリックイベント処理

		Parameters
		----------
		x : int
			マウスクリック座標x.
		y : TYPE
			マウスクリック座標y.

		Returns
		-------
		None.

		"""
		CardWidth, CardHeight = Card.Dimensions(0)
		if x >= 15 and x < 15 + CardWidth * 4 and \
			y >= 10 and y < 10 + CardHeight * 4:
			cx = (x - 15) // CardWidth
			cy = (y - 10) // CardHeight
			i = cy * 4 + cx
			if i >= len(self.bafuda) or self.bafuda[i] == None:
				return
			if i in self.selected:
				self.selected.remove(i)
				if len(self.selected) == 0:
					self.selectedType = Type.NONE
					self.selectedSum = 0
				elif self.selectedSum < 0:
					self.selectedSum += 1
				else:
					self.selectedSum -= self.bafuda[i].getNumber()
			elif len(self.selected) > 0 and \
				self.bafuda[i].getType() == self.selectedType and \
				(self.bafuda[i].getNumber() + self.selectedSum == 15 or \
				self.selectedSum == -2 and self.bafuda[i].getNumber() > 10):
				self.selected.append(i)
				for j in self.selected:
					if self.exist():
						self.bafuda[j] = self.pop()
					else:
						self.bafuda[j] = None
				self.selected.clear()
				self.selectedType = Type.NONE
				self.selectedSum = 0
			else:
				if self.selectedType == Type.NONE:
					self.selectedType = self.bafuda[i].getType()
				elif self.selectedType != self.bafuda[i].getType():
					return
				if self.bafuda[i].getNumber() > 10:
					if self.selectedSum > 0:
						return
					self.selectedSum -= 1
				elif self.bafuda[i].getNumber() + self.selectedSum > 15:
					return
				else:
					self.selectedSum += self.bafuda[i].getNumber()
				self.selected.append(i)
					
	def paint(self):
		"""
		場札を描画する

		Parameters
		----------
		screen 描画スクリーン

		Returns
		-------
		None.

		"""
		if all([i is None for i in self.bafuda]):
			font = pygame.font.SysFont(None, 48)
			text = font.render("Congratulations!!", True, (0,0,0))
			self.blit(text, 30, 290)
		else:
			CardWidth, CardHeight = Card.Dimensions(0)
			for i in range(16):
				if self.bafuda[i] is None:
					continue
				x = (i % 4) * CardWidth + 15
				y = (i // 4) * CardHeight + 10
				self.blit(self.bafuda[i].getImage(0), x, y)
				if i in self.selected:
					self.drawRect((255, 0, 0), Rect((x, y), (CardWidth, CardHeight)), 1)

			
class MasterFrame(Game):
	"""
		メニューフレーム
	"""
	def __init__(self, master=None):
		"""
		コンストラクタ

		Parameters
		----------
		master : tk.Tk, 省略可能
			描画トップレベル. 省略時: None

		Returns
		-------
		None.

		"""
		self.game = None
		pygame.display.set_caption("menu")
		self.screen = pygame.display.set_mode((450, 375))
		self.button = []
		self.button.append(Button((0, 0), 32, (192, 192, 192), (0, 0, 0), self.monteCarlo, 'MonteCarlo', 450, 75))
		self.button.append(Button((0,75), 32, (192, 192, 192), (0, 0, 0), self.golf, 'Golf', 450, 75))
		self.button.append(Button((0,150), 32, (192, 192, 192), (0, 0, 0),	self.pyramid, 'Pyramid', 450, 75))
		self.button.append(Button((0, 225), 32, (192, 192, 192), (0, 0, 0), self.couple, 'Couple', 450, 75))
		self.button.append(Button((0, 300), 32, (192, 192, 192), (0, 0, 0), self.fourLeafClover, 'Four Leaf Clover', 450, 75))
	def monteCarlo(self):
		"""
		モンテカルロボタン押下時の処理関数

		Returns
		-------
		None.

		"""
		self.game = MonteCarlo()
	def golf(self):
		"""
		ゴルフボタン押下時の処理関数

		Returns
		-------
		None.

		"""
		self.game = Golf()
	def pyramid(self):
		"""
		ピラミッドボタン押下時の処理関数

		Returns
		-------
		None.

		"""
		self.game = Pyramid()
	def couple(self):
		"""
		カップルボタン押下時の処理関数

		Returns
		-------
		None.

		"""
		self.game = Couple()
	def fourLeafClover(self):
		"""
		四葉のクローバーボタン押下時の処理関数

		Returns
		-------
		None.

		"""
		self.game = FourLeafClover()
					  
if __name__ == '__main__':
	pygame.init()
	Card.initImage()
	game = MasterFrame()
	while game is not None:
		game = game.play()
	pygame.quit()
	sys.exit(0)