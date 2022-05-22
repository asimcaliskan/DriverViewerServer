# How to run:
# PS C:\Users\sunge\Masaüstü\Flask> $env:FLASK_APP  = "api"
# PS C:\Users\sunge\Masaüstü\Flask> flask run --host=0.0.0.0

from flask import jsonify, request, Flask
import sqlite3
import cv2, numpy as np, base64
import head_pose, drowsiness_detection

not_looking_forward_counter = 0
drowsiness_counter = 0

connection = sqlite3.connect(r"D:\GitHub\DriverViewerServer\database.db", check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)

@app.route("/")
def index():
    return '<h1>DriverViewer Application</h1>'

@app.route("/post", methods=["POST"])
def processjson():

    global drowsiness_counter, not_looking_forward_counter

    data = request.get_json()
    image = data["image"]
    time = data["time"]
    longitude = data["longitude"]
    latitude = data["latitude"]

    decoded_data = base64.b64decode(image)
    np_data = np.fromstring(decoded_data,np.uint8)
    img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    is_drowsiness = drowsiness_detection.is_drowsiness(img)
    is_looking_forward = head_pose.is_looking_forward(img)

    if is_drowsiness:
        drowsiness_counter += 1
    else:
        drowsiness_counter = 0


    if is_looking_forward == False:
        not_looking_forward_counter += 1
    else:
        not_looking_forward_counter = 0

    if drowsiness_counter > 3 or not_looking_forward_counter > 3:
        print(f"Latitude: {latitude} -Longitude: {longitude} -Time: {time} -Sleeping: {not is_drowsiness} -Looking Forward: {is_looking_forward}")
        cursor.execute("""INSERT INTO Posts VALUES
                ("{latitude}", "{longitude}", "{time}", "{is_eye_open}", "{is_looking_forward}")""".format(
                        latitude = latitude, longitude = longitude, time = time, is_eye_open = not is_drowsiness, is_looking_forward = is_looking_forward))
        connection.commit()
    return jsonify({"handled" : True})



@app.route("/get", methods=["GET"])
def getdata():
    res = cursor.execute("SELECT * from Posts")
    data = [dict(latitude=row[0], longitude=row[1], time=row[2], is_eye_open=row[3], is_looking_forward=row[4]) for row in res.fetchall()]
    return jsonify(data)






