# -*- coding: utf-8 -*-

import time
from moviepy.editor import *
from pydub import AudioSegment
from pydub import effects
from datetime import datetime
from reuse.telcommon import create_folder, text_to_speech, string_audio, split_string, delete_folder
from content.tel_web import ques_ans

folname = "web_zunk"
files_loc = create_folder(folname)

# ques_ans = [
#     ("తొలివేదకాలంలో గోవులు, గడ్డి భూముల కొరకు జరిగే యుద్ధాలను ఏమని పిలిచేవారు ?", "ముష్టి యుద్ధాలు", "కర్ర యుద్ధాలు", "గవిస్తి", "రాతి యుద్ధాలు", "గవిస్తి"),
# ]

qspace = "\n\n\n\t"
nlmspace = "\n\t\t\t"
aspace = "\n\t"
video_clips = []

for idx, qa in enumerate(ques_ans, 1):
	textseg = []
	filenames = []
	comque = ""
	gapduration = 500
	question = qa[0]
	options = qa[1:-1]
	answer = qa[-1]

	qaud = f"que_audio_{idx}.mp3"
	qopt1 = f"option_{idx}_1.mp3"
	qopt2 = f"option_{idx}_2.mp3"
	qopt3 = f"option_{idx}_3.mp3"
	qopt4 = f"option_{idx}_4.mp3"
	aaud = f"ans_audio_{idx}.mp3"

	print(f"{idx}: Processing.... ")

	# Calculate the length of each option and store in a list
	option_lengths = [len(option) for option in qa]
	max_length = max(option_lengths)

	# Calculate the number of spaces to add
	spaces_to_add = max(0, max_length-len(question)) + 20

	if (len(question) < 90):
		text_to_speech(question, files_loc + qaud)
	else:
		string_audio(question, files_loc + qaud)
	que_duration = AudioSegment.from_file(files_loc + qaud, format="mp3") + AudioSegment.silent(duration=gapduration)+6
	que_duration = que_duration.speedup(1.3,150,25)
	que_duration.export(files_loc + qaud, format="mp3")

	textseg.append(qspace + split_string(f"ప్రశ్న {idx}: {question}", "web"))
	filenames.append(f"{idx}_question.mp3")

	# Options Audio
	for option_idx, option in enumerate(options, 1):
		if option_idx == 4:
			gapduration = 2000
		if option_idx == 1:
			text_to_speech(f"{option}", files_loc+qopt1)
			qoption = AudioSegment.from_file(files_loc+qopt1, format="mp3") + AudioSegment.silent(duration=gapduration)+6
			qoption = qoption.speedup(1.3,150,25)
			qoption.export(files_loc+qopt1, format="mp3")
		elif option_idx == 2:
			text_to_speech(f"{option}", files_loc + qopt2)
			qoption = AudioSegment.from_file(files_loc + qopt2, format="mp3") + AudioSegment.silent(duration=gapduration)+6
			qoption = qoption.speedup(1.3,150,25)
			qoption.export(files_loc+qopt2, format="mp3")
		elif option_idx == 3:
			text_to_speech(f"{option}", files_loc + qopt3)
			qoption = AudioSegment.from_file(files_loc + qopt3, format="mp3") + AudioSegment.silent(duration=gapduration)+6
			qoption = qoption.speedup(1.3,150,25)
			qoption.export(files_loc+qopt3, format="mp3")
		elif option_idx == 4:
			text_to_speech(f"{option}", files_loc + qopt4)
			qoption = AudioSegment.from_file(files_loc + qopt4, format="mp3") + AudioSegment.silent(duration=gapduration)+6
			qoption = qoption.speedup(1.3,150,25)
			qoption.export(files_loc+qopt4, format="mp3")
		textseg.append(nlmspace + split_string(f"{option_idx}) {option}", "web"))
		filenames.append(f"option{option_idx}.mp3")

	text_to_speech("సమాధానము: "+answer, files_loc+aaud)
	ans_duration = AudioSegment.from_file(files_loc+aaud, format="mp3")+6
	ans_duration = ans_duration.speedup(1.3,150,25)
	ans_duration.export(files_loc+aaud, format="mp3")
	textseg.append(aspace + split_string(f"సమాధానము: {answer}", "web"))
	filenames.append(f"{idx}_answer.mp3")

	q_style = {'font': 'Vani-bold', 'fontsize': 38, 'color': '#000000', 'align': 'west'}
	a_style = {'font': 'Vani-bold', 'fontsize': 38, 'color': '#F00000'}

	tclipquestion = textseg[0] + " " * spaces_to_add
	if (len(tclipquestion) < 100):
		newlen = 100-len(tclipquestion)
		tclipquestion = tclipquestion + (" " * newlen)

	selopta = tclipquestion+textseg[1]
	seloptb = selopta + textseg[2]
	seloptc = seloptb + textseg[3]
	seloptd = seloptc + textseg[4]
	selans =  textseg[5]

	audques = AudioFileClip(files_loc+qaud).duration
	audopt1 = AudioFileClip(files_loc+qopt1).duration
	audopt2 = AudioFileClip(files_loc+qopt2).duration
	audopt3 = AudioFileClip(files_loc+qopt3).duration
	audopt4 = AudioFileClip(files_loc+qopt4).duration
	audans = AudioFileClip(files_loc+aaud).duration

	question_clip = TextClip(textseg[0], **q_style).set_duration(audques)
	question_clip =  question_clip.set_audio(AudioFileClip(files_loc+qaud).set_duration(audques))

	qopt_a = TextClip(selopta, **q_style).set_duration(audopt1)
	qopt_a = qopt_a.set_audio(AudioFileClip(files_loc+qopt1).set_duration(audopt1))

	qopt_b = TextClip(seloptb, **q_style).set_duration(audopt2)
	qopt_b = qopt_b.set_audio(AudioFileClip(files_loc+qopt2).set_duration(audopt2))

	qopt_c = TextClip(seloptc, **q_style).set_duration(audopt3)
	qopt_c = qopt_c.set_audio(AudioFileClip(files_loc+qopt3).set_duration(audopt3))

	qopt_d = TextClip(seloptd, **q_style).set_duration(audopt4)
	qopt_d = qopt_d.set_audio(AudioFileClip(files_loc+qopt4).set_duration(audopt4))

	selquestion = TextClip(seloptd + '\n', **q_style).set_duration(audans)
	a_clip = TextClip(selans, **a_style).set_duration(audans)
	a_clip = a_clip.set_position(("center", "bottom"))
	final_clip = CompositeVideoClip([selquestion,a_clip])
	answer_clip = final_clip.set_audio(AudioFileClip(files_loc+aaud).set_duration(audans))

	# Concatenate video clips
	video = concatenate_videoclips([question_clip, qopt_a, qopt_b, qopt_c, qopt_d, answer_clip])
	video_clips.append(video)

final_video = concatenate_videoclips(video_clips)
image_clip = ImageClip("image/telugu/bg.png").set_duration(final_video.duration)
final_clip = CompositeVideoClip([image_clip,final_video])

fname = str(datetime.now().strftime('%Y%m%d%H%M%S'))+'.mp4';
final_clip.write_videofile(fname,codec="libx264",fps=24)

time.sleep(10)
delete_folder(folname)
