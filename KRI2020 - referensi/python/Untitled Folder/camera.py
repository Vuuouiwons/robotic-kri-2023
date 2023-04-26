import cv2
import serial
import time
import numpy as np

camera360 = cv2.VideoCapture(2)
# ser = serial.Serial('/dev/ttyUSB0', 2000000)

def rotate(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated

def get_string_from_arduino():
    ser.write('o'.encode("utf-8"))
    msg = ser.read(22).decode("utf-8")
    # while '#' not in msg:
    #     time.sleep(1)
    #     msg = ser.read(22).decode("utf-8")
    #     print('wait for arduino')
    index = msg.find('#')
    msg = msg[index:] + msg[:index]
    return (msg)

def showImg(img360, degree):
    cv2.imshow('video', rotate(img360,degree, (287, 261)))


# mask center :
# -horizontal = 286
# -vertical = 260
# -radius = 15
# -thickness = 51

# mask edge :
# -horizontal = 286
# -vertical = 260
# -radius = 325
# -thickness = 251

def maskImg(img):
    image = cv2.circle(img, (286,260), 15, (0,0,0), 51) 
    image = cv2.circle(img, (286,260), 325, (0,0,0), 251) 
    return img

    
def main():
    print('wait 12s')
    # time.sleep(20)
    print('start loop')
    
    while(True):

        ret, img360 = camera360.read() 
        
        # msg = get_string_from_arduino()

        # print(msg)

        # degree = (int(msg[1:4]))

        # img360 = maskImg(img360)

        # showImg(img360,degree)

        cv2.imshow('camera', img360)

        print('test')
        
        if cv2.waitKey(1) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()