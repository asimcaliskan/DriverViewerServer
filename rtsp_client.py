import cv2

# Set RTSP Transport Protocol to UDP
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

cap = cv2.VideoCapture("rtsp://192.168.1.30:1935", cv2.CAP_FFMPEG)

while True:
    ret, frame = cap.read()
    if not ret:
        #print("Empty frame") # absl-py logging would be better
        # time.sleep(0.1) # You may sleep and try again 
        continue
    
    cv2.imshow("RTSP Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()