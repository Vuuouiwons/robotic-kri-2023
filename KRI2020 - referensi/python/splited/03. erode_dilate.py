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

    def erode_dilate_img(self):
        dilatation_size = 10
        element_dilate = cv.getStructuringElement(
            2, (dilatation_size, dilatation_size))
        self.orange_filtered_dilated_frame = cv.dilate(
            self.orange_filtered_frame, element_dilate)

        erodetion_size = 10
        element_erode = cv.getStructuringElement(
            2, (erodetion_size, erodetion_size))
        self.orange_filtered_eroded_frame = cv.erode(
            self.orange_filtered_frame, element_erode)

    def show_orange_filtered_dilated_img(self):
        cv.imshow('orange dilate filter', self.orange_filtered_dilated_frame)
        cv.imshow('orange erode filter', self.orange_filtered_eroded_frame)


def main():
    imgwidget = ImageProcessingWidget('img/bola.png')

    imgwidget.show_original_img()
    imgwidget.orange_filtering()
    imgwidget.show_orange_filtered_img()
    imgwidget.erode_dilate_img()
    imgwidget.show_orange_filtered_dilated_img()

    cv.waitKey(0)
    cv.destroyAllWindows()


main()
