import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


print(setuptools.find_packages())

setuptools.setup(
    name='pyvidcompress',
    version='0.0.4',
    author="Dimuthu Upeksha, Chathura Widanage",
    author_email="dimuthu.upeksha2@gmail.com, chathurawidanage@gmail.com",
    description="Tensor decomposition based video compression library for CPUs and GPUs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chathurawidanage/pyvidcompress",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy',
        'opencv-python',
        'matplotlib',
        'tensorly',
        'torch',
        'scikit-video',
        'cloudpickle'
    ],
)
