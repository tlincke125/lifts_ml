import cv2
import os

"""
Extracts JPG images from frames
I know you can work on videos - but this just makes it easier to
think about and work with for a cv beginner like me
"""


# Files are named ./good/lift_{index}/frame{i}.jpg
# index is good_index or bad_index
# i is the frame index of the video
good_index = 0
bad_index = 0

# Iterate through all the movies in this directory
for video in os.listdir("./"):
    sp = os.path.splitext(video)
    di = ""

    if sp[1] != ".mp4":
        continue

    # Good lift
    if "good" in sp[0].lower():
        di = f"./good/lift_{good_index}"
        if not os.path.isdir(di):
            os.mkdir(di)
        good_index += 1

    # Bad lift
    elif "bad" in sp[0].lower():
        di = f"./bad/lift_{bad_index}"
        if not os.path.isdir(di):
            os.mkdir(di)
        bad_index += 1
    else:
        print("Oh No! ", sp[0])

    # Create a video capture and write the video to the folder 
    vidcap = cv2.VideoCapture(video)
    success, image = vidcap.read()
    count = 0
    while success:
        filename = os.path.join(di, f"frame{count}.jpg")
        cv2.imwrite(filename, image)     # save frame as JPEG file      
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1
