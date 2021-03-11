import sox
# get the sample rate
n_samples = sox.file_info.sample_rate('test(2).wav')
print(n_samples)
