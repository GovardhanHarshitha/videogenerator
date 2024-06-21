# -*- coding: utf-8 -*-

from moviepy.editor import *
from pydub import AudioSegment
import time
from datetime import datetime
from reuse.telcommon import split_string, text_to_speech, create_folder, string_audio, delete_folder
from content.tel_shorts import ques_ans

#Configuration
video_clips = []
# question_css = {'font':'Vani-bold', 'fontsize':80, 'color':'#F00000', 'align':'west'}
# answer_css = {'font':'Vani-bold', 'fontsize':80, 'color':'#11AB59', 'align':'west'}
question_css = {'font':'Vani-bold', 'fontsize':75, 'color':'#65fff2', 'align':'west'}
answer_css = {'font':'Vani-bold', 'fontsize':75, 'color':'#edd36c', 'align':'west'}

folname = "shorts_zunk"
files_loc = create_folder(folname)

# ques_ans = [
#     ("తొలివేదకాలంలో గోవులు, గడ్డి భూముల కొరకు జరిగే యుద్ధాలను ఏమని పిలిచేవారు ?", "ముష్టి యుద్ధాలు", "కర్ర యుద్ధాలు", "గవిస్తి", "రాతి యుద్ధాలు", "గవిస్తి"),
# ]

for idx, qa in enumerate(ques_ans, 1):
    question = qa[0]
    answer = qa[-1]
    # print(question)
    # print(answer)
    qinfo = split_string(f"{question}", "short")
    ainfo = split_string(f"{answer}", "short")
    print_ques = "\t"+qinfo[0]
    print_ans = "\n\t"+ainfo[0]
    gapduration = AudioSegment.silent(duration=1000)
    print(f"{idx}: Processing.... ")
    #Question Audio Generation
    questionaudio = f"{idx}question.mp3"
    if (len(question) < 86):
        text_to_speech(question, files_loc+questionaudio)
    else:
        string_audio(question, files_loc+questionaudio)
    que_duration = AudioSegment.from_file(files_loc+questionaudio, format="mp3")+gapduration+ 5
    que_duration = que_duration.speedup(1.3,100,25)
    que_duration.export(files_loc+questionaudio, format="mp3")
    qes_duration_time = AudioFileClip(files_loc+questionaudio).duration

    #Answer Audio Generation
    answeraudio = f"{idx}answer.mp3"
    text_to_speech(answer, files_loc+answeraudio)
    ans_duration = AudioSegment.from_file(files_loc+answeraudio, format="mp3")+gapduration+ 5
    ans_duration = ans_duration.speedup(1.3,100,25)

    ans_duration.export(files_loc+answeraudio, format="mp3")
    ans_duration_time = AudioFileClip(files_loc+answeraudio).duration

    #Total Audio
    fullaudio = f"{idx}questionanswer.mp3"
    qans_duration = que_duration + ans_duration
    qans_duration.export(files_loc+fullaudio, format="mp3")
    qans_duration_time = AudioFileClip(files_loc+fullaudio).duration

    image_clip = TextClip(" ", size=(1100, None)).set_duration(qans_duration_time)

    question_title = TextClip(f"ప్రశ్న:", **question_css)
    question_title_pos = question_title.set_position((80,500))
    quetit_duration = question_title_pos.set_duration(qans_duration_time)

    question_clip = TextClip(print_ques, **question_css)
    question_pos = question_clip.set_position((80,600))
    qclip_duration = question_pos.set_duration(qans_duration_time)

    answer_title = TextClip(f"\nసమాధానము:", **answer_css)
    answer_title_pos = answer_title.set_position((100,700+(qinfo[1]*100)))
    answer_title_pos = answer_title_pos.set_start(qes_duration_time)
    anstit_duration = answer_title_pos.set_duration(ans_duration_time)

    answer_clip = TextClip(print_ans, **answer_css)
    answer_pos = answer_clip.set_position((80,800+(qinfo[1]*100)))
    answer_pos = answer_pos.set_start(qes_duration_time)
    aclip_duration = answer_pos.set_duration(ans_duration_time)

    final_clip = CompositeVideoClip([image_clip, quetit_duration, qclip_duration, anstit_duration, aclip_duration])
    final_clip = final_clip.set_audio(AudioFileClip(files_loc+fullaudio))
    video_clips.append(final_clip)

final_video = concatenate_videoclips(video_clips)
image_clip = ImageClip("image/telugu/shorts.webp").set_duration(final_video.duration)
final_clip = CompositeVideoClip([image_clip,final_video])

fname = str(datetime.now().strftime('%Y%m%d%H%M%S'))+'.mp4'
final_clip.write_videofile(fname,codec="libx264",fps=24)

time.sleep(5)
delete_folder(folname)
