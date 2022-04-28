import cv2
import time

cam = cv2.VideoCapture(1)
cv2.namedWindow("test")

img_counter=0

start_time = time.time()

while True :
    ret,frame = cam.read()

    if not ret :
        print("failed to grab frame")
        break
    cv2.imshow("test",frame)

    k=cv2.waitKey(1)
    if(img_counter == 1):
        break
    elif(time.time() -start_time >3):
        cv2.imwrite('data/captured.jpg',frame)
        img_counter +=1

cam.release()
cv2.destroyAllWindows()