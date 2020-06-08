#!/usr/bin/python3
from datetime import datetime
import sys,re
import os.path
from collections import namedtuple

LRC_IN = sys.argv[1]
SRT_OUT = sys.argv[2]

def convertTime(time):
	t=datetime.strptime(time, '%H:%M:%S.%f')
	return "{}:{}:{},{}".format(str(t.hour)[:1],str(t.minute).zfill(2),str(t.second).zfill(2),str(t.microsecond).zfill(6)[:3])

def loadLRC(file):
	lyrics=[]
	Lyric = namedtuple('Lyric', 'time lyric')

	with open(file,encoding="utf-8") as f:
		for l in f.readlines():
			st=l.split(":")
			if (len(st)==3) and st[0][1:].isdigit():
				sp=l.split("]")
				if len(sp)==2:
					time=sp[0][1:]
					lyric=sp[1].strip()
					lyrics.append(Lyric(time, lyric))
	return lyrics

def convertSRT(lyricsArray):
	output=""
	a = 0
	b = 0
	lyric = ""
	for i, row in enumerate(lyricsArray):
		currentSecond = datetime.strptime(row[0], '%H:%M:%S.%f').second
		currentLyric = row[1].split()[1].strip() if len(row[1].split())==2 else ''

		if (currentSecond != b and currentLyric != "" and i != len(lyricsArray)):
			if (a > 0):
				timeEnd = lyricsArray[len(lyricsArray)-1][0] if i>=len(lyricsArray) else row[0]
				lyric_ = re.sub(r'[。]+','。',lyric)
				output+="{}\n{}\n\n".format(convertTime(timeEnd), lyric)
			if (i != 0):
				if (currentLyric.strip() != ""):
					output+="{}\n{} --> ".format(a,convertTime(lyricsArray[i][0]))
					a+=1
					lyric = currentLyric 
					b = currentSecond
		else:
			lyric+=("。"+currentLyric)

	return output

if len(sys.argv)==3:
	if os.path.isfile(LRC_IN):
		with open(SRT_OUT,"w",encoding="utf-8") as w:
			lrc = loadLRC(LRC_IN)
			lrc.sort(key=lambda x: getattr(x, 'time')) 
			w.write(convertSRT(lrc))
	else:
		print("Error! File {} not exist".format(sys.argv[1]))
else:
	print("lrc2srt.py <in.lrc> <out.srt>")
