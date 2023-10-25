# Python program to save a
# video using OpenCV


import cv2
import numpy as np
import math

def draw_label(img, text, pos, bg_color):
   font_face = cv2.FONT_HERSHEY_SIMPLEX
   scale = 2
   color = (0, 0, 0)
   thickness = cv2.FILLED
   margin = 2
   txt_size = cv2.getTextSize(text, font_face, scale, thickness)

   end_x = pos[0] + txt_size[0][0] + margin
   end_y = pos[1] - txt_size[0][1] - margin

   cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
   cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)
def overlayTrail(x1,y1,x2,y2,frame,frameT,frame_width,frame_height,frameT_width,frameT_height,trailLength=900,scaleFactor=1):
    # trail size is the actually trial length in pixels, not its image width or height
    #scaleFactor make the trail bigger or smaller. its size also depend on the distance between the points
    distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    midPosX = int((x1+x2)/2)
    midPosY = int((y1+y2)/2)
    angle = (math.atan2(y1-y2, x1-x2)*180)/math.pi

    resizeFactor = (distance / trailLength)*scaleFactor
    newWidth = int(frameT_width*resizeFactor)
    newHeight = int(frameT_height*resizeFactor)
    resized = cv2.resize(frameT, (newWidth, newHeight), interpolation=cv2.INTER_AREA)
    resized_rotated = rotate_image(resized,angle*(-1)+180)
    if (midPosX> newWidth/2 and midPosY>newHeight/2 and midPosX<frame_width-newWidth/2 and midPosY<frame_height-newHeight/2):
        left = midPosX - int(newWidth / 2)
        right = midPosX + int(newWidth / 2)
        up = midPosY + int(newHeight / 2)
        down = midPosY - int(newHeight / 2)
        frame[down:up, left:right, :] = resized_rotated[:up-down,:right-left,:] + frame[down:up, left:right, :]

    return frame

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

# Create an object to read
# from camera
# video = cv2.VideoCapture(0)
video = cv2.VideoCapture("regular.avi")
videoTrail = cv2.VideoCapture("fireball.gif")
# We need to check if camera
# is opened previously or not
if (video.isOpened() == False):
    print("Error reading video file")

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(video.get(3))
frame_height = int(video.get(4))

frameT_width = int(videoTrail.get(3))
frameT_height = int(videoTrail.get(4))

size = (frame_width, frame_height)

# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.

# result = cv2.VideoWriter('regular3.avi',
#                         cv2.VideoWriter_fourcc(*'MJPG'),
#                         30.0, size)
# resultMask = cv2.VideoWriter('masked.avi',
#                          cv2.VideoWriter_fourcc(*'MJPG'),
#                          30, size)

# video.set(cv2.CAP_PROP_FPS,30)
t=0
x1=0
y1=0


while (True):
    ret, frame = video.read()
    retT, frameT = videoTrail.read()

    #does loop
    if not retT:
        print('no video')
        videoTrail.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    upper = [15, 98, 97]
    lower = np.array([160, 40, 40], np.uint8)
    upper = np.array([179, 255, 255], np.uint8)
    # print(video.get(cv2.CAP_PROP_FPS))
    HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(HSVframe, lower, upper)
    if ret == True:

        # Write the frame into the
        # file 'filename.avi'
        # result.write(frame)
        #resultMask.write(np.repeat(mask,3))
        #resultMask.write(np.dstack([mask]®*3))


        # newWidth = int(frameT_width/2)
        # newHeight = int(frameT_height/2)
        # resized = cv2.resize(frameT,(newWidth,newHeight),interpolation=cv2.INTER_AREA)
        # resized_rotated = rotate_image(resized,90)
        # frame[:newHeight,:newWidth,:] = resized_rotated + frame[:newHeight,:newWidth,:]

        t = t+0.2
        a=1
        v= 20
        v0 = 30
        x2=x1
        y2=y1
        x1 = 300+v*t
        y1 = 300+30*t - 0.5*a*t**2


        frame = overlayTrail(x1,y1,x2,y2,frame,frameT,frame_width,frame_height,frameT_width,frameT_height,900,30)
        draw_label(frame, 'Hello World', (20, 20), (255, 0, 0))
        cv2.imshow('Frame', frame)






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
# result.release()

# Closes all the frames
cv2.destroyAllWindows()

print("The video was successfully saved")

