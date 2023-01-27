import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_UP, K_DOWN, K_SPACE, Rect
import socket
import threading
import queue
import time
import random

pygame.init()
surface = pygame.display.set_mode((800,650))
fpsclock = pygame.time.Clock()
pygame.display.set_caption("Shot")

class Client:
	def __init__(self, q, ip, port):
		self.q = q
		self.serv_address = (ip, port)
		self.cnt = 0
	def c2s(self, msg, retry=10):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		msg = "{}%{}".format(self.cnt, msg)
#		time.sleep(0.1)
		for _ in range(retry):
			s.sendto(msg.encode('utf-8'), self.serv_address)
			
		self.cnt += 1
	def com_init(self):
		sendmsg = "init_start"
		while True:
			if self.q.empty() == False:
				msg = self.q.get()
				if msg == "init_start":
					sendmsg = "init_end"
				elif msg == "init_end":
					if sendmsg == "init_start":
						self.c2s("init_end", 5)
					break
				else:
					print("invalid message:", msg)
					return -1
			self.c2s(sendmsg, 1)
			time.sleep(0.5)

class Server:
	def __init__(self, q, port2):
		self.q = q
		self.host = socket.gethostbyname(socket.gethostname())
		self.port = port2
		self.bufsize = 1024
		
		self.sock =	 socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((self.host, self.port))
		self.thread = threading.Thread(target=self.c2s, daemon=True)
		self.thread.start()
		self.table = dict()
	def c2s(self):
		try:
			while True:
				msg, cli_addr = self.sock.recvfrom(self.bufsize)
				msg = msg.decode('utf-8').split("%")
				if msg[0] not in self.table:
					self.q.put(msg[1])
					self.table[msg[0]] = msg[1]
		except Exception as e:
			print(e)
			
class Ship:
	def __init__(self, is_self):
		self.shots = []
		self.size = 100
		self.is_self = is_self
		if is_self:
			image = pygame.image.load("png/war_sentouki_man.png")
			self.image = pygame.transform.scale(image, (self.size, self.size))
		else:
			image = pygame.image.load("png/war_sentouki_woman.png")
			image = pygame.transform.scale(image, (self.size, self.size))
			self.image = pygame.transform.flip(image, True, False)
		image = pygame.image.load("png/bakuhatsu.png")
		self.explosion_img = pygame.transform.scale(image, (self.size, self.size))
		self.alive = True
	def setpos(self, pos):
		self.rect = Rect(pos[0], pos[1], self.size, self.size)
	def move(self, dy):
		if self.alive and ((dy > 0 and self.rect.bottom + dy < 600) or (dy < 0 and self.rect.top + dy > 0)):
			self.rect = self.rect.move(0, dy)
	def shot(self, dy=None):
		if self.alive and len(self.shots) < 7:
			shot = Shot(self.is_self)
			shot.setpos(self.rect.center)
			if dy is not None:
				shot.dy = dy
			self.shots.append(shot)
			return shot.dy
		return None
	def explosion(self):
		self.image = self.explosion_img
		self.shots.clear()
		self.alive = False
	def draw(self):
		surface.blit(self.image, self.rect.topleft)
		for shot in self.shots:
			shot.draw()
			if shot.move():
				self.shots.remove(shot)
		
class Shot:
	def __init__(self, is_self):
		self.size = 6
		self.is_self = is_self
		self.dy = random.randint(-5, 5)
	def setpos(self, pos):
		self.rect = Rect(pos[0], pos[1], self.size, self.size)
	def move(self):
		if self.is_self:
			if self.rect.right + 10 < 800 and self.rect.top + self.dy > 0 and self.rect.bottom + self.dy < 600:
				self.rect = self.rect.move(10, self.dy)
			else:
				return True
		else:
			if self.rect.left - 10 > 0 and self.rect.top + self.dy > 0 and self.rect.bottom + self.dy < 600:
				self.rect = self.rect.move(-10, self.dy)
			else:
				return True
		return False
	def draw(self):
		pygame.draw.circle(surface, (255,255,0) if self.is_self else (255,0,255), self.rect.center, self.size)

def main():
	ip = input("相手のPCのIPアドレスを入力してください。-> ")
	n = int(input("ポートID: 相手が0なら1を、相手が1なら0を入力して下さい。-> "))
	port1 , port2 = (8080, 8081) if n == 0 else (8081, 8080)
	q = queue.Queue()
	server = Server(q, port2)
	client = Client(q, ip, port1)
	client.com_init()
	
	myship = Ship(True)
	myship.setpos((50, 250))
	yourship = Ship(False)
	yourship.setpos((650, 250))
	move_y = 0
	message = None
	sysfont = pygame.font.SysFont("Meiryo", 30)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				client.c2s("quit#")
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					move_y = -10
				elif event.key == K_DOWN:
					move_y = 10
				elif event.key == K_SPACE:
					dy = myship.shot()
					if dy is not None:
						client.c2s("shot#{}".format(dy), 5)
			elif event.type == KEYUP:
				move_y = 0
		if move_y != 0:
			myship.move(move_y)
			client.c2s("move#{}".format(move_y), 5)
		if client.q.empty() == False:
			cmd = client.q.get().split("#")
			if cmd[0] == "quit":
				pygame.quit()
				sys.exit()
			elif cmd[0] == "move":
				yourship.move(int(cmd[1]))
			elif cmd[0] == "shot":
				yourship.shot(int(cmd[1]))
			elif cmd[0] == "lose":
				yourship.explosion()
				message = "あなたの勝ち"
		for shot in yourship.shots:
			if myship.rect.colliderect(shot.rect):
				myship.explosion()
				message = "あなたの負け"
				client.c2s("lose#")
				break
		surface.fill((255,255,255))
		myship.draw()
		yourship.draw()
		if message is not None:
			text = sysfont.render(message, True, (255,0,0))
			surface.blit(text, (300, 250))
		pygame.display.update()
		fpsclock.tick(15)

if __name__ == '__main__':
	main()