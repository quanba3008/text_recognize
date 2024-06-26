import flask
from flask import request, jsonify
from service import paddleocr_detect, tesseract_detect

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/paddle', methods=['POST'])
def paddle():
    if 'image' not in request.files and request.form.get('url') is None:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image'] if 'image' in request.files else None
    data = paddleocr_detect(file=file, url=request.form.get('url'))
    return {'data': data}

@app.route('/tesseract', methods=['POST'])
def tesseract():
    if 'image' not in request.files and request.form.get('url') is None:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image'] if 'image' in request.files else None
    data = tesseract_detect(file=file, url=request.form.get('url'))
    return {'data': data}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)