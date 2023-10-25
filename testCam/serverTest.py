# first of all import the socket library
import socket
import numpy as np
import cv2 as cv
def video_to_array(path):
    cap = cv.VideoCapture(path)
    frameCount = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    buf = np.empty((frameCount, 400, 640, 3), np.dtype('uint8'))

    fc = 0
    ret = True

    while (fc < frameCount  and ret):
        ret, frame = cap.read()
        buf[fc] = cv.resize(frame, (640, 400))
        fc += 1

    cap.release()
    return buf


images = video_to_array('../regular2.mp4')

frameMp4 = images[60]
# next create a socket object
s = socket.socket()
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print("socket binded to %s" % (port))


# put the socket into listening mode
s.listen(5)

print("socket is listening")

# a forever loop until we interrupt it or
# an error occurs

video = cv.VideoCapture(0)
c, addr = s.accept()

while True:
    ret, frame = video.read()
    resizedFrame = cv.resize(frame, (640, 400))
    # Establish connection with client.
    print('Got connection from', addr)

    # send a thank you message to the client. encoding to send byte type.
    # c.send('Thank you for connecting'.encode())
    ret, jpeg = cv.imencode('.png', resizedFrame)
    img = jpeg.tobytes()

    ret2, jpeg2 = cv.imencode('.png', frameMp4)
    frameMp42 = jpeg2.tobytes()

    # print(len(img))
    # x = len(img).to_bytes(4,"little")
    sizeBytes = int(len(img)).to_bytes(4, "little")

    c.send(sizeBytes + img)
    # Close the connection with the client
    # c.close()

    # Breaking once connection closed
    # break