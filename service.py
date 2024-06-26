import os
import sys
import tempfile
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import pytesseract
import urllib.request

def paddleocr_detect(file = None, url = None):
    if not file and not url:
        return []
    ocr = PaddleOCR(use_angle_cls=True, lang="japan")

    # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    #     temp_file_path = temp_file.name
    #     file.save(temp_file_path)

    # try:
    #     pass
    #     # Perform OCR
    #     # result = ocr.ocr(temp_file_path, cls=True)
    # finally:
    #     # Clean up the temporary file
    #     os.remove(temp_file_path)

    # # for line in result:
    # #     print(line)
    if file is not None:
        image = Image.open(file.stream)
        image = image.convert("RGB")
        image = np.array(image)
    else:
        urllib.request.urlretrieve(url, "image.png")
        script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        image = script_directory + '/image.png'


    # Perform OCR
    assert isinstance(image, (np.ndarray, list, str, bytes)), "Image format not supported"
    result = ocr.ocr(image, cls=True)
    if result[0] is None:
        return []

    boxes = [line[0] for line in result[0]]
    txts = [line[1][0] for line in result[0]]
    scores = [line[1][1] for line in result[0]]
    return txts

def tesseract_detect(file = None, url = None):
    if not file and not url:
        return []
    if file is not None:
        image = Image.open(file.stream)

    else:
        urllib.request.urlretrieve(url, "image.png")
        script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        image = script_directory + '/image.png'
        image = Image.open(image)
    
    custom_config = r'-l jpn --oem 3 --psm 6'
    txts = pytesseract.image_to_string(image, config=custom_config)
    return str(txts).split('\n')
