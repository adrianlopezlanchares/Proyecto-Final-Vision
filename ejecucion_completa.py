import cv2
from picamera2 import Picamera2
import imageio.v2 as imageio
import matplotlib.pyplot as plt
import yaml
import numpy as np
from PIL import Image
import time
import keyboard
from pynput import keyboard
import multiprocessing
from pynput import keyboard as pynput_keyboard

TimeSinceDetected = 0


def initialize_camera():
    picam = Picamera2()
    picam.preview_configuration.main.size = (300, 275)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    return picam


def take_picture(picam: Picamera2):
    return picam.capture_array()


def detect_blue_square(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    detected = False
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1500:  # You can adjust this threshold based on your application
            epsilon = 0.05*cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4:
                # cv2.drawContours(frame, [approx], 0, (0, 0, 255), 5)
                detected = True
    return frame, detected


def detect_yellow_triangle(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([25, 100, 100])
    upper_yellow = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    contours = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    detected = False
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1500:  # You can adjust this threshold based on your application
            epsilon = 0.05*cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 3:
                # cv2.drawContours(frame, [approx], 0, (0, 0, 255), 5)
                detected = True
    return frame, detected


def detect_red_circle(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detected = False
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1500:  # You can adjust this threshold based on your application
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            if len(approx) > 4:  # Assuming a circular shape
                detected = True

    return frame, detected


def detect_green_square(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Adjust the lower range for green color
    lower_green = np.array([60, 100, 100])
    # Adjust the upper range for green color
    upper_green = np.array([120, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    contours = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    detected = False

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1500:  # You can adjust this threshold based on your application
            epsilon = 0.05 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) > 3:
                detected = True

    return frame, detected


def detect_pattern(frame, pattern_detector):
    # Función genérica para detectar un patrón utilizando el detector específico
    return pattern_detector(frame)


def detect_pattern_within_time(frame, detect_function, timeout):
    start_time = time.time()
    detected = False

    while time.time() - start_time < timeout:
        frame, detected = detect_pattern(frame, detect_function)
        cv2.imshow("Camera Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if detected:
            break

    return detected


def show_camera_frame(picam):
    # Función para mostrar la imagen de la cámara en tiempo real
    while True:
        frame = take_picture(picam)
        cv2.imshow("Camera Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def track_prisioner(frame, contour_history):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([0, 100, 100])
    upper_orange = np.array([20, 255, 255])
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    contours = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    detected = False
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 200:  # You can adjust this threshold based on your application
            epsilon = 0.1*cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4:
                cv2.drawContours(frame, [approx], 0, (0, 0, 255), 4)
                detected = True

                contour_history.append(approx.ravel()
                                       )

    for i in range(1, len(contour_history)):
        cv2.line(frame, (contour_history[i - 1][0], contour_history[i - 1][1]),
                 (contour_history[i][0], contour_history[i][1]), (0, 255, 0), 2)

    return frame, detected


def wait_for_enter():
    with pynput_keyboard.Listener(on_press=lambda key: None if key == pynput_keyboard.Key.enter else False) as listener:
        listener.join()


def main():
    contour_history = []
    picam = initialize_camera()

    STATES = ["yellow_triangle", "blue_square", "red_circle", "green_square"]
    current_state = 0  # Start with the first pattern in the sequence

    print("Looking for pattern 1:")

    startTime = time.time()
    TimeSinceDetected = startTime

    while current_state < len(STATES):

        frame = take_picture(picam)

        if STATES[current_state] == "yellow_triangle":
            # detected = detect_pattern_within_time(frame, detect_yellow_triangle, 15)  # 15-second timeout
            _, detected = detect_yellow_triangle(frame)
        elif STATES[current_state] == "blue_square":
            # detected = detect_pattern_within_time(frame, detect_blue_square, 15)
            _, detected = detect_blue_square(frame)
        elif STATES[current_state] == "red_circle":
            # detected = detect_pattern_within_time(frame, detect_red_circle, 15)
            _, detected = detect_red_circle(frame)
        elif STATES[current_state] == "green_square":
            # detected = detect_pattern_within_time(frame, detect_green_square, 15)
            _, detected = detect_green_square(frame)

        if detected:
            startTime = time.time()
            TimeSinceDetected = startTime
            current_state += 1
            print("Correct pattern detected. Now looking for pattern " +
                  str(current_state + 1) + ":")
            time.sleep(0.5)

        else:

            TimeSinceDetected += time.time() - TimeSinceDetected

            if TimeSinceDetected - startTime > 15:
                print(
                    "Pattern not detected within the time limit or wrong pattern. Resetting to initial state.")
                print("Looking for pattern 1:")
                current_state = 0
                startTime = time.time()
                TimeSinceDetected = startTime

        cv2.imshow("Camera Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Correct sequence detected. Access granted!")

    print("SECURITY SYSTEM ACTIVATED")

    cv2.destroyAllWindows()

    while True:

        frame = take_picture(picam)
        frame, detected = track_prisioner(frame, contour_history)

        cv2.imshow("CAMERA SECTOR C", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()
