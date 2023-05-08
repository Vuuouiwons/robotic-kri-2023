import cv2 as cv


class ImageProcessingWidget(object):

    def __init__(self, filename):
        self.original_img = cv.imread(filename, 0)

    def show_original_img(self):
        cv.imshow('original img', self.original_img)

    def get_blob_center(self, img):
        M = cv.moments(self.original_img)

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        return cX, cY

    def show_dotted_img(self):
        center_coordinate = self.get_blob_center(self.original_img)
        dot_color = (0, 255, 0)
        self.dotted_img = self.original_img
        self.dotted_img = cv.circle(
            self.original_img, center_coordinate, 2, dot_color, 2)
        cv.imshow('dotted img', self.dotted_img)


def main():
    imgwidget = ImageProcessingWidget('img/bolamask.png')

    imgwidget.show_original_img()
    imgwidget.show_dotted_img()

    key = cv.waitKey(0)
    if key == ord('q'):
        cv.destroyAllWindows()
        exit()


main()
