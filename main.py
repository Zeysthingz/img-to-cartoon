import cv2
from flask import Flask, request, render_template,Response
import os


app = Flask(__name__,template_folder="html")
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the uploaded image
        image = request.files["image"]
        img = ImagesToCartoon("img/" + image.filename)
        cartoon_image =img.convert_image()
        # save image as output.jpg
        cv2.imwrite("static/output.jpg", cartoon_image)
        full_filename = os.path.join('static', "output.jpg")

        return render_template("result.html", user_image=full_filename)
    return render_template("index.html")
def send_file_custom(file, attachment_filename=None):
    response = Response()
    response.data = open(file, "rb").read()
    response.headers["Content-Type"] = "application/octet-stream"
    if attachment_filename:
        response.headers["Content-Disposition"] = "attachment; filename={}".format(attachment_filename)
    return response
# define endpoint for downloading the image
@app.route("/download")
def download():
    return send_file_custom("static/output.jpg", attachment_filename="output.jpg")

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
    app.run(debug=True)

