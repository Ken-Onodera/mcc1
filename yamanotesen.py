import os
from inputimeout import inputimeout, TimeoutOccurred

title = "山手線の駅名"
remain = ["とうきょう", "かんだ","あきはばら","おかちまち","うえの","うぐいすだに","にっぽり","にしにっぽり","たばた","こまごめ","すがも","おおつか","いけぶくろ","めじろ","たかだのばば","しんおおくぼ","しんじゅく","よよぎ","はらじゅく","しぶや","えびす","めぐろ","ごたんだ","おおさき","しながわ","たかなわげーとうぇい","たまち","はままつちょう","しんばし","ゆうらくちょう"]
consume = []

print(title,"をひらがなでタイムアウト時間以内に入力しね。タイムアウト時間以内に入力しないか、入力済の名前を入力するか、間違っていたらアウトだよ")
timeout = int(input("タイムアウト時間を入力したら開始だよ。　タイムアウト時間（秒）は: "))

while len(remain) > 0:
	try:
		station = inputimeout(prompt=title+"は？"+str(timeout)+"秒以内に答てね: ",timeout=timeout)
	except TimeoutOccurred:
		print("タイムオーバーです！")
		break
	if station in remain:
		os.system('cls')
		print("正解です！")
		remain.remove(station)
		consume.append(station)
	elif station in consume:
		print("入力済の名前です、アウト！")
		break
	else:
		print("間違いです、アウト！")
		break
if len(remain) == 0:
	print("大正解です！")
else:
	print("正解は、",remain, "です。")