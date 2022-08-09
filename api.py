# way to upload image: endpoint
# way to save the image
# function to make prediction on the image
# Show the result

import os

from flask import Flask
from flask import request
from flask import render_template

import pickle

from skimage.transform import resize
from skimage.io import imread

app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/dhuma/Desktop\deployment/static'

model = pickle.load(open("C:/Users/dhuma/Desktop/deployment/model_pickle", 'rb'))
Categories = ['benign', 'malignant']


def prediction(x):
    img = imread(x)
    img_resize = resize(img, (150, 150, 3))
    l = [img_resize.flatten()]
    data = Categories[model.predict(l)[0]]
    return data


@app.route("/", methods=["GET", "POST"])
def upload_predict():
    if request.method == "POST":
        image_file = request.files["image"]
        if image_file:
            image_loacation = os.path.join(
                UPLOAD_FOLDER,
                image_file.filename
            )
            image_file.save(image_loacation)
            pred = prediction(image_loacation)
            return render_template("index.html", prediction=pred, image_loc=image_file.filename)
    return render_template("index.html", prediction=0, image_loc=None)


if __name__ == "__main__":
    app.run(port=1200, debug=True)