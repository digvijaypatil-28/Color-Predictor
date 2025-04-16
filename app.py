from flask import Flask, render_template, request, jsonify
import pandas as pd
import cv2
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the color dataset
csv_path = 'colors.csv'  # Make sure this exists
index = ["color_name", "hex", "R", "G", "B"]
df = pd.read_csv(csv_path, names=index, header=0)

def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = df.loc[i, "color_name"]
    return cname

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'image' in request.files:
            image = request.files['image']
            path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(path)
            return render_template("index.html", uploaded_image=image.filename)

        else:
            x = int(request.form["x"])
            y = int(request.form["y"])
            filename = request.form["filename"]
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img = cv2.imread(image_path)
            if img is not None and 0 <= y < img.shape[0] and 0 <= x < img.shape[1]:
                B, G, R = img[y, x]
                color_name = get_color_name(R, G, B)
                return jsonify({"color": color_name, "R": int(R), "G": int(G), "B": int(B)})
            else:
                return jsonify({"color": "Invalid click", "R": 0, "G": 0, "B": 0})

    return render_template("index.html", uploaded_image=None)

if __name__ == "__main__":
    app.run(debug=True)
