import cv2
import mediapipe as mp
import time
import os
import numpy as np
import pandas as pd


verbose = True

columns = ["Video Index", "Frame Index", "Label"] + \
          [f"Joint_{id}_x" for id in range(33)] + \
          [f"Joint_{id}_y" for id in range(33)] + \
          [f"Joint_{id}_z" for id in range(33)] + \
          [f"Joint_{id}_c" for id in range(33)]

df = pd.DataFrame(columns = columns)

i = 0

good_lifts = os.listdir("./good")
bad_lifts = os.listdir("./bad")

num_lifts = len(good_lifts) + len(bad_lifts)

for video in bad_lifts:
    print(f"Video {i} of {num_lifts} (Bad) Shape: {df.shape}")

    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils
    pTime = 0
    
    for im_index in range(len(os.listdir(os.path.join("./bad", video)))):
        f = os.path.join("./bad", video, f"frame{im_index}.jpg")
        if not os.path.isfile(f):
            print("ERROR: ", f)
            continue

        img = cv2.imread(f)

        arr = {"Video Index" : str(i), "Frame Index" : im_index, "Label" : 0}

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        #print(results.pose_landmarks)

        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w,c = img.shape
            if verbose:
                print(lm)
            arr[f"Joint_{id}_x"] = lm.x
            arr[f"Joint_{id}_y"] = lm.y
            arr[f"Joint_{id}_z"] = lm.z
            arr[f"Joint_{id}_c"] = lm.visibility

            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)

        df = df.append(arr, ignore_index = True)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        if verbose:
            cv2.putText(img, str(int(fps)), (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)

    i += 1

for video in good_lifts:
    print(f"Video {i} of {num_lifts} (Good) Shape: {df.shape}")

    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils
    pTime = 0
    
    for im_index in range(len(os.listdir(os.path.join("./good", video)))):
        f = os.path.join("./good", video, f"frame{im_index}.jpg")
        if not os.path.isfile(f):
            print("ERROR: ", f)
            continue

        img = cv2.imread(f)

        arr = {"Video Index" : str(i), "Frame Index" : im_index, "Label" : 1}

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        #print(results.pose_landmarks)

        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w,c = img.shape
            if verbose:
                print(lm)
            arr[f"Joint_{id}_x"] = lm.x
            arr[f"Joint_{id}_y"] = lm.y
            arr[f"Joint_{id}_z"] = lm.z
            arr[f"Joint_{id}_c"] = lm.visibility

            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)

        df = df.append(arr, ignore_index = True)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        if verbose:
            cv2.putText(img, str(int(fps)), (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)

    i += 1


df.to_csv("./data.csv")
