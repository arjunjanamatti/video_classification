import subprocess
# result = subprocess.run('ffmpeg -i C:/Users/Arjun Janamatti/PycharmProjects/video_classification/sample_video.mp4 sample_video.mp4')
# print(result)

def get_codecs():
    cmd = "ffmpeg -codecs"
    x = subprocess.check_output(["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe", "-i", "sample_video.mp4", "sample_video_1.mp4"], shell=True)
    print(x)
    # x = x.split(b'\n')
    # for e in x:
    #     print(e)

# ffmpeg -i <inputfilename> -s 640x480 -b:v 512k -vcodec mpeg1video -acodec copy <outputfilename>
get_codecs()