# -*- coding: utf-8 -*-

from moviepy.editor import *
from pydub import AudioSegment
import time
from datetime import datetime
from reuse.engcommon import split_string, text_to_speech, create_folder, string_audio, delete_folder
from content.eng_shorts import ques_ans

#Configuration
video_clips = []
question_css = {'font':'Tahoma', 'fontsize':55, 'color':'#F00000', 'align':'west'}
answer_css = {'font':'Tahoma', 'fontsize':55, 'color':'#F00000', 'align':'west'}

folname = "eng_shorts"
files_loc = create_folder(folname)

# ques_ans = [
#     ("తొలివేదకాలంలో గోవులు, గడ్డి భూముల కొరకు జరిగే యుద్ధాలను ఏమని పిలిచేవారు ?", "ముష్టి యుద్ధాలు", "కర్ర యుద్ధాలు", "గవిస్తి", "రాతి యుద్ధాలు", "గవిస్తి"),
# ]

for idx, qa in enumerate(ques_ans, 1):
    question = qa[0]
    options = qa[1:-1]
    answer = qa[-1]

    qinfo = split_string(f"{question}", "short")
    qopt1 = split_string(f"{options[0]}", "short")
    qopt2 = split_string(f"{options[1]}", "short")
    qopt3 = split_string(f"{options[2]}", "short")
    qopt4 = split_string(f"{options[3]}", "short")
    ainfo = split_string(f"{answer}", "short")

    print_ques = "\t"+qinfo[0]
    print_qopt1 = "\t a) "+qopt1[0]
    print_qopt2 = "\t b) "+qopt2[0]
    print_qopt3 = "\t c) "+qopt3[0]
    print_qopt4 = "\t d) "+qopt4[0]
    print_ans = "\t"+ainfo[0]

    gapduration = AudioSegment.silent(duration=1000)

    #Question Audio Generation
    questionaudio = f"{idx}question.mp3"
    if (len(question) < 90):
        text_to_speech(question, files_loc+questionaudio)
    else:
        string_audio(question, files_loc+questionaudio)
    que_duration = AudioSegment.from_file(files_loc+questionaudio, format="mp3")+gapduration
    que_duration.export(files_loc+questionaudio, format="mp3")
    qes_duration_time = AudioFileClip(files_loc+questionaudio).duration

    #Options Audio Generation
    optaudioa = f"{idx}optiona.mp3"
    text_to_speech(options[0], files_loc+optaudioa)
    opt1_duration = AudioSegment.from_file(files_loc+optaudioa, format="mp3")+gapduration
    opt1_duration.export(files_loc+optaudioa, format="mp3")
    opt1_duration_time = AudioFileClip(files_loc+optaudioa).duration

    optaudiob = f"{idx}optionb.mp3"
    text_to_speech(options[1], files_loc+optaudiob)
    opt2_duration = AudioSegment.from_file(files_loc+optaudiob, format="mp3")+gapduration
    opt2_duration.export(files_loc+optaudiob, format="mp3")
    opt2_duration_time = AudioFileClip(files_loc+optaudiob).duration

    optaudioc = f"{idx}optionc.mp3"
    text_to_speech(options[2], files_loc+optaudioc)
    opt3_duration = AudioSegment.from_file(files_loc+optaudioc, format="mp3")+gapduration
    opt3_duration.export(files_loc+optaudioc, format="mp3")
    opt3_duration_time = AudioFileClip(files_loc+optaudioc).duration

    optaudiod = f"{idx}optiond.mp3"
    text_to_speech(options[3], files_loc+optaudiod)
    opt4_duration = AudioSegment.from_file(files_loc+optaudiod, format="mp3")+gapduration
    opt4_duration.export(files_loc+optaudiod, format="mp3")
    opt4_duration_time = AudioFileClip(files_loc+optaudiod).duration

    #Answer Audio Generation
    answeraudio = f"{idx}answer.mp3"
    text_to_speech(answer, files_loc+answeraudio)
    ans_duration = AudioSegment.from_file(files_loc+answeraudio, format="mp3")+gapduration
    ans_duration.export(files_loc+answeraudio, format="mp3")
    ans_duration_time = AudioFileClip(files_loc+answeraudio).duration

    #Question Options Audio
    qoptaudio = f"{idx}questionoption.mp3"
    qopt_duration = que_duration + opt1_duration + opt2_duration + opt3_duration + opt4_duration
    qopt_duration.export(files_loc+qoptaudio, format="mp3")
    qopt_duration_time = AudioFileClip(files_loc+qoptaudio).duration

    #Total Audio
    fullaudio = f"{idx}questionanswer.mp3"
    qans_duration = que_duration + opt1_duration + opt2_duration + opt3_duration + opt4_duration + ans_duration
    qans_duration.export(files_loc+fullaudio, format="mp3")
    qans_duration_time = AudioFileClip(files_loc+fullaudio).duration

    image_clip = TextClip(" ", size=(1100, None)).set_duration(qans_duration_time)

    question_title = TextClip(f"Question:", **question_css)
    question_title_pos = question_title.set_position((80,200))
    quetit_duration = question_title_pos.set_duration(qans_duration_time)

    question_clip = TextClip(print_ques, **question_css)
    question_pos = question_clip.set_position((80,300))
    qclip_duration = question_pos.set_duration(qans_duration_time)

    opt1_clip = TextClip(print_qopt1, **question_css)
    opt1_pos = opt1_clip.set_position((80,180+(qinfo[1]*100)))
    opt1_duration = opt1_pos.set_duration(qans_duration_time)

    opt2_clip = TextClip(print_qopt2, **question_css)
    opt2_pos = opt2_clip.set_position((80,280+(qinfo[1]*100)))
    opt2_duration = opt2_pos.set_duration(qans_duration_time)

    opt3_clip = TextClip(print_qopt3, **question_css)
    opt3_pos = opt3_clip.set_position((80,380+(qinfo[1]*100)))
    opt3_duration = opt3_pos.set_duration(qans_duration_time)

    opt4_clip = TextClip(print_qopt4, **question_css)
    opt4_pos = opt4_clip.set_position((80,480+(qinfo[1]*100)))
    opt4_duration = opt4_pos.set_duration(qans_duration_time)

    answer_title = TextClip(f"Answer:", **answer_css)
    answer_title_pos = answer_title.set_position((100,680+(qinfo[1]*100)))
    answer_title_pos = answer_title_pos.set_start(qopt_duration_time)
    anstit_duration = answer_title_pos.set_duration(ans_duration_time)

    answer_clip = TextClip(print_ans, **answer_css)
    answer_pos = answer_clip.set_position((80,780+(qinfo[1]*100)))
    answer_pos = answer_pos.set_start(qopt_duration_time)
    aclip_duration = answer_pos.set_duration(ans_duration_time)

    final_clip = CompositeVideoClip([image_clip, quetit_duration, qclip_duration, opt1_duration, opt2_duration, opt3_duration, opt4_duration, anstit_duration, aclip_duration])
    final_clip = final_clip.set_audio(AudioFileClip(files_loc+fullaudio))
    video_clips.append(final_clip)

final_video = concatenate_videoclips(video_clips)
image_clip = ImageClip("image/english/shorts.webp").set_duration(final_video.duration)
final_clip = CompositeVideoClip([image_clip,final_video])

fname = str(datetime.now().strftime('%Y%m%d%H%M%S'))+'.mp4'
final_clip.write_videofile(fname,codec="libx264",fps=24)

time.sleep(5)
delete_folder(folname)
