import cv2


highH=0
lowH=21
highS=87
lowS=248
highV=107
lowV=255

def nothing(x):
    pass

def getHighH():
    highH=cv2.getTrackbarPos('highH','trackBar')
    return highH
def getLowH():
    lowH=cv2.getTrackbarPos('lowH','trackBar')
    return lowH
def getHighS():
    highS=cv2.getTrackbarPos('highS','trackBar')
    return highS
def getLowS():
    lowS=cv2.getTrackbarPos('lowS','trackBar')
    return lowS
def getHighV():
    highV=cv2.getTrackbarPos('highV','trackBar')
    return highV
def getLowV():
    lowV=cv2.getTrackbarPos('lowV','trackBar')
    return lowV

def convert(img, highH,highS,highV, lowH,lowS,lowV):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print((highH,highS,highV), (lowH,lowS,lowV))
    hsv = cv2.inRange(hsv, (highH,highS,highV), (lowH,lowS,lowV))
    return hsv

def trackBar():
    cv2.namedWindow('trackBar')
    #cv.createTrackbar(trackbar_name, title_window , 0, alpha_slider_max, on_trackbar)
    cv2.createTrackbar('highH', 'trackBar', highH, 255, nothing)
    cv2.createTrackbar('lowH', 'trackBar', lowH, 255, nothing)
    cv2.createTrackbar('highS', 'trackBar', highS, 255, nothing)
    cv2.createTrackbar('lowS', 'trackBar', lowS, 255, nothing)
    cv2.createTrackbar('highV', 'trackBar', highV, 255, nothing)
    cv2.createTrackbar('lowV', 'trackBar', lowV, 255, nothing)
    
def resizing(img):
    scale_percent = 20 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized
    
def dieroding(hsv):
    erosion_size = 7
    dilatation_size = 7
    element = cv2.getStructuringElement(2, (2*erosion_size + 1, 2*erosion_size+1), (erosion_size, erosion_size))
    hsv = cv2.erode(hsv, element)
    element = cv2.getStructuringElement(2, (2*dilatation_size + 1, 2*dilatation_size+1), (dilatation_size, dilatation_size))
    hsv = cv2.dilate(hsv, element)
    element = cv2.getStructuringElement(2, (2*dilatation_size + 1, 2*dilatation_size+1), (dilatation_size, dilatation_size))
    hsv = cv2.dilate(hsv, element)
    element = cv2.getStructuringElement(2, (2*erosion_size + 1, 2*erosion_size+1), (erosion_size, erosion_size))
    hsv = cv2.erode(hsv, element)
    return hsv

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    trackBar()

    while True:
        _, img = cap.read()
        highH = getHighH()
        lowH = getLowH()
        highS = getHighS()
        lowS = getLowS()
        highV = getHighV()
        lowV = getLowV()
        
        hsv = convert(img,highH,highS,highV, lowH,lowS,lowV)
        #hsv = dieroding(hsv)
        
        cv2.imshow('bola',img)
        cv2.imshow('bolaHSV',hsv)

        key = cv2.waitKey(1)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()