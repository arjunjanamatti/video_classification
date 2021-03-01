import subprocess
import time
# result = subprocess.run('ffmpeg -i C:/Users/Arjun Janamatti/PycharmProjects/video_classification/sample_video.mp4 sample_video.mp4')
# print(result)

def get_codecs():
    start = time.perf_counter()
    cmd = "ffmpeg -codecs"
    # x = subprocess.check_output(["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe", "-i", "sample_video.mp4", "sample_video_1.mp4"], shell=True)
    # x = subprocess.check_output(["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe", "-i", "sample_video.mp4", '-c:v','libx264',
    #                              '-preset', 'superfast','-b:a', '256k', '-vf', '-c:a','aac', "sample_video_1.mp4"], shell=True)
    # x = subprocess.check_output(["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe", "-i", "sample_video.mp4",
    #                              "-vcodec", "msmpeg4v2", "-acodec", "copy", "sample_video_1.mp4"],shell=True)
    # x = subprocess.check_output(["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe", "-i", "sample.mp4",
    #                              "-vcodec", "libx265", "-crf", "30", "sample_1.mp4"],shell=True)
    # video_info = 'ffmpeg -i video.mp4'
    command_0 = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", "sample.mp4", "-vcodec", "h264", "-acodec", "aac", "-preset", "ultrafast","sample_1.mp4"]
    # ffmpeg -i video.mp4 -vcodec h264 -b:v 1000k -acodec mp3 output.mp4
    command_1 = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", "sample.mp4", "-vcodec", "h264", "-b:v", "1000k","-acodec", "mp3", "-preset", "ultrafast","sample_1.mp4"]
    command_2 = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", "sample.mp4", "-vcodec", "h264", "-acodec", "mp2", "-preset", "ultrafast","sample_1.mp4"]
    command_3 = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", "sample.mp4", "-vcodec", "h264", "-acodec", "mp3", "-preset", "ultrafast","sample_1.mp4"]
    command_4 = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", "sample.mp4", "-vcodec", "h264", "-b:v", "1000k","-acodec", "mp3", "-preset", "ultrafast","sample_1.mp4"]
    command_5 = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", "sample.mp4", "-vcodec", "libx265", "-crf", "30", "-preset", "ultrafast","sample_1.mp4"]
    command_6 = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", "sample.mp4", "-vcodec", "libx264", "-crf", "30", "-preset", "ultrafast","sample_1.mp4"]
    command_7 = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", "sample.mp4", "-vcodec", "libx264", "-crf", "35", "-preset", "ultrafast","sample_1.mp4"]
    command_8 = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", "sample.mp4", "-vcodec", "libx264", "-crf", "40", "-preset", "ultrafast","sample_1.mp4"]
    command_9 = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", "sample.mp4", "-vcodec", "libx264", "-crf", "30", "-preset", "fast","sample_1.mp4"]
    command_10 = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", "sample.mp4", "-vcodec", "libx264", "-crf", "30", "sample_1.mp4"]
    compress_video = subprocess.check_output(command_10, shell=True)
    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} seconds(s) ')


def compress_without_base_64(video):
    start = time.perf_counter()
    command = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
                 "-i", f"{video}", "-vcodec", "libx264", "-crf", "45", "temp_output.mp4"]
    compress_video = subprocess.check_output(command, shell=True)
    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} seconds(s) ')
    pass

def compress_wit_base_64():
    start = time.perf_counter()
    # command = ["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe",
    #              "-i", f"{video}", "-vcodec", "libx264", "-crf", "45", "temp_output.mp4"]
    # compress_video = subprocess.check_output(command, shell=True)

    import base64

    with open("temp_output.mp4", "rb") as videoFile:
        text = base64.b64encode(videoFile.read())
        print(text)
        file = open("temp_output.txt", "wb")
        file.write(text)
        file.close()

        fh = open("video.mp4", "wb")
        fh.write(base64.b64decode(text))
        fh.close()

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} seconds(s) ')
    pass


compress_wit_base_64()
# get_codecs()

# # original video: 381mb, command_10, reduced_video_size: 155mb , time_taken: 1200 seconds
# # original video: 381mb, command_9, reduced_video_size: 157mb , time_taken: 986 seconds
# # original video: 381mb, command_8, reduced_video_size: 115mb , time_taken: 169 seconds
# # original video: 381mb, command_7, reduced_video_size: 197mb , time_taken: 169 seconds
# # original video: 381mb, command_6, reduced_video_size: 350mb , time_taken: 169 seconds
# # original video: 381mb, command_3, reduced_video_size: 800mb , time_taken: 230 seconds
# # original video: 381mb, command_5, reduced_video_size: 98.5mb , time_taken: 830 seconds
# # original video: 381mb, command_4, reduced_video_size: 259mb , time_taken: 244 seconds
# # original video: 381mb, command_2, reduced_video_size: 859mb , time_taken: 192 seconds
# # original video: 381mb, command_0, reduced_video_size: 326mb , time_taken: 1900 seconds
# # original video: 381mb, -crf 30, reduced_video_size: 124mb , time_taken: 1962 seconds
# # original video: 381mb, -crf 45, reduced_video_size: 47mb , time_taken: 1705 seconds
# # original video: 381mb, -crf 35, reduced_video_size: 100mb , time_taken: 1003 seconds
# # ffmpeg -i input.mp4 -vcodec libx264 -crf 35 output.mp4 -- 50.2mb [reduced file size] time taken is 477 seconds
# # ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4 -- 78.6mb [reduced file size] time taken is 500 seconds
# # ffmpeg -i input.mp4 -vcodec libx264 -crf 18 output.mp4 -- 172mb
# # ffmpeg -i input.mp4 -vcodec libx264 -crf 20 output.mp4 -- 142mb
# # ffmpeg -i input.avi -vcodec msmpeg4v2 -acodec copy output.avi
# # ffmpeg -i sample_video.mp4 -c:v libx264 -preset superfast -b:a 256k -vf -b:v 1.5M -c:a aac sample_video_1.mp4
# # ffmpeg -i <inputfilename> -s 640x480 -b:v 512k -vcodec mpeg1video -acodec copy <outputfilename>
# get_codecs()

from subprocess import Popen, PIPE

# p = Popen(["C:/PATH_programs/ffmpeg-4.3.2-2021-02-20-full_build/bin/ffmpeg.exe", "-i", "sample.mp4", "-hide_banner"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
# output, err = p.communicate(b"input data that is passed to subprocess' stdin")
# rc = p.returncode
# print(p.returncode, p.stdout, p.stderr)

#filters output
