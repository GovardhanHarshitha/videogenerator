# -*- coding: utf-8 -*-

from gtts import gTTS
from pydub import AudioSegment
import os
from datetime import datetime
import stat
import shutil

def split_string(orgtext,type):
	lines = []
	resInfo = []
	trimmed_text = orgtext.strip()
	text = trimmed_text.replace(",", ", ")
	words = text.split()
	current_line = []
	if ((type == "web") or (type == "lweb") or (type == "caffairs")):
		max_length=74
	elif (type == "short"):
		max_length=26
	else:
		max_length=50

	for indword in words:
		word = indword.strip()
		if len(' '.join(current_line + [word])) <= max_length:
			current_line.append(word)
		else:
			lines.append(' '.join(current_line))
			current_line = [word]

	if current_line:
		lines.append(' '.join(current_line))

	result = '\n\t'.join(lines)
	if ((type == "short") or (type == "lweb") or (type == "caffairs")):
		resInfo.append(result)
		resInfo.append(len(lines))
		return resInfo
	return result


def string_audio(orgtext,filename):
	segments = []
	max_length = 74
	trimmed_text = orgtext.strip()
	text = trimmed_text.replace(",", ", ")
	words = text.split()
	current_line = []
	audio_segments = []

	# Split stringInfo into segments of max 90 characters
	for word in words:
		if len(' '.join(current_line + [word])) <= max_length:
			current_line.append(word)
		else:
			segments.append(' '.join(current_line))
			current_line = [word]
	if current_line:
	 	segments.append(' '.join(current_line))

	for segment in segments:
		temp_file = "temp.mp3"
		text_to_speech(segment, temp_file)
		audio_segments.append(AudioSegment.from_mp3(temp_file))

		# Clean up the temp file after using
		os.remove(temp_file)
	combined_audio = AudioSegment.empty()
	for segment in audio_segments:
		combined_audio += segment

	# Export the combined audio as a single audio file (e.g., output.mp3)
	combined_audio.export(filename, format="mp3")
	return

def delete_files(filenames):
	#folder_path = 'D:/Python/Workspace/videogenerator'
	folder_path = os.getcwd()
	for filename in filenames:
		# Construct the full path to the file
		file_path = os.path.join(folder_path,filename)
		# Check if the file exists before attempting to delete it
		try:
			# Attempt to remove the file
			os.remove(file_path)
		except PermissionError as e:
			print(f"PermissionError: {e}.Cannot delete {filename}.")
		except FileNotFoundError as e:
			print(f"FileNotFoundError: {e}.{filename} not found.")
		except Exception as e:
			print(f"An error occurred while deleting {filename}: {e}")


def text_to_speech(text,filename):
	tts = gTTS(text=text,lang='te')
	tts.save(filename)

def create_folder(path):
    folname = str(datetime.now().strftime('%Y%m%d%H%M%S'))
    folder_path = path+"/"+folname
    files_loc = folder_path+"/"
    # Create the folder
    os.makedirs(folder_path, exist_ok=True)
    # Set full access permissions (read, write, execute) for owner, group, and others
    os.chmod(folder_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    return files_loc

def delete_folder(folname):
	folder_path = os.getcwd() + '/'+folname
	try:
		shutil.rmtree(folder_path)
		print(f"Deleted the folder: {folname}")
	except Exception as e:
		print(f"Error deleting the folder: {str(e)}")
