# pip install setuptools
# pip install ./

import sys

if (sys.version_info.major < 3):
    print('PYTHON VERSION MUST BE 3 OR GREATER!!')
    exit(1)


from setuptools import setup, find_packages

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setup(
    name="zdiscord",
    version="0.0.1",
    author="Zach McFadden",
    author_email="zrmmaster92@gmail.com",
    description="A discord bot with a generic integration framework, configurable via JSON",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/xxdunedainxx/zdiscord",
    install_requires=["requests", "discord"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)