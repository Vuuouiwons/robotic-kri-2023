import cv2 as cv


class ImageProcessingWidget(object):
    def __init__(self, filename):
        self.original_img = cv.imread(filename, 1)

    def show_original_img(self):
        cv.imshow('original img', self.original_img)


def main():
    imgwidget = ImageProcessingWidget('img/bola.png')

    imgwidget.show_original_img()

    cv.waitKey(0)
    cv.destroyAllWindows()


main()
