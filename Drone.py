import cv2
import sys
from djitellopy import Tello
SET_POINT_X = 960/2
SET_POINT_Y = 720/2
Path = "path"  # Path of the model used to reveal faces
faceCascade = cv2.CascadeClassifier(Path)
drone = Tello()  # declaring drone object
drone.connect()
drone.takeoff()


drone.streamon()  # start camera streaming


while True:

    frame = drone.get_frame_read().frame  # capturing frame from drone
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # turning image into gray scale

    faces = faceCascade.detectMultiScale(  # face detection
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    i = 0
    for (x, y, w, h) in faces:

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 5)  # contour rectangle
        cv2.circle(frame, (int(x+w/2), int(y+h/2)), 12, (255, 0, 0), 1)  # face-centered circle
        
        

        cv2.circle(frame, (int(SET_POINT_X), int(SET_POINT_Y)), 12, (255, 255, 0), 8)  # setpoint circle
        i = i+1
        distanceX = x+w/2 - SET_POINT_X
        distanceY = y+h/2 - SET_POINT_Y

        up_down_velocity = 0
        right_left_velocity = 0

        if distanceX < -5:
            
            right_left_velocity = - 20

        elif distanceX > 5:
            
            right_left_velocity = 20
        else:
            print("OK")

        if distanceY < -5:
            
            up_down_velocity = 20
        elif distanceY > 5:
            
            up_down_velocity = - 20

        else:
            

        if abs(distanceX) < 20:
            right_left_velocity = int(right_left_velocity / 2)
        if abs(distanceY) < 20:
            up_down_velocity = int(up_down_velocity / 2)

        drone.send_rc_control(right_left_velocity, 0, up_down_velocity, 0)

    cv2.imshow('Video', frame)  

    if cv2.waitKey(1) & 0xFF == ord('q'):  # quit from script
        break

# rilascio risorse
# video_capture.release()
cv2.destroyAllWindows()