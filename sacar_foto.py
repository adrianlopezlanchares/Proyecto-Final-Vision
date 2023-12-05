import cv2
from picamera2 import Picamera2
import imageio.v2 as imageio
import matplotlib.pyplot as plt
import yaml
import numpy as np
from PIL import Image
def capturar_imagen():
    picam = Picamera2()
    picam.preview_configuration.main.size=(200, 150)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    print("Enter para sacar foto")
    num = input()
    frame = picam.capture_array()
    frame = Image.fromarray(frame)
    frame.save(f"foto{num}.jpg")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capturar_imagen()