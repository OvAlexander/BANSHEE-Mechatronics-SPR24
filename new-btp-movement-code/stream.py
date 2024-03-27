import cv2
import numpy as np
import pickle
import socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1000000)
ip="127.0.0.1"
port=6666

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while cap.isOpened():
    ret, img = cap.read()
    cv2.imshow('img client',img)
    ret, buffer=cv2.imencode(".jpg",img,[int(cv2.IMWRITE_JPEG_QUALITY),30])
    x_as_bytes=pickle.dumps(buffer)
    s.sendto((x_as_bytes),(ip,port))
    if cv2.waitKey(5)&0xFF==27:
        break
cv2.destroyAllWindows()
cap.release()