import sys
import multiprocessing


from PIL import Image
import numpy as np
from scipy import linalg as LA
import cv2
import imageio
import tqdm

BEST_PERCENT = 0.2

def pixelate_image(image, percent):
    A = image
    m, n = A.shape
    U, S, V_t = LA.svd(A)
    best = np.array(sorted(enumerate(S), key=lambda x: x[1], reverse=True))
    x = list(best.shape)[0]
    reduced = int(x*percent)
    best = best[reduced:]
    sigma = np.zeros((m, n))
    sigma[:m, :m] = np.diag(S)
    for index, _ in best:
        index = int(index)
        sigma[index, index] = 0

    return U.dot(sigma.dot(V_t))

def color_worker(frame, percent, color, allframes):
    # print("Started work on",color)
    processed = pixelate_image(frame, percent)
    allframes[color] = processed

def process_image(filename, output_file='result.png'):
    data = Image.open(filename).convert('L')
    data = np.matrix(data)
    result = pixelate_image(data, BEST_PERCENT)
    saver = Image.fromarray(result)
    saver = saver.convert("L")
    saver.save(output_file)

def color_pixelate_parallel(frame, percent):
    b, g, r = cv2.split(frame)
    jobs = []
    manager = multiprocessing.Manager()
    allframes = manager.dict()
    for f, col in ((b,'b'), (g,'g'), (r,'r')):
        p = multiprocessing.Process(target=color_worker, args=(f, percent, col, allframes))
        jobs.append(p)
        p.start()
    for process in jobs:
        process.join()
    b = allframes['b']
    g = allframes['g']
    r = allframes['r']
    return cv2.merge((b, g, r))

def get_specs(read_cap):
    # Get specifics of video
    if read_cap.isOpened():
        height = int(read_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(read_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        count = read_cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = read_cap.get(cv2.CAP_PROP_FPS)
        print(f"height: {height}, width: {width}, count: {count}, fps: {fps}")
        return (height, width, count, fps)
    else:
        return (None, None, None, None)

def process_video(filename, output_file='1999.mp4'):
    cap_read = cv2.VideoCapture(filename)
    (height, width, total_frames, fps) = get_specs(cap_read)
    writer = imageio.get_writer(output_file, fps=fps)
    frame_count = 0
    ret_bool = True
    pro_bar = tqdm.tqdm(total=total_frames)
    while cap_read.isOpened() and ret_bool:
        ret_bool, frame = cap_read.read()
        if ret_bool:
            frame_count += 1
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # fixed_frame = pixelate_image(gray_frame, BEST_PERCENT).astype(np.uint8)
            fixed_frame = color_pixelate_parallel(frame, BEST_PERCENT).astype(np.uint8)
            writer.append_data(fixed_frame)
            pro_bar.update(1)
    pro_bar.close()
    cap_read.release()
    writer.close()
    cv2.destroyAllWindows()


def main():
    print(sys.argv)
    if(len(sys.argv) <= 3):
        return print("Usage: compress.py [i|v] [input filename] [output filename]\
                \n       i -> image, v -> video")
    filename = sys.argv[2]
    output_filename = sys.argv[3]
    if sys.argv[1] == 'i':
        process_image(filename, output_filename)
        print("output file at:",'result.png')
    elif sys.argv[1] == 'v':
        process_video(filename, output_filename)
        print("output file at:",'1999.mp4')
    else:
        print("Invalid use")

if __name__ == "__main__":
    main()
