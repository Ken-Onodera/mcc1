import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import copy
import random
import time
import socket
import threading
import queue

pygame.init()
surface = pygame.display.set_mode((400,300))
fpsclock = pygame.time.Clock()
pygame.display.set_caption("RPG")
sysfont = pygame.font.SysFont("Meiryo", 12)

class Client:
	def __init__(self, q, ip, port):
		self.q = q
		self.serv_address = (ip, port)
		self.cnt = 0
	def c2s(self, msg, retry=10):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		msg = "{}%{}".format(self.cnt, msg)
		time.sleep(0.1)
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
	def play(self, offense, defense, id):
		console = Console((20, 280), sysfont)
	
		def draw():
			surface.fill((255,255,255))
			offense.draw(surface)
			defense.draw(surface)
			console.draw(surface)
			pygame.display.update()
			if console.waittime == 0:
				fpsclock.tick(10)
			else:
				fpsclock.tick(console.waittime)
				console.clear()		
	
		while True:
			offense.setcheck(True)
			defense.setcheck(False)
			item = None
			while item is None:
				offense.setmode()
				defense.setmode()
				if offense.id == id:
					if console.text is None:
						console.settext("{}さんの番です。アイテムを選び、クリックして下さい。".format(offense.name), 0)
					for event in pygame.event.get():
						if event.type == QUIT:
							self.c2s("quit#interrupt")
							pygame.quit()
							sys.exit()
						elif event.type == MOUSEBUTTONDOWN:
							pos = event.pos						
							for i, it in enumerate(offense.items):
								if check_rect(it.rect, pos):
									if offense.select == i:
										item = offense.items[i]
										console.settext("{}は{}を使った。".format(offense.name, item.name), 0.3)
										if len(item.effect) == 1:
											effect = item.effect[0]
										else:
											effect = random.choice(item.effect)
										self.c2s("item#{}#{}".format(i, effect))
									else:
										offense.selectitem(i)
									break
				elif offense.select is None:
					console.settext("{}さんの番です".format(offense.name), 0)
					while self.q.empty():
						for event in pygame.event.get():
							if event.type == QUIT:
								self.c2s("quit#interrupt")
								pygame.quit()
								sys.exit()
						draw()
					msg = self.q.get().split("#")
					if msg[0] == "quit":
						pygame.quit()
						sys.exit()
					elif msg[0] == "item":
						offense.selectitem(int(msg[1]))
						effect = int(msg[2])
				else:
					item = offense.items[offense.select]
					console.settext("{}は{}を使った。".format(offense.name, item.name), 0.3)
				draw()
			offense.clearselect()
			if effect > 0:
				defense.damage(effect)
				console.settext("{}のHPが{}に減った。".format(defense.name, defense.hp), 0.5)
			elif effect < 0:
				offense.damage(effect)
				console.settext("{}のHPが{}に回復した。".format(offense.name, offense.hp), 0.5)
			else:
				console.settext("何もおこならなった", 0.5)
			draw()
			if defense.hp == 0:
				defense.setmode(5)
				console.settext("{}は死んでしまった。".format(defense.name), 0.5)
				draw()
				offense.setmode(6)
				console.settext("{}が{}に勝ちました。".format(offense.name, defense.name), 0.1)
				draw()
				break
			offense, defense = defense, offense
		
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
					#print(msg)
		except Exception as e:
			print(e)

def check_rect(rect, pos):
	x, y, w, h = rect
	mx, my = pos
	return x <= mx and mx <= x+w and y <= my and my <= y+h
	
class Player:
	def __init__(self, name, hp, images, size, id):
		self.name = name
		self.id = id
		self.hp = hp
		self.images = []
		for fn in images:
			image = pygame.image.load(fn)
			self.images.append(pygame.transform.scale(image, (size, size)))
		self.checked = False
		self.mode = 0
		self.size = size
		self.items = []
		self.select = None
	def selectitem(self, i):
		for j, item in enumerate(self.items):
			if i == j:
				item.setcheck(True)
			elif item.checked:
				item.setcheck(False)
		self.select = i
	def clearselect(self):
		for item in self.items:
			if item.checked:
				item.setcheck(False)
		self.select = None
	def setpos(self, pos):
		self.rect = (pos[0], pos[1], self.size, self.size)
		x, y = pos[0], pos[1]+self.size+20
		for item in self.items:
			item.setpos((x, y))
			y += item.rect[3]
	def damage(self, hp):
		if hp > 0:
			self.mode = 4
			hp = min(hp, self.hp)
		else:
			self.mode = 3
		self.hp -= hp
	def setfont(self, font):
		self.font = font
		for item in self.items:
			item.setfont(font)
	def setcheck(self, checked):
		self.checked = checked
	def setmode(self, mode=None):
		if mode is None:
			if self.hp > 100:
				self.mode = 1
			elif self.hp <= 50:
				self.mode = 2
			else:
				self.mode = 0
		else:
			self.mode = mode
	def additem(self, item):
		self.items.append(copy.copy(item))
	def draw(self, surface):
		surface.blit(self.images[self.mode], (self.rect[0], self.rect[1]))
		if self.checked:
			pygame.draw.rect(surface, (255,0,0), self.rect, 3)
		profile = self.font.render("{} HP:{}".format(self.name, self.hp), True, (0,0,0))
		surface.blit(profile, (self.rect[0], self.rect[1]+self.size))
		for item in self.items:
			item.draw(surface)
		
class Item:
	def __init__(self, name, imagefile, effect, size):
		self.name = name
		self.effect = effect
		self.imagefile = imagefile
		image = pygame.image.load(imagefile)
		self.image = pygame.transform.scale(image, (size, size))
		self.size = size
		self.checked = False
	def setpos(self, pos):
		self.rect = (pos[0], pos[1], 150, self.size)
	def setcheck(self, checked):
		self.checked = checked
	def setfont(self, font):
		self.font = font
	def draw(self, surface):
		surface.blit(self.image, (self.rect[0], self.rect[1]))
		if self.checked:
			pygame.draw.rect(surface, (0,0,255), self.rect, 3)
		profile = self.font.render("{} 効果:{}".format(self.name, str(self.effect)), True, (0,0,0))
		surface.blit(profile, (self.rect[0]+self.size+10, self.rect[1]+self.size//4))
	def __copy__(self):
		return Item(self.name, self.imagefile, self.effect, self.size)
		
items = [Item("剣", "game_ken.png", [20], 25),\
	Item("魔剣", "game_ken_maken.png", [0, 50], 25),\
	Item("薬", "medical_kusuri_bin.png", [-20], 25),
	Item("謎の薬", "medical_bannouyaku.png", [0, -50], 25)]
	
class Console:
	def __init__(self, pos, font):
		self.pos = pos
		self.font = font
		self.waittime = 0
		self.text = None
	def settext(self, text, waittime):
		self.text = text
		self.waittime = waittime
	def clear(self):
		self.waittime = 0
		self.text = None
	def draw(self, surface):
		if self.text is not None:
			text = self.font.render(self.text, True, (0,0,0))
			surface.blit(text, self.pos)

def main():
	ip = input("相手のPCのIPアドレスを入力してください。-> ")
	n = int(input("ポートID: 相手が0なら1を、相手が1なら0を入力して下さい。-> "))
	port1 , port2 = (8080, 8081) if n == 0 else (8081, 8080)
	q = queue.Queue()
	server = Server(q, port2)
	client = Client(q, ip, port1)
	client.com_init()
	name = input("プレイヤーの名前を入れて下さい。 -> ")
	if n == 0:
		client.c2s("player#{}".format(name))
		while client.q.empty():
			time.sleep(0.1)
		msg = client.q.get().split("#")
		while msg[0] != "player":
			if client.q.empty() != False:
				msg = client.q.get().split("#")
		player1 = name
		player2 = msg[1]
		sid, eid = 0, 1
		turn = random.choice([True, False])
		client.c2s("turn#"+str(not turn))
	elif n == 1:
		while client.q.empty():
			time.sleep(0.1)
		msg = client.q.get().split("#")
		while msg[0] != "player":
			if client.q.empty() != False:
				msg = client.q.get().split("#")
		player1 = msg[1]
		player2 = name
		sid, eid = 1, 0
		client.c2s("player#{}".format(name))
		while client.q.empty():
			time.sleep(0.1)
		msg = client.q.get().split("#")
		while msg[0] != "turn":
			if client.q.empty() != False:
				msg = client.q.get().split("#")
		turn = True if msg[1] == "True" else False
	
	players = [Player(player1, 100, ["png/stand1_front05_man.png", "png/pose_genki03_man.png", \
		"png/shinpai_man.png", "png/yaruki_moeru_man.png", "png/pose_shock_man.png",\
		"png/sick_kaoiro_man.png", "png/seikou_banzai_man.png"], 150, 0), \
		Player(player2, 100, ["png/stand1_front06_woman.png", "png/pose_genki04_woman.png",\
		"png/shinpai_woman.png", "png/yaruki_moeru_woman.png", "png/pose_shock_woman.png",\
		"png/sick_kaoiro_woman.png", "png/seikou_banzai_woman.png"], 150, 1)]
	x = 30
	for player in players:
		for item in items:
			player.additem(item)
		player.setfont(sysfont)
		player.setpos((x,0))
		x += 200
	
	offense = players[sid if turn else eid]
	defense = players[eid if turn else sid]
	
	client.play(offense, defense, sid)

if __name__ == '__main__':
	main()