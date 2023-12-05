import cv2
from picamera2 import Picamera2
import imageio.v2 as imageio
import matplotlib.pyplot as plt
import yaml
import numpy as np


def cargar_fotos():
    return [imageio.imread(f"foto{i}.jpg") for i in range(2, 9)]





if __name__ == "__main__":
    picam = Picamera2()
    picam.preview_configuration.main.size=(200, 150)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    print("inicializando")

    # INICIALIZAR PARÁMETROS
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    ########################################Blob Detector##############################################

    # Setup SimpleBlobDetector parameters.
    blobParams = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    blobParams.minThreshold = 8
    blobParams.maxThreshold = 255

    # Filter by Area.
    blobParams.filterByArea = True
    blobParams.minArea = 64     # minArea may be adjusted to suit for your experiment
    blobParams.maxArea = 2500   # maxArea may be adjusted to suit for your experiment

    # Filter by Circularity
    blobParams.filterByCircularity = True
    blobParams.minCircularity = 0.1

    # Filter by Convexity
    blobParams.filterByConvexity = True
    blobParams.minConvexity = 0.87

    # Filter by Inertia
    blobParams.filterByInertia = True
    blobParams.minInertiaRatio = 0.01

    # Create a detector with the parameters
    blobDetector = cv2.SimpleBlobDetector_create(blobParams)

    ###################################################################################################

    ###################################################################################################

    # Original blob coordinates, supposing all blobs are of z-coordinates 0
    # And, the distance between every two neighbour blob circle centers is 72 centimetres
    # In fact, any number can be used to replace 72.
    # Namely, the real size of the circle is pointless while calculating camera calibration parameters.
    objp = np.zeros((44, 3), np.float32)
    objp[0]  = (0  , 0  , 0)
    objp[1]  = (0  , 30 , 0)
    objp[2]  = (0  , 60, 0)
    objp[3]  = (0  , 90, 0)
    objp[4]  = (15 , 15 , 0)
    objp[5]  = (15 , 45, 0)
    objp[6]  = (15 , 75, 0)
    objp[7]  = (15 , 105, 0)
    objp[8]  = (30 , 0  , 0)
    objp[9]  = (30 , 30 , 0)
    objp[10] = (30 , 60, 0)
    objp[11] = (30 , 90, 0)
    objp[12] = (45, 15,  0)
    objp[13] = (45, 45, 0)
    objp[14] = (45, 75, 0)
    objp[15] = (45, 105, 0)
    objp[16] = (60, 0  , 0)
    objp[17] = (60, 30 , 0)
    objp[18] = (60, 60, 0)
    objp[19] = (60, 90, 0)
    objp[20] = (75, 15 , 0)
    objp[21] = (75, 45, 0)
    objp[22] = (75, 75, 0)
    objp[23] = (75, 105, 0)
    objp[24] = (90, 0  , 0)
    objp[25] = (90, 30 , 0)
    objp[26] = (90, 60, 0)
    objp[27] = (90, 90, 0)
    objp[28] = (105, 15 , 0)
    objp[29] = (105, 45, 0)
    objp[30] = (105, 75, 0)
    objp[31] = (105, 105, 0)
    objp[32] = (120, 0  , 0)
    objp[33] = (120, 30 , 0)
    objp[34] = (120, 60, 0)
    objp[35] = (120, 90, 0)
    objp[15] = (135, 15 , 0)
    objp[37] = (135, 45, 0)
    objp[38] = (135, 75, 0)
    objp[39] = (135, 105, 0)
    objp[40] = (150, 0  , 0)
    objp[41] = (150, 30 , 0)
    objp[42] = (150, 60, 0)
    objp[43] = (150, 90, 0)
    ###################################################################################################

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    ###################################################################################################

    print("Empezando")
    fotos = cargar_fotos()
    for img in fotos:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        keypoints = blobDetector.detect(gray) # Detect blobs.

        # Draw detected blobs as red circles. This helps cv2.findCirclesGrid() .
        im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        im_with_keypoints_gray = cv2.cvtColor(im_with_keypoints, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findCirclesGrid(im_with_keypoints, (4,11), None, flags = cv2.CALIB_CB_ASYMMETRIC_GRID)   # Find the circle grid

        if ret == True:
            print("true")
            objpoints.append(objp)  # Certainly, every loop objp is the same, in 3D.

            corners2 = cv2.cornerSubPix(im_with_keypoints_gray, corners, (11,11), (-1,-1), criteria)    # Refines the corner locations.
            imgpoints.append(corners2)

            # Draw and display the corners.
            im_with_keypoints = cv2.drawChessboardCorners(img, (4,11), corners2, ret)
            plt.show()
            _ = input()

        print("mostrando imagen")
        cv2.imshow("img", im_with_keypoints) # display
        cv2.waitKey(2)


    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


    data = {'camera_matrix': np.asarray(mtx).tolist(), 'dist_coeff': np.asarray(dist).tolist()}
    with open("calibration.yaml", "w") as f:
        yaml.dump(data, f)