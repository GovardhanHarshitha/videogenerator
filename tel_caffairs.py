# -*- coding: utf-8 -*-

from moviepy.editor import *
from pydub import AudioSegment
from reuse.telcommon import create_folder, text_to_speech, string_audio, split_string
from content.tel_caffs import ques_ans

folname = "web_caffzunk"
files_loc = create_folder(folname)

qspace = "\n\n\n\t"
video_clips = []
quse_length = []
com_clip = []
def generate_question_with_audio(question):
	textseg = []
	filenames = []
	gapduration = 1500
	qaud = f"que_audio_{idx}.mp3"

	reformatques = split_string(f"{question}", "caffairs")
	quse_length.append(reformatques[1])
	if (len(question) < 90):
		text_to_speech(question, files_loc + qaud)
	else:
		string_audio(question, files_loc + qaud)
	que_duration = AudioSegment.from_file(files_loc + qaud, format="mp3") + AudioSegment.silent(duration=gapduration)
	que_duration.export(files_loc + qaud, format="mp3")

	textseg.append(qspace + reformatques[0])
	filenames.append(f"{idx}_question.mp3")

	q_style = {'font': 'Vani-bold', 'fontsize': 38, 'color': '#ffffff', 'align': 'west'}

	tclipquestion = textseg[0] + " " * 20
	if (len(tclipquestion) < 100):
		newlen = 100-len(tclipquestion)
		tclipquestion = tclipquestion + (" " * newlen)

	audques = AudioFileClip(files_loc+qaud).duration

	question_clip = TextClip(textseg[0], **q_style).set_duration(audques)
	question_clip =  question_clip.set_audio(AudioFileClip(files_loc+qaud).set_duration(audques))

	# Concatenate video clips
	return concatenate_videoclips([question_clip])

cres = 0  # Initialize cres before the loop
comid = []  # Initialize comid as an empty list
queslen = len(quse_length)-1
for idx, x in enumerate(quse_length):
    print(idx, x)
    cres += x
    if cres >= 6:
        comid.append(idx)
        cres = 0  # Reset cres to 0 when it exceeds 7
if queslen not in quse_length:
    comid.append(queslen)

for idx, question in enumerate(ques_ans, 1):
	video = generate_question_with_audio(question)
	com_clip.append(video)

	# video = concatenate_videoclips([question_clip, qopt_a, qopt_b, qopt_c, qopt_d, answer_clip])
	# video_clips.append(video)
# print(quse_length)



# for idx, x in enumerate(quse_length):
# 	# Concatenate video clips
# 	video = concatenate_videoclips([question_clip, qopt_a, qopt_b, qopt_c, qopt_d, answer_clip])
# 	video_clips.append(video)

# final_video = concatenate_videoclips(video_clips)
# image_clip = ImageClip("image/telugu/caffairs.png").set_duration(final_video.duration)
# final_clip = CompositeVideoClip([image_clip,final_video])
#
# fname = str(datetime.now().strftime('%Y%m%d%H%M%S'))+'.mp4';
# final_clip.write_videofile(fname,codec="libx264",fps=24)

# time.sleep(5)
# delete_folder(folname)
