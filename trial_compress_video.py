import subprocess
# result = subprocess.run('ffmpeg -i C:/Users/Arjun Janamatti/PycharmProjects/video_classification/sample_video.mp4 sample_video.mp4')
# print(result)

def get_codecs():
    cmd = "ffmpeg -codecs"
    # x = subprocess.check_output(["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe", "-i", "sample_video.mp4", "sample_video_1.mp4"], shell=True)
    # x = subprocess.check_output(["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe", "-i", "sample_video.mp4", '-c:v','libx264',
    #                              '-preset', 'superfast','-b:a', '256k', '-vf', '-c:a','aac', "sample_video_1.mp4"], shell=True)
    x = subprocess.check_output(["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe", "-i", "sample_video.mp4",
                                 "-vcodec", "msmpeg4v2", "-acodec", "copy", "sample_video_1.mp4"],shell=True)
    print(x)
    # x = x.split(b'\n')
    # for e in x:
    #     print(e)

# ffmpeg -i input.mp4 -vcodec libx264 -crf 20 output.mp4
# ffmpeg -i input.avi -vcodec msmpeg4v2 -acodec copy output.avi
# ffmpeg -i sample_video.mp4 -c:v libx264 -preset superfast -b:a 256k -vf -b:v 1.5M -c:a aac sample_video_1.mp4
# ffmpeg -i <inputfilename> -s 640x480 -b:v 512k -vcodec mpeg1video -acodec copy <outputfilename>
get_codecs()