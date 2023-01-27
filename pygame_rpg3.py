import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import copy
import random
import time
import socket
import threading
import queue
import math

pygame.init()
surface = pygame.display.set_mode((800,650))
fpsclock = pygame.time.Clock()
pygame.display.set_caption("RPG")
sysfont = pygame.font.SysFont("Meiryo", 12)
titlefont = pygame.font.SysFont("Meiryo", 20)

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
	def play(self, offense, defense, player, enemy):
		console = Console((50, 610), sysfont)
		player.setpos((50, 0))
		enemy.setpos((450, 0))
	
		def draw():
			surface.fill((255,255,255))
			player.draw(surface)
			enemy.draw(surface)
			console.draw(surface)
			pygame.display.update()
			if console.waittime == 0:
				fpsclock.tick(10)
			else:
				fpsclock.tick(console.waittime)
				console.clear()	
								
		while True:
			if player.stage is None:
				no = None
				while player.stage is None:
					console.settext("戦うレンジャーを選んで下さい。", 0)
					for event in pygame.event.get():
						if event.type == QUIT:
							self.c2s("quit#interrupt")
							pygame.quit()
							sys.exit()
						elif event.type == MOUSEBUTTONDOWN:
							pos = event.pos
							for i, ranger in enumerate(player.rangers):
								if check_rect(ranger.rect, pos):
									no = i
									player.setstage(ranger)
									break
					draw()
				self.c2s("select#{}".format(i))
			console.clear()
			draw()
			if enemy.stage is None:
				msg = self.q.get().split("#")
				while msg[0] != "select":
					if self.q.empty() != False:
						msg = self.q.get().split("#")
				enemy.setstage(enemy.rangers[int(msg[1])])
			offense.stage.setcheck(True)
			defense.stage.setcheck(False)
			item = None
			while item is None:
				offense.stage.setmode()
				defense.stage.setmode()
				if offense == player:
					if console.text is None:
						console.settext("{}さんの番です。アイテムを選び、クリックして下さい。".format(offense.name), 0)
					for event in pygame.event.get():
						if event.type == QUIT:
							self.c2s("quit#interrupt")
							pygame.quit()
							sys.exit()
						elif event.type == MOUSEBUTTONDOWN:
							pos = event.pos						
							for i, it in enumerate(offense.stage.items):
								if check_rect(it.rect, pos):
									if offense.stage.select == i:
										item = offense.stage.items[i]
										console.settext("{}さんの{}は{}を使った。".format(offense.name, offense.stage.name, item.name), 0.3)
										if len(item.effect) == 1:
											effect = item.effect[0]
										else:
											effect = random.choice(item.effect)
										if type(item) is Item:
											if effect == None:
												effect = (0,0)
											elif offense.stage.spell is not None:
												if offense.stage.spell.effect >= 0:
													effect = (effect[0] * offense.stage.spell.effect, effect[1] * offense.stage.spell.effect)
												else:
													effect = (int(effect[0] / -offense.stage.spell.effect), int(effect[1] / -offense.stage.spell.effect))
											self.c2s("item#{}#{}#{}".format(i, effect[0], effect[1]))
										else:
											if effect == None:
												effect = (1,1)
											if len(item.turn) == 1:
												turn = item.turn[0]
											else:
												turn = random.choice(item.turn)
											self.c2s("spell#{}#{}#{}#{}".format(i, effect[0], effect[1], turn))
									else:
										offense.stage.selectitem(i)
									break
				elif offense.stage.select is None:
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
						offense.stage.selectitem(int(msg[1]))
						effect = (int(msg[2]), int(msg[3]))
					elif msg[0] == "spell":
						offense.stage.selectitem(int(msg[1]))
						effect = (int(msg[2]), int(msg[3]))
						turn = int(msg[4])
				else:
					item = offense.stage.items[offense.stage.select]
					console.settext("{}さんの{}は{}を使った。".format(offense.name, offense.stage.name, item.name), 0.3)
				draw()
			offense.stage.clearselect()
			if offense.stage.spell is not None:
				if offense.stage.spell.turn > 0:
					offense.stage.spell.turn -= 1
				if offense.stage.spell.turn == 0:
					offense.stage.spell = None
			if type(item) is Item:
				if effect[0] != 0:
					defense.stage.damage(effect[0])
					if effect[0] > 0:
						console.settext("{}さんの{}のHPが{}に減った。".format(defense.name, defense.stage.name, defense.stage.hp), 0.5)
					else:
						console.settext("{}さんの{}のHPが{}に回復した。".format(defense.name, defense.stage.name, defense.stage.hp), 0.5)
				if effect[1] != 0:
					offense.stage.damage(-effect[1])
					if effect[0] > 0:
						console.settext("{}さんの{}のHPが{}に減った。".format(offense.name, offense.stage.name, offense.stage.hp), 0.5)
					else:
						console.settext("{}さんの{}のHPが{}に回復した。".format(offense.name, offense.stage.name, offense.stage.hp), 0.5)					
				if effect[0] == 0 and effect[1] == 0:
					console.settext("何もおこならなった", 0.5)
			else:
				spell = copy.copy(item)
				spell.turn = turn
				if effect[0] != 1:
					spell.effect = effect[0]
					defense.stage.setspell(spell)
					if effect[0] > 1:
						console.settext("{}さんの{}の能力が{}ターン{}倍になった。".format(defense.name, defense.stage.name, turn, effect[0]), 0.5)
					else:
						console.settext("{}さんの{}の能力が{}ターン{}分の1になった。".format(defense.name, defense.stage.name, turn, -effect[0]), 0.5)
				if effect[1] != 1:
					spell.effect = effect[1]
					offense.stage.setspell(spell)
					if effect[1] > 1:
						console.settext("{}さんの{}の能力が{}ターン{}倍になった。".format(offense.name, offense.stage.name, turn, effect[0]), 0.5)
					else:
						console.settext("{}さんの{}の能力が{}ターン{}分の1になった。".format(offense.name, offense.stage.name, turn, -effect[0]), 0.5)
				if effect[0] == 1 and effect[1] == 1:
					console.settext("何もおこならなった", 0.5)
			draw()
			if defense.stage.hp == 0:
				defense.stage.setmode(5)
				offense.stage.setmode(6)
				console.settext("{}さんの{}は死んでしまった。".format(defense.name, defense.stage.name), 0.5)
				draw()
				defense.stage = None
				if len(defense.rangers) == 0:
					console.settext("{}が{}に勝ちました。".format(offense.name, defense.name), 0.1)
					draw()
					break
			if offense.stage.hp == 0:
				offense.stage.setmode(5)
				defense.stage.setmode(6)
				console.settext("{}さんの{}は死んでしまった。".format(offense.name, offense.stage.name), 0.5)
				draw()
				offense.stage = None
				if len(offense.rangers) == 0:
					console.settext("{}が{}に勝ちました。".format(defense.name, offense.name), 0.1)
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
	
class Ranger:
	def __init__(self, male, images, files=None):
		self.male = male
		if images is None:
			self.images = []
			for fn in files:
				self.images.append(pygame.image.load(fn))
		else:
			self.images = images
		self.checked = False
		self.mode = 0
		self.items = []
		self.select = None
		self.spell = None
	def setspell(self, spell):
		self.spell = spell
	def setsize(self, size):
		self.size = size
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

	def damage(self, hp):
		if hp > 0:
			self.mode = 4
			hp = min(hp, self.hp)
		else:
			self.mode = 3
		self.hp -= hp
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
	def draw(self, surface, itemdetail=True):
		if self.spell is None:
			mode = self.mode
		elif self.mode in [0, 1, 2]:
			if self.spell.effect > 1:
				mode = 8
			else:
				mode = 7
		else:
			mode = self.mode
		image = pygame.transform.scale(self.images[mode], (self.size, self.size))
		pygame.draw.rect(surface, self.color, self.rect)
		surface.blit(image, (self.rect[0], self.rect[1]))
		if self.checked:
			pygame.draw.rect(surface, (255,0,0) if self.male else (0,0,255), self.rect, 3)
		if itemdetail:
			profile = sysfont.render("{} HP:{}".format(self.name, self.hp), True, (0,0,0))
			surface.blit(profile, (self.rect[0], self.rect[1]+self.size))
			if self.spell is not None:
				if self.spell.effect > 0:
					spell = sysfont.render("{}により、{}ターン、能力が{}倍".format(self.spell.name, self.spell.turn, self.spell.effect), True, (0,0,0))
				elif self.spell.effect == 0:
					spell = sysfont.render("{}により、あと{}ターン、能力がなし".format(self.spell.name, self.spell.turn), True, (0,0,0))
				else:
					spell = sysfont.render("{}により、あと{}ターン、能力が{}分の1".format(self.spell.name, self.spell.turn, -self.spell.effect), True, (0,0,0))
				surface.blit(spell, (self.rect[0], self.rect[1]+self.size+20))
		else:
			profile = sysfont.render("{}".format(self.name), True, (0,0,0))
			surface.blit(profile, (self.rect[0], self.rect[1]+self.size))
			profile = sysfont.render("HP: {}".format(self.hp), True, (0,0,0))
			surface.blit(profile, (self.rect[0], self.rect[1]+self.size+15))
		if self.spell is not None:
			x, y = self.rect[0], self.rect[1]+self.size+40
		else:
			x, y = self.rect[0], self.rect[1]+self.size+20	
		for i, item in enumerate(self.items):
			if itemdetail:
				item.setpos((x, y))
				y += item.rect[3]
				item.setsize(25)
				item.draw(surface)
			else:
				itemname = sysfont.render("{}".format(item.name), True, (0,0,0))
				surface.blit(itemname, (self.rect[0], self.rect[1]+self.size+30+i*15))
				
	def clone(self, name, hp, color, item_nums=None):
		ranger = Ranger(self.male, self.images)
		ranger.name = name
		ranger.hp = hp
		ranger.color = color
		if item_nums is None:
			for item in self.items:
				ranger.additem(item)
		else:
			for i in item_nums:
				ranger.additem(items[i-1])
		return ranger
	def __copy__(self):
		return self.clone(self.name, self.hp, self.color)

class Player:
	def __init__(self, name):
		self.name = name
		self.rangers = []
		self.stage = None
	def addranger(self, ranger):
		self.rangers.append(copy.copy(ranger))
	def setpos(self, pos):
		self.pos = pos
	def setstage(self, ranger):
		self.stage = ranger
		self.rangers.remove(ranger)
	def changestage(self, ranger):
		self.rangers.append(self.stage)
		self.setstage(ranger)
	def draw(self, surface):
		title = titlefont.render(self.name, True, (0,0,0))
		surface.blit(title, (self.pos[0]+25, self.pos[1]))
		if self.stage is None:
			if len(self.rangers) == 0:
				title = titlefont.render("負けました", True, (255,0,0))
				surface.blit(title, (self.pos[0]+100, self.pos[1]+150))
			else:
				pygame.draw.rect(surface, (128,128,128), (self.pos[0]+50, self.pos[1]+50, 250, 250))
		else:
			self.stage.setsize(250)
			self.stage.setpos((self.pos[0]+50, self.pos[1]+50))
			self.stage.draw(surface)
		for i, ranger in enumerate(self.rangers):
			ranger.setsize(100)
			ranger.setpos((self.pos[0]+i*120, self.pos[1]+420))
			ranger.draw(surface, False)

class Item:
	def __init__(self, name, imagefile, effect):
		self.name = name
		self.effect = effect
		self.imagefile = imagefile
		self.image = pygame.image.load(imagefile)
		self.checked = False
		self.size = 0
	def setsize(self, size):
		self.size = size
	def setpos(self, pos):
		self.rect = (pos[0], pos[1], 250, self.size)
	def setcheck(self, checked):
		self.checked = checked
	def drawprofile(self, surface, right):
		if right:
			text = "{} 効果:{}".format(self.name, str(self.effect))
			profile = sysfont.render(text, True, (0,0,0))
			surface.blit(profile, (self.rect[0]+self.size+10, self.rect[1]+self.size//4))
		else:
			text = "アイテム:{}".format(self.name)
			profile = sysfont.render(text, True, (0,0,0))
			surface.blit(profile, (self.rect[0], self.rect[1]+self.size))
			text = "{}".format(str(self.effect))
			profile = sysfont.render(text, True, (0,0,0))
			surface.blit(profile, (self.rect[0], self.rect[1]+self.size+15))
	def draw(self, surface, right=True):
		image = pygame.transform.scale(self.image, (self.size, self.size))
		surface.blit(image, (self.rect[0], self.rect[1]))
		if self.checked:
			pygame.draw.rect(surface, (0,0,255), self.rect, 3)
		self.drawprofile(surface, right)
	def __copy__(self):
		return Item(self.name, self.imagefile, self.effect)
		
class Spell(Item):
	def __init__(self, name, imagefile, effect, turn):
		super().__init__(name, imagefile, effect)
		self.turn = turn
		self.profile = "{} 効果:{}期間:{}".format(self.name, str(self.effect), str(self.turn))
	def drawprofile(self, surface, right):
		if right:
			text = "{} 効果:{}{}".format(self.name, str(self.effect), str(self.turn))
			profile = sysfont.render(text, True, (0,0,0))
			surface.blit(profile, (self.rect[0]+self.size+10, self.rect[1]+self.size//4))
		else:
			text = "スペル: {}".format(self.name)
			profile = sysfont.render(text, True, (0,0,0))
			surface.blit(profile, (self.rect[0], self.rect[1]+self.size))
			text = "{}".format(str(self.effect))
			profile = sysfont.render(text, True, (0,0,0))
			surface.blit(profile, (self.rect[0], self.rect[1]+self.size+15))
			text = "{}".format(str(self.turn))
			profile = sysfont.render(text, True, (0,0,0))
			surface.blit(profile, (self.rect[0], self.rect[1]+self.size+30))
	def __copy__(self):
		return Spell(self.name, self.imagefile, self.effect, self.turn)
		
items = [\
	Item("竹刀","png/sports_kendou_shinai.png",[(20,0)]),\
	Item("剣","png/game_ken.png",[(40,0)]),\
	Item("聖剣","png/game_ken_seiken.png",[(60,0)]),\
	Item("水","png/bousai_water.png",[(0,20)]),\
	Item("栄養剤","png/drink_energy.png",[(0,40)]),\
	Item("薬","png/medical_syrup_kusuri.png",[(0,60)]),\
	Item("謎の剣","png/war_etsuou_kousenken.png",[None,(50,0)]),\
	Item("謎の薬", "png/medical_bannouyaku.png", [None,(0,50)]),\
	Item("魔剣", "png/game_ken_maken.png", [None, None,(100,0)]),\
	Item("魔法の薬", "png/medical_kusuri_bin.png", [None,None,(0,100)]),\
	Spell("忍術","png/ninja.png",[None,(1,2)],[2,3]),\
	Spell("悪魔の呪い","png/character_akuma.png",[None,(-3,1)],[4]),\
	Spell("くノ一の術","png/ninja_kunoichi.png",[None,(1,2),(-2,1)],[1,2]),\
	Spell("魔女の呪い","png/fantasy_witch.png",[(1,-2),(-2,1)],[2]),\
	]
	
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

ranger_man = Ranger(True, None, ["png/stand1_front05_man.png",\
	"png/pose_genki03_man.png", "png/shinpai_man.png", "png/pose_makasenasai_boy.png",\
	"png/pose_shock_man.png", "png/sick_kaoiro_man.png", "png/seikou_banzai_man.png",\
	"png/sick_panic_man.png", "png/yaruki_moeru_man.png"])
ranger_woman = Ranger(False, None, ["stand1_front06_woman.png",\
	"png/pose_genki04_woman.png", "png/shinpai_woman.png", "png/pose_makasenasai_girl.png",\
	"png/pose_shock_woman.png", "png/sick_kaoiro_woman.png", "png/seikou_banzai_woman.png",\
	"png/sick_panic_woman.png", "png/yaruki_moeru_woman.png"])
rangers = [ranger_woman.clone("ホワイト",100,(255,255,255),[1,6,13]),\
	ranger_woman.clone("ピンク",100,(255,105,180),[1,5,7]),\
	ranger_woman.clone("レッド",100,(255,0,0),[2,6,13]),\
	ranger_woman.clone("オレンジ",100,(255,165,0),[1,5,14]),\
	ranger_woman.clone("バイオレット",100,(238,130,238),[2,5,10]),\
	ranger_man.clone("ブルー",150,(0,0,255),[2,8,9]),\
	ranger_man.clone("グリーン",150,(0,255,0),[2,10,11]),\
	ranger_man.clone("イエロー",150,(255,255,0),[3,4,9]),\
	ranger_man.clone("アクア",150,(0,255,255),[3,5,11]),\
	ranger_man.clone("ブラック",150,(0,0,0),[3,4,12])]
	
def selectranger():
	console = Console((20, 600), sysfont)
	
	def draw():
		surface.fill((255,255,255))
		text = titlefont.render("アイテム／スペル一覧", True, (0,0,0))
		surface.blit(text, (20, 0))
		for i, item in enumerate(items):
			item.setsize(80)
			item.setpos((25+(i%5)*150, 30+(i//5)*120))
			item.draw(surface, False)
		text = titlefont.render("レンジャー一覧", True, (0,0,0))
		surface.blit(text, (20, 400))
		for i, ranger in enumerate(rangers):
			ranger.setsize(60)
			ranger.setpos((20+i*75, 435))
			ranger.draw(surface, False)
		console.draw(surface)
		if ok:
			pygame.draw.rect(surface, (255,0, 0), (450, 600, 100, 20))
			text = titlefont.render("決定", True, (255,255,255))
		else:
			pygame.draw.rect(surface, (0,255,0), (450, 600, 100, 20))
			text = titlefont.render("決定", True, (0,0,0))
		surface.blit(text, (480, 595))
		pygame.display.update()
		fpsclock.tick(10)
	
	console.settext("レンジャーを３人クリックで選んで、決定ボタンを押して下さい。", 0)
	checked_rangers = []
	ok = False
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				#self.c2s("quit#interrupt")
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				pos = event.pos
				if check_rect((450,600,100,20), pos) and len(checked_rangers) == 3:
					ok = True
					draw()
					return checked_rangers
				for i, ranger in enumerate(rangers):
					if check_rect(ranger.rect, pos):
						if not ranger.checked and len(checked_rangers) < 3:
							ranger.setcheck(True)
							checked_rangers.append(i)
						elif ranger.checked:
							ranger.setcheck(False)
							checked_rangers.remove(i)
		draw()
	
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
	
	players = [Player(player1), Player(player2)]
		
	offense = players[sid if turn else eid]
	defense = players[eid if turn else sid]
	
	ids = selectranger()
	client.c2s("rangers#{}:{}:{}".format(ids[0],ids[1],ids[2]))
	for i in ids:
		players[sid].addranger(rangers[i])
	msg = client.q.get().split("#")
	while msg[0] != "rangers":
		if client.q.empty() != False:
			msg = client.q.get().split("#")
	for i in msg[1].split(":"):
		players[eid].addranger(rangers[int(i)])
	client.play(offense, defense, players[sid], players[eid])

if __name__ == '__main__':
	main()