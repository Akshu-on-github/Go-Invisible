#!/usr/bin/env python3

import speech_recognition as sr
import cv2
import numpy as np
import time

# Notes:

## The magic word is *please*

## The turnInvisible function has drawn inspiration from https://www.geeksforgeeks.org/invisible-cloak-using-opencv-python-project/


def turnInvisible():
    video_capture = cv2.VideoCapture(0)
    time.sleep(3)
    background=0
    for i in range(30):
        ret,background = video_capture.read()

    background = np.flip(background,axis=1)

    while(video_capture.isOpened()):
        # stored in a numpy array
        ret, img = video_capture.read()
        
        # TODO: Delete if not needed - else, the wrong pixels will be replaced
        img = np.flip(img,axis=1)
        
        # Converting image to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        value = (35, 35)
        
        blurred = cv2.GaussianBlur(hsv, value,0)
        
	      # Detecting Red - lower range
        lower_red = np.array([0,120,70])
        upper_red = np.array([10,255,255])
        mask1 = cv2.inRange(hsv,lower_red,upper_red)
        
        # Detecting Red - upper range
        lower_red = np.array([170,120,70])
        upper_red = np.array([180,255,255])
        mask2 = cv2.inRange(hsv,lower_red,upper_red)
        
        # Creating the final mask
        mask = mask1+mask2
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
        
        # Replacing red pixels in cloak with background pixels
        img[np.where(mask==255)] = background[np.where(mask==255)]
        cv2.imshow('Display',img)
        k = cv2.waitKey(10)
        if k == 27:
            break


def sayTheMagicWord():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("What's the magic word?")
        audio = r.listen(source)
    
    # recognize speech using Google Speech Recognition
    try:
        magic_word = r.recognize_google(audio)
        if magic_word == "please":
            print("Did I hear please?")
            time.sleep(1)
            print("Very well young'un, press enter")
            turnInvisible()
        else:
            print("Either these old ears are woosey, or you just said " + magic_word)
            sayTheMagicWord()
    except sr.UnknownValueError:
        print("These old ears are woosey, try again?")
        sayTheMagicWord()
    except sr.RequestError as e:
        print("Hmm, I'm under the weather, try again later.")


# Introductory text
print("What's this?")
time.sleep(1)
print("I hear that you want to turn invisible?")
time.sleep(1)

sayTheMagicWord()
