import cv2
from hand_pose import get_head_pose_estimation
img = cv2.imread(r"D:\GitHub\RTSP_client\image.jpg")



cap = cv2.VideoCapture(0)

#while cap.isOpened():
#    success, image = cap.read()
print(get_head_pose_estimation(img))