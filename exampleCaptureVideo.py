# Python program to save a
# video using OpenCV


import cv2
import numpy as np

# Create an object to read
# from camera
#video = cv2.VideoCapture(0)       # LIVE CAMERA
video = cv2.VideoCapture("/Users/yhonatangayer/Library/CloudStorage/OneDrive-post.bgu.ac.il/BGU/regular2.avi")
# We need to check if camera
# is opened previously or not
if (video.isOpened() == False):
    print("Error reading video file")

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(video.get(3))
frame_height = int(video.get(4))

size = (frame_width, frame_height)

# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.
result = cv2.VideoWriter('regular.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         15, size)
resultMask = cv2.VideoWriter('masked.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         15, size)

while (True):
    ret, frame = video.read()
    upper = [15, 98, 97]
    lower = np.array([160, 40, 40], np.uint8)
    upper = np.array([179, 255, 255], np.uint8)


    HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(HSVframe, lower, upper)
    if ret == True:

        # Write the frame into the
        # file 'filename.avi'
        result.write(frame)
        #resultMask.write(np.repeat(mask,3))
        resultMask.write(np.dstack([mask]*3))

        # Display the frame
        # saved in the file
        cv2.imshow('Frame', mask)

        # Press S on keyboard
        # to stop the process
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture and video
# write objects
video.release()
result.release()

# Closes all the frames
cv2.destroyAllWindows()

print("The video was successfully saved")