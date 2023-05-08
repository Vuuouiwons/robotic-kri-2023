import cv2 as cv


class ImageProcessingWidget(object):

    def __init__(self, filename):
        self.capture = cv.VideoCapture(0)
        self.original_img = cv.imread(filename, 1)

        self.orange_HSV = {
            'lowH': 0,
            'highH': 18,
            'lowS': 149,
            'highS': 255,
            'lowV': 222,
            'highV': 255
        }

    def update(self):
        self.original_img, _ = self.capture.read()


    def show_original_img(self):
        cv.imshow('original img', self.original_img)

    def orange_filtering(self):
        print(self.orange_HSV)

        ball_hsv_lower_filter = (
            self.orange_HSV['lowH'], self.orange_HSV['lowS'], self.orange_HSV['lowV'])
        ball_hsv_upper_filter = (
            self.orange_HSV['highH'], self.orange_HSV['highS'], self.orange_HSV['highV'])

        # self.orange_filtered_frame = cv.cvtColor(
        #     self.original_img, cv.COLOR_BGR2HSV)
        # self.orange_filtered_frame = cv.inRange(
        #     self.orange_filtered_frame, ball_hsv_lower_filter, ball_hsv_upper_filter)

        self.orange_filtered_frame = cv.cvtColor(self.original_img, cv.COLOR_BGR2HSV)
        self.orange_filtered_frame = cv.inRange(self.orange_filtered_frame,(self.orange_HSV['lowH'],self.orange_HSV['lowS'],self.orange_HSV['lowV']) , (self.orange_HSV['highH'],self.orange_HSV['highS'],self.orange_HSV['highV']))


    def show_orange_filtered_img(self):
        cv.imshow('orange filter', self.orange_filtered_frame)

    def create_trackbar(self):

        cv.namedWindow('trackbar window')
        cv.createTrackbar('lowH', 'trackbar window', 0, 255, self.nothing)
        cv.createTrackbar('highH', 'trackbar window', 255, 255, self.nothing)
        cv.createTrackbar('lowS', 'trackbar window', 0, 255, self.nothing)
        cv.createTrackbar('highS', 'trackbar window', 255, 255, self.nothing)
        cv.createTrackbar('lowV', 'trackbar window', 0, 255, self.nothing)
        cv.createTrackbar('highV', 'trackbar window', 255, 255, self.nothing)

    def nothing(self, _):
        pass

    def update_trackbar(self):
        self.orange_HSV['lowH'] = cv.getTrackbarPos('lowH', 'trackbar window')
        self.orange_HSV['highH'] = cv.getTrackbarPos(
            'highH', 'trackbar window')
        self.orange_HSV['lowS'] = cv.getTrackbarPos('lowS', 'trackbar window')
        self.orange_HSV['highS'] = cv.getTrackbarPos(
            'highS', 'trackbar window')
        self.orange_HSV['lowV'] = cv.getTrackbarPos('lowV', 'trackbar window')
        self.orange_HSV['highV'] = cv.getTrackbarPos(
            'highV', 'trackbar window')


def main():
    imgwidget = ImageProcessingWidget('img/bola.png')

    imgwidget.show_original_img()

    imgwidget.create_trackbar()

    while True:
        imgwidget.update()
        imgwidget.update_trackbar()
        imgwidget.orange_filtering()
        imgwidget.show_orange_filtered_img()

        if cv.waitKey(10) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break


main()
