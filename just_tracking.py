import imageio.v2 as imageio
import matplotlib.pyplot as plt
import yaml
import numpy as np
from PIL import Image
import time
import keyboard
from pynput import keyboard
import multiprocessing
import cv2
from picamera2 import Picamera2



def initialize_camera():
    picam = Picamera2()
    picam.preview_configuration.main.size=(250, 200)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    return picam

def take_picture(picam: Picamera2):
    return picam.capture_array()

def track_prisioner(frame,contour_history):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([0, 100, 100])
    upper_orange = np.array([20, 255, 255])
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    detected=False
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 400:  # You can adjust this threshold based on your application
            epsilon = 0.1*cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4:
                cv2.drawContours(frame, [approx], 0, (0, 0, 255), 4)
                detected=True

                contour_history.append(approx.ravel()
                                       )
                
    for i in range(1, len(contour_history)):
        cv2.line(frame, (contour_history[i - 1][0], contour_history[i - 1][1]),
                (contour_history[i][0], contour_history[i][1]), (0, 255, 0), 2)

    return frame, detected



if __name__ == "__main__":
    picam = initialize_camera()
    contour_history = []
    while True:
        frame= take_picture(picam)
        frame, detected = track_prisioner(frame,contour_history)

     

        cv2.imshow("CAMERA SECTOR C", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()