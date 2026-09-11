import glob
import os.path
import string
import time

DATA_FOLDER = "PRE_02_mapreduce/data"
INPUT_FOLDER = "PRE_02_mapreduce/temp/input"
OUTPUT_FOLDER = "PRE_02_mapreduce/temp/output"

if os.path.exists(INPUT_FOLDER):
    for file in glob.glob(f"{INPUT_FOLDER}/*"):
        os.remove(file)
else:
    os.makedirs(INPUT_FOLDER)

n = 1000

for file in glob.glob(f"{DATA_FOLDER}/*"):

    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    for i in range(1, n + 1):

        raw_filename_with_extension = os.path.basename(file)

        raw_filename_without_extension = os.path.splitext(raw_filename_with_extension)[
            0
        ]

        new_filename = f"{raw_filename_without_extension}_{i:05d}.txt"

        with open(f"{INPUT_FOLDER}/{new_filename}", "w", encoding="utf-8") as f2:
            f2.write(text)

