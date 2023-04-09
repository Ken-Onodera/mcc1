import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import random

class Button:
	def __init__(self, image, i, size, fontsize):
		self.font = pygame.font.SysFont(None, fontsize)
		width, height = image.get_size()
		self.width = width // size
		self.height = height // size
		self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		self.image.blit(image, (0, 0), (self.width * (i % size), self.height * (i // size), width, height))
		self.visible = True
	def setName(self, name, overwrite = False):
		self.name = name
		if overwrite:
			self.text = self.font.render(name, True, (255, 0, 0))
			self.text_rect = self.text.get_rect()
		else:
			self.text = None
	def setPos(self, x, y):
		self.rect = pygame.Rect(x * self.width, y * self.height, self.width, self.height)
	def show(self, surface):
		if self.visible:
			surface.blit(self.image, self.rect.topleft)
#			pygame.draw.rect(surface, (255, 255, 255), self.rect, width=1)
			if self.text is not None:
				self.text_rect.center = self.rect.center
				surface.blit(self.text, self.text_rect.topleft)
			
class CustomButton(Button):
	def __init__(self, image, size, i):
		super().__init__(image, i, size, 40)
		self.size = size
		self.isMovable = False
		self.setName(str(i+1))
		self.setPos(i % self.size, i // self.size)
		self.position = i
	def collidepoint(self, x, y):
		return self.rect.collidepoint(x, y)
	def move(self, cb):
		if self.isMovable:
			self.position, cb.position = cb.position, self.position
			self.rect, cb.rect = cb.rect, self.rect
	def getPos(self):
		return (self.position % self.size, self.position // self.size)

class Game:
	def __init__(self, title, image, size, randcnt):
		width, height = image.get_size()
		self.randcnt = randcnt
		self.SURFACE = pygame.display.set_mode([width, height])
		pygame.display.set_caption(title)
		self.FPSCLOCK = pygame.time.Clock()
		self.myCustomButton = []
		self.randlist = []
		for i in range(size*size-1):
			self.myCustomButton.append(CustomButton(image, size, i))
		self.emptyButton = CustomButton(image, size, size*size-1)
		self.emptyButton.setName("Succeed", True)
		self.init()
	def init(self):	
		self.emptyButton.visible = False
		self.setMovable()
		for i in range(self.randcnt):
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
	if len(sys.argv) == 2:
		size = 4
		randcnt = 50
	elif len(sys.argv) == 3:
		size = int(sys.argv[2])
		randcnt = 50
	elif len(sys.argv) == 4:
		size = int(sys.argv[2])
		randcnt = int(sys.argv[3])
	else:
		print("使い方： python3 PG15puzzleImg.py イメージファイル名 (分割数:4) (ランダム数:50)")
		sys.exit()
	pygame.init()
	image = pygame.image.load(sys.argv[1])
	game = Game("15 puzzle", image, size, randcnt)
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
