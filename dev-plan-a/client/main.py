import cv2 as cv
from sensors.camera import Camera
from object_segments import find
# init camera
camObj = Camera(0, 1280, 720, dict())

# hsv color
green = [[68, 91, 121], [111, 195, 212]]

while True:
    frame = camObj.get_processed_frame(green)
    ctr = camObj.get_center_object(frame)
    print(camObj.get_object_location(ctr[1]))

    cv.imshow("frame", frame)

    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()
