import cv2
import pyrealsense2
from realsense_depth import *
import matplotlib.pyplot as plt     
from cv2 import aruco
import numpy
import pyrealsense2

class ardetect:
    # 1. Load the ArUco dictionary
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)  # Choose your desired dictionary
    parameters = cv2.aruco.DetectorParameters_create()

    # 2. Access video capture
    video_capture = DepthCamera()  # Use 0 for webcam, or file path for a video file

    while True:
        # 3. Capture a frame
        ret, depth_frame,color_frame = video_capture.get_frame()
        # boolean to determine if arm is in right positiono with battery
        armstart=False
        # Get frame dimensions
        height, width, _ = color_frame.shape

        #set middle box height and weight
        box_size = 50
        box_x = int((width - box_size) / 2)
        box_y = int((height - box_size) / 2)

        # Draw the center box on the frame
        cv2.rectangle(color_frame, (box_x, box_y), (box_x + box_size, box_y + box_size), (0, 255, 0), 2)
        # 4. Detect ArUco markers
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(color_frame, aruco_dict, parameters=parameters)

        # 5. Draw detected markers on the frame and calculate overlap
        # check to see if ar marker is being recognized
        if ids is not None:
            for i in range(len(ids)):
                

                # Get the center of the first detected AR marker
                marker_center = corners[0][0].mean(axis=0).astype(int)

                # Update the point based on the AR marker's center
                point = tuple(marker_center)
                # get distance of the depth on ar marker
                distance = depth_frame[point[1], point[0]]

                # Calculate the overlap between the middle box and ArUco marker detection box
                middle_box = np.array([[box_x, box_y], [box_x + box_size, box_y + box_size]])
                aruco_box = np.int0(corners[i][0])  # Convert corners to integer for calculations
                intersection_area = cv2.contourArea(cv2.convexHull(np.concatenate([middle_box, aruco_box])))
                union_area = box_size**2 + cv2.contourArea(cv2.convexHull(aruco_box)) - intersection_area
                overlap_ratio = intersection_area / union_area
                print(overlap_ratio)

                # Display the confidence level between 0 and 100
                if overlap_ratio<=1 and overlap_ratio>0:
                    #if confidence level hits at least 98%
                    if overlap_ratio<=1 and overlap_ratio>=.98:
                            #turn on arm
                            armstart=True
                    print(armstart)
                    #put text for ratio next to ar marker boxes
                    cv2.putText(color_frame, f"Overlap Ratio: {overlap_ratio:.2%}",(int(corners[i][0][:, 0].mean()), int(corners[i][0][:, 1].mean()) + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),2)     
                    #put text for distance
                    cv2.putText(color_frame, f"distance: {distance} mm", (point[0], point[1] - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
            # Draw detected markers after calculating overlap
            cv2.aruco.drawDetectedMarkers(color_frame, corners, ids)

        # Draw the center box on the frame
        cv2.rectangle(color_frame, (box_x, box_y), (box_x + box_size, box_y + box_size), (0, 255, 0), 2)

        # 6. Display the frame
        cv2.imshow('ArUco Marker Detection with Confidence', color_frame)
        #cv2.imshow("depth frame", depth_frame)
        #cv2.imshow("Color frame", color_frame)

        key = cv2.waitKey(1)
        if key == 27:
            break