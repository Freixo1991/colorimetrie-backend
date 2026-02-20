from flask import Flask, request, jsonify
from PIL import Image
import numpy as np

app = Flask(__name__)

def get_dominant_color(img):
    img = img.resize((50,50))
    arr = np.array(img)
    r,g,b = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()
    return r,g,b

@app.route("/analyse", methods=["POST"])
def analyse():
    if "file" not in request.files:
        return jsonify({"error":"Pas de fichier"}), 400

    file = request.files["file"]
    try:
        img = Image.open(file.stream)
        r,g,b = get_dominant_color(img)
        brightness = (r+g+b)/3
        warmScore = r-b

        if warmScore>15 and brightness>170:
            season = "Printemps"
        elif warmScore<=15 and brightness>170:
            season = "Été"
        elif warmScore>15 and brightness<=170:
            season = "Automne"
        else:
            season = "Hiver"

        return jsonify({"season": season})
    except Exception as e:
        return jsonify({"error":str(e)}), 500

if __name__ == "__main__":
    app.run()
