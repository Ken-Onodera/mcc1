import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import random

class Button:
	def __init__(self, size, fontsize):
		self.font = pygame.font.SysFont(None, fontsize)
		self.size = size
		self.visible = True
	def setName(self, name, color):
		self.name = name
		self.text = self.font.render(name, True, color)
		self.text_rect = self.text.get_rect()
	def setPos(self, x, y):
		self.rect = pygame.Rect(x * self.size, y * self.size, self.size-1, self.size-1)
	def show(self, surface):
		if self.visible:
			pygame.draw.rect(surface, (192, 192, 192), self.rect)
			pygame.draw.rect(surface, (0, 0, 0), self.rect, width=1)
			self.text_rect.center = self.rect.center
			surface.blit(self.text, self.text_rect.topleft)
			
class CustomButton(Button):
	def __init__(self, i):
		super().__init__(100, 40)
		self.isMovable = False
		self.setName(str(i+1), (0, 0, 0))
		self.setPos(i % 4, i // 4)
		self.position = i
	def collidepoint(self, x, y):
		return self.rect.collidepoint(x, y)
	def move(self, cb):
		if self.isMovable:
			self.position, cb.position = cb.position, self.position
			self.rect, cb.rect = cb.rect, self.rect
	def getPos(self):
		return (self.position % 4, self.position // 4)

class Game:
	def __init__(self, title, width, height):
		pygame.init()
		self.SURFACE = pygame.display.set_mode([width, height])
		pygame.display.set_caption(title)
		self.FPSCLOCK = pygame.time.Clock()
		self.myCustomButton = []
		self.randlist = []
		for i in range(15):
			self.myCustomButton.append(CustomButton(i))
		self.emptyButton = CustomButton(15)
		self.emptyButton.setName("OK", (0,0,0))
		self.init()
	def init(self):	
		self.emptyButton.visible = False
		self.setMovable()
		for i in range(100):
			random.choice(self.randlist).move(self.emptyButton)
			self.setMovable()
	def setMovable(self):
		self.randlist.clear()
		xeb, yeb = self.emptyButton.getPos()
		for button in self.myCustomButton:
			x, y = button.getPos()
			if (y == yeb and abs(x - xeb) == 1) or \
				(x == xeb and abs(y - yeb) == 1):
				button.isMovable = True
				self.randlist.append(button)
			else:
				button.isMovable = False
	def checkComplete(self):
		for button in self.myCustomButton:
			if button.name != str(button.position+1):
				return
		self.emptyButton.visible = True
	def button_click(self, x, y):
		for button in self.myCustomButton:
			if button.collidepoint(x, y):
				button.move(self.emptyButton)
				self.setMovable()
				self.checkComplete()
				return
		if self.emptyButton.visible:
			if self.emptyButton.collidepoint(x, y):
				self.init()
	def show(self):
		self.SURFACE.fill((255, 255, 255))
		for button in self.myCustomButton:
			button.show(self.SURFACE)
		self.emptyButton.show(self.SURFACE)
		pygame.display.update()
		self.FPSCLOCK.tick(15)

def main():
	game = Game("15 puzzle", 400, 400)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				x, y = event.pos
				game.button_click(x, y)
		game.show()

if __name__ == '__main__':
	main()
