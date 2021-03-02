from algorithms.cp import CPDecoder, CPEncoder
from base.encoder import Encoder
from algorithms.tucker import TuckerDecoder, TuckerEncoder, TuckerTdv
from base.config import Config
from base.util import calculate_psnr, claculate_compression_ratio

# TUCKER DECOMPOSITION

# initialize stateless encoder and decoder
conf = Config()
conf.set("ranks", [20, 20, 50, 3])
tuck_coder = TuckerEncoder(conf)
tuck_decoder = TuckerDecoder(conf)

file_location = 'C:/Users/Arjun Janamatti/PycharmProjects/jeeva_project/video_and_image_classification/upload_videos/test/Obama.mp4'

# encode a file
tuck_tdv = tuck_coder.encode_file(file_location)

tuck_tdv.persist("compressed_video_tuck.tdv")
tuck_decoder.decode_to_file(tuck_tdv, "output_tuck.mp4")


# load again from file(optional)
tdv_loaded = TuckerTdv.load("compressed_video.tdv")
tuck_decoder.decode_to_file(tdv_loaded, "output_loaded.mp4")


# calculate psnr
psnr = calculate_psnr(file_location, "output_tuck.mp4")
ratio = claculate_compression_ratio(
    file_location, "output_tuck.mp4")
print("Tucker", psnr, ratio)


# CP DECOMPOSITION

# initialize stateless encoder and decoder
conf = Config()
conf.set("rank", 2)
cp_coder = CPEncoder(conf)
cp_decoder = CPDecoder(conf)

# encode a file
cp_tdv = cp_coder.encode_file(file_location)

cp_tdv.persist("compressed_video_cp.tdv")
cp_decoder.decode_to_file(cp_tdv, "output_cp.mp4")


# calculate psnr
psnr = calculate_psnr(file_location, "output_cp.mp4")
ratio = claculate_compression_ratio(
    file_location, "output_cp.mp4")
print("CP", psnr, ratio)
