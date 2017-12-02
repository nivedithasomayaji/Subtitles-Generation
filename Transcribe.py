#!/usr/bin/env python3
import datetime
import speech_recognition as sr
import subprocess

print("Enter the .mp4 file that needs to be converted(full path required) :")
file1 = raw_input()
subprocess.call("rm -f ../audio.wav", shell = True)
subprocess.call("rm -f ./SubtitlesFile.srt", shell = True)
print("Extracting audio from the video..")
command = "ffmpeg -nostats -loglevel 0 -i "+file1+" -vn -acodec pcm_s16le -ar 44100 -ac 2 ../audio.wav"
subprocess.call(command, shell = True)
r = sr.Recognizer()
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath("/home/niveditha/niveditha/sp/speechstuff/")), "audio.wav")

currentTime = datetime.datetime(100,1,1,0,0,0)
print("Enter the duration for which the subtitles should be generated(in minutes):")
num = raw_input()
num = int(num)
maxTime = datetime.datetime(100,1,1,0,num,0)

blockNum = 0
print("Generating subtitles file...\nThis might take around "+str(int(num*0.75))+" minutes and "+str(((num*0.75)-int(num*0.75))*60)+" seconds..\nPlease wait..")
def speechToSrt(currentTime,maxTime, block) :

	with sr.AudioFile(AUDIO_FILE) as source :				
		
		while currentTime < maxTime :
		# recognize speech using Sphinx
			audio = r.record(source,duration = 5)  
			block += 1
			block_str = str(block)
			try:
		   			sentence = (r.recognize_sphinx(audio))
			except sr.UnknownValueError:
	    			print("Sphinx could not understand audio")
			except sr.RequestError as e:
	    			print("Sphinx error; {0}".format(e))
		
			timeAdd = 5
			endTime = currentTime + datetime.timedelta(0,timeAdd)
			currentTimeStr = str(currentTime.time())
			endTimeStr = str(endTime.time())

			with open("SubtitlesFile.srt" , "a") as f:
				f.write(block_str)
				f.write("\n")
				f.write(currentTimeStr)
				f.write(" --> ")
				f.write(endTimeStr)
				f.write("\n")
				f.write(sentence)
				f.write("\n\n")

			currentTime = endTime

	return 

speechToSrt(currentTime,maxTime,blockNum)
print("File SubtitleFile.srt generated.\n")
