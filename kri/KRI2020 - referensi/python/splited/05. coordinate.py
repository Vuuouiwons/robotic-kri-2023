import cv2 as cv


class ImageProcessingWidget(object):

    def __init__(self, filename, src=0):
        self.capture = cv.VideoCapture(src)
        self.capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
        _, self.original_img = self.capture.read()
        # self.original_img = cv.imread(filename, 1)
    
    def set_img(self):
        _, self.original_img = self.capture.read()
        

    def show_original_img(self):
        cv.imshow('original img', self.original_img)

    def create_trackbar(self, maxX, maxY):

        cv.namedWindow('trackbar window')
        cv.createTrackbar('coordinate X', 'trackbar window',
                          0, maxX, self.nothing)
        cv.createTrackbar('coordinate Y', 'trackbar window',
                          0, maxY, self.nothing)

    def nothing(self, _):
        pass

    def update_trackbar(self):
        self.coordinate_x = cv.getTrackbarPos(
            'coordinate X', 'trackbar window')
        self.coordinate_y = cv.getTrackbarPos(
            'coordinate Y', 'trackbar window')

    def show_dotted_img(self):
        center_coordinate = (self.coordinate_x, self.coordinate_y)
        dot_color = (0, 255, 0)
        self.dotted_img = self.original_img
        self.dotted_img = cv.circle(
            self.original_img, center_coordinate, 2, dot_color, 2)
        cv.imshow('dotted img', self.dotted_img)


def main():
    imgwidget = ImageProcessingWidget('img/bolamask.png')

    x, y, _ = imgwidget.original_img.shape


    imgwidget.create_trackbar(y, x)

    while True:
        imgwidget.set_img()
        imgwidget.update_trackbar()
        imgwidget.show_original_img()

        imgwidget.show_dotted_img()

        if cv.waitKey(10) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break


main()
