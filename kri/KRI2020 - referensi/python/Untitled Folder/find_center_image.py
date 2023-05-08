import cv2

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

def nothing(x):
  pass

def createTrackbar():
    cv2.namedWindow('to find center of image 360')
    trackbar_name = 'to find center of image 360'

    cv2.createTrackbar("Vertical", "to find center of image 360",0,500,nothing)
    cv2.createTrackbar("Horizontal", "to find center of image 360",0,500,nothing)
    cv2.createTrackbar("Radius", "to find center of image 360",1,500,nothing)
    cv2.createTrackbar("Thickness", "to find center of image 360",1,500,nothing)

def draw_center_dot(image,x,y,radius,thickness):
    image = cv2.circle(image, (x,y), radius, (0, 255, 0), thickness) 
    return image

def main():
    y = 0
    x = 0
    radius = 1
    thickness = 1
    camera360 = cv2.VideoCapture(3)

    createTrackbar()

    while(True):

        x = cv2.getTrackbarPos("Vertical", "to find center of image 360")
        y = cv2.getTrackbarPos("Horizontal", "to find center of image 360")
        radius = cv2.getTrackbarPos("Radius", "to find center of image 360")
        thickness = cv2.getTrackbarPos("Thickness", "to find center of image 360")

        print(str(x)+'\t'+str(y))

        ret, img360 = camera360.read()
        
        img360 = draw_center_dot(img360,x,y,radius,thickness)

        cv2.imshow('video', img360)
        
        if cv2.waitKey(1) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()