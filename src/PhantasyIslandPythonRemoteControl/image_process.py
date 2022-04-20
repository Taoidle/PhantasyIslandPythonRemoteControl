import base64
from cv2 import cv2
import numpy as np


# https://jdhao.github.io/2020/03/17/base64_opencv_pil_image_conversion/
def read_b64_img(uri: str):
    if uri is None:
        return None
    im_b64 = uri.split(',')[1]
    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img
