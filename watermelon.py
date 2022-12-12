import random
import keyboard

def get_key():
	keyboard.read_key()
	return keyboard.read_key()

watermelon_x = random.randint(0, 5)
watermelon_y = random.randint(0, 5)

player_x = random.randint(0, 5)
player_y = random.randint(0, 5)

while player_x == watermelon_x and player_y == watermelon_y:
	player_x = random.randint(0, 5)
	player_y = random.randint(0, 5)
	
while player_x != watermelon_x or player_y != watermelon_y:
	print("スイカとの距離x", abs(player_x - watermelon_x), "スイカとの距離y", abs(player_y - watermelon_y))
	while True:
		print("矢印キーを押してね")
		c = get_key()
		if c == "up":
			player_y += 1
			break
		elif c == "down":
			player_y -= 1
			break
		elif c == "left":
			player_x -= 1
			break
		elif c == "right":
			player_x += 1
			break

print("スイカを割りました！")
		