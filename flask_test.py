from flask import Flask, request, jsonify
import base64
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello Mann</p>"

@app.route('/post_image/<image_data>', methods=['POST', 'GET'])                                                                                                          
def post_image(image_data):
    if request.method == 'POST':
        return "zaaa"
    else:
        return 'GET request successfully'



@app.route('/authenticate/',methods = ['POST'])
def authenticate():
    content = request.json

    encodedImg = content['image'] # 'file' is the name of the parameter you used to send the image
    imgdata = base64.b64decode(str.encode(encodedImg))
    filename = 'image.jpg'  # choose a filename. You can send it via the request in an other variable
    with open(filename, 'wb') as f:
        f.write(imgdata)
    return jsonify({"uuid":"asd"})