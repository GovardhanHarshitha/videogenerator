# -*- coding: utf-8 -*-

import time
from moviepy.editor import *
from pydub import AudioSegment
from datetime import datetime
from reuse.telcommon import create_folder, text_to_speech, string_audio, split_string, delete_folder
from content.tel_shorts import ques_ans

folname = "web_zunk"
files_loc = create_folder(folname)

# ques_ans = [
# 	("విధ్యను ప్రాథమిక హక్కుగా గుర్తించాలని చెప్పినకేసు?","ఇందిరాసహని వర్సెస్ యూనియన్ ఆఫ్ ఇండియా 1992","మినార్వ మిల్స్ వర్సెస్ యూనియన్ ఆఫ్ ఇండియా 1980","సజ్జన్ సింగ్ వర్సెస్ స్టేట్ ఆఫ్ రాజస్థాన్ 1964","ఉన్నికృష్ణన్ వర్సెస్ ఆంద్రప్రదేశ్ - మెహినిజైన్ వర్సెస్ కర్ణాటక 1993","ఉన్నికృష్ణన్ వర్సెస్ ఆంద్రప్రదేశ్ - మెహినిజైన్ వర్సెస్ కర్ణాటక 1993"),
# ]

qspace = "\n\n\n\n\t"
ospace = "\n\n"
aspace = "\n\t\t"

video_clips = []
quse_length = []
com_clip = []

q_style = {'font':'Vani-bold', 'fontsize':75, 'color':'#65fff2', 'align':'west'}
a_style = {'font':'Vani-bold', 'fontsize':75, 'color':'#edd36c', 'align':'west'}

def generate_question_with_audio(txtaudio, txtmsg, idx, sidx):
	gapduration = 1000
	qaud = f"gen_audio_{idx}_{sidx}.mp3"

	string_audio(txtaudio, files_loc + qaud)
	que_duration = AudioSegment.from_file(files_loc + qaud, format="mp3") + AudioSegment.silent(duration=gapduration) + 5
	que_duration = que_duration.speedup(1.3,100,25)
	que_duration.export(files_loc + qaud, format="mp3")

	audques = AudioFileClip(files_loc+qaud).duration
	question_clip = TextClip(txtmsg, **q_style).set_duration(audques)
	question_clip = question_clip.set_audio(AudioFileClip(files_loc+qaud).set_duration(audques))

	# Concatenate video clips
	return concatenate_videoclips([question_clip])

def generate_sans_with_audio(txtaudio, txtmsg1, txtmsg2, idx, sidx):
	gapduration = 200
	qaud = f"gen_audio_{idx}_{sidx}.mp3"

	string_audio(txtaudio, files_loc + qaud)
	que_duration = AudioSegment.from_file(files_loc + qaud, format="mp3") + AudioSegment.silent(duration=gapduration) + 5
	que_duration = que_duration.speedup(1.3,100,25)
	que_duration.export(files_loc + qaud, format="mp3")

	audques = AudioFileClip(files_loc+qaud).duration
	question_clip = TextClip(txtmsg1, **q_style).set_duration(audques)
	answer_clip = TextClip(txtmsg2, **a_style).set_duration(audques)
	answer_clip = answer_clip.set_position(("center","bottom"))
	final_clip = CompositeVideoClip([question_clip, answer_clip])
	final_clip = final_clip.set_audio(AudioFileClip(files_loc+qaud).set_duration(audques))

	# Concatenate video clips
	return concatenate_videoclips([final_clip])

for idx, qa in enumerate(ques_ans, 1):
	question = qa[0]
	answer = qa[-1]

	print(f"{idx}: Processing.... ")

	# Formatting Audio Questions
	aques = split_string(question, "short")

	# Formatting  Questions

	qtitle = qspace + f"ప్రశ్న:" + '\n\t'
	ques = split_string(f"{question}", "short")

	ans = split_string(f"{answer}", "short")

	prnque = qtitle + ques[0]
	prnque += " " * max(0, 26 - len(prnque)) + ospace

	prnans = "సమాధానము: " + "\n" + ans[0]

	question_clip = generate_question_with_audio(aques[0], prnque, idx, 'ques')
	answer_clip = generate_sans_with_audio(ans[0], prnque, prnans, idx, 'ans')

	# Concatenate video clips
	video = concatenate_videoclips([question_clip, answer_clip])
	video_clips.append(video)

final_video = concatenate_videoclips(video_clips)
image_clip = ImageClip("image/telugu/shorts.webp").set_duration(final_video.duration)
final_clip = CompositeVideoClip([image_clip,final_video])

fname = str(datetime.now().strftime('%Y%m%d%H%M%S'))+'.mp4';
final_clip.write_videofile(fname,codec="libx264",fps=24)
