import cv2 as cv


class ImageProcessingWidget(object):

    def __init__(self, filename):
        self.original_img = cv.imread(filename, 1)

        self.orange_HSV = {
            'lowH': 0,
            'highH': 18,
            'lowS': 149,
            'highS': 255,
            'lowV': 222,
            'highV': 255
        }

    def show_original_img(self):
        cv.imshow('original img', self.original_img)

    def orange_filtering(self):

        ball_hsv_lower_filter = (
            self.orange_HSV['lowH'], self.orange_HSV['lowS'], self.orange_HSV['lowV'])
        ball_hsv_upper_filter = (
            self.orange_HSV['highH'], self.orange_HSV['highS'], self.orange_HSV['highV'])

        self.orange_filtered_frame = cv.cvtColor(
            self.original_img, cv.COLOR_BGR2HSV)
        self.orange_filtered_frame = cv.inRange(
            self.orange_filtered_frame, ball_hsv_lower_filter, ball_hsv_upper_filter)

    def show_orange_filtered_img(self):
        cv.imshow('orange filter', self.orange_filtered_frame)


def main():
    imgwidget = ImageProcessingWidget('img/bola.png')

    imgwidget.show_original_img()
    imgwidget.orange_filtering()
    imgwidget.show_orange_filtered_img()

    cv.waitKey(0)
    cv.destroyAllWindows()


main()
