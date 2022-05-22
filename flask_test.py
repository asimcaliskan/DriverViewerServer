from turtle import pos
from flask import Flask, request, jsonify, g
import base64
from PIL import Image
import io
import numpy as np
import cv2
from hand_pose import get_head_pose_estimation
from drowsiness_detection import get_drowsiness_estimation

app = Flask(__name__)



@app.route('/')
def index():
    return "<h1>HELLO MAN</h1>"

@app.route('/authenticate/', methods=['POST'])
def authenticate():
    content = request.json
    # 'file' is the name of the parameter you used to send the image
    encodedImg = content['image']
    altitude = content['latitude']
    longitude = content['longitude']
    time = content['time']
    #print(f"altitude: {altitude}, longitude:{longitude}, time:{time}")
    decoded_data = base64.b64decode(encodedImg)
    np_data = np.fromstring(decoded_data,np.uint8)
    img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    print("Drawsiness: ", get_drowsiness_estimation(img))
    print("Look Forward: ", get_head_pose_estimation(img))
    return jsonify({"handled": True})
