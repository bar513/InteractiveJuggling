# main.py
# import the necessary packages
from flask import Flask, render_template, Response
from cameraClass import VideoCamera

app = Flask(__name__)
@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')
def gen(camera):
    for i in range(5):
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
               # b'Content-Length: ' + len(frame).to_bytes()
                 )
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
# def video_feed():
#     return Response(VideoCamera().get_frame(), mimetype='image/png')

if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port='8080', debug=True)