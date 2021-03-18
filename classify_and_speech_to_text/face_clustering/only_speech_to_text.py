import subprocess
import time
import os


dir_loc =  'C:/Users/Arjun Janamatti/PycharmProjects/video_classification/classify_and_speech_to_text'
DEEPSPEECH_MODEL_PATH = f"{dir_loc}/deepspeech-0.9.3-models.pbmm"
DEEPSPEECH_SCORER_PATH = f"{dir_loc}/deepspeech-0.9.3-models.scorer"
ffmpeg_location = "C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe"

video = 'sample.mp4'

# command = [ffmpeg_location, "-i", f"{video}", "-ac", "1", "-ab", "16000", "-ar", "16000", "temp_output.wav"]
# print(command)
# video_to_audio = subprocess.check_output(command, shell=True)
# print(f'{video_to_audio} completed')
audio_filename = 'temp_output.wav'
proc = subprocess.Popen(
            f"deepspeech --model {DEEPSPEECH_MODEL_PATH}  --audio " + audio_filename,
            shell=True, stdout=subprocess.PIPE, )

output = proc.communicate()[0]
os.remove("temp_output.wav")
print(output)