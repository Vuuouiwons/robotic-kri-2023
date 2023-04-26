import cv2 as cv


class ImageProcessingWidget(object):

    def __init__(self, maskfile, ballfile):
        self.mask = cv.imread(maskfile, 0)
        self.ball = cv.imread(ballfile, 0)

    def show_all_img(self):
        cv.imshow('mask img', self.mask)
        cv.imshow('ball img', self.ball)
        cv.imshow('ballmasked img', self.ballmasked)

    def masking(self):
        self.ball = cv.line(self.ball,
                            (235, 171),
                            (275, 70), 255, 10)
        self.ballmasked = cv.bitwise_and(self.mask, self.ball)


def main():
    imgwidget = ImageProcessingWidget('img/lapangan.png', 'img/bolamask.png')

    imgwidget.masking()
    imgwidget.show_all_img()

    key = cv.waitKey(0)
    if key == ord('q'):
        cv.destroyAllWindows()


main()
