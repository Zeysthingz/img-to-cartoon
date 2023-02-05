import cv2
import numpy as np
import matplotlib.pyplot as plt



class ImagesToCartoon:
    def __init__(self, image_file):
        self.image_file = image_file

    def convert_image(self):
        img = cv2.imread(self.image_file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        # if pixes valuee is greater than adaptive threshold value then it is assigned to 255 helps finding edges
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

        #  bilateral filter is used for smoothening images and reducing noise, while preserving edges
        colored_img = cv2.bilateralFilter(img, 9, 250, 250)

        cartoon = cv2.bitwise_and(colored_img, colored_img, mask=edges)
        return cartoon


if __name__ == "__main__":
    image = ImagesToCartoon("img/michael.jpg")
    img =image.convert_image()
    cv2.imwrite("img/cartoon-michael.jpg", img)
#     save the image

