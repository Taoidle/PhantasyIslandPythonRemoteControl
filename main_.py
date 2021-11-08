from typing import Dict

import requests
import json
import base64
import cv2
import numpy as np


# https://jdhao.github.io/2020/03/17/base64_opencv_pil_image_conversion/
def read_b64_img(uri):
    im_b64 = uri.split(',')[1]
    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img


def process_airplane_image(j: Dict[str, any]):
    if j['ok'] is True:
        airplanes = j['airplanes']
        # print(airplanes)
        for air in airplanes:
            # print(air)
            print(air['keyName'])
            print(air['typeName'])
            print(air['updateTimestamp'])
            print(air['status'])
            # print(air['cameraDown'])
            # print(air['cameraFront'])
            cameraFront = air['cameraFront']
            # print(cameraFront['imgDataString'])
            img = read_b64_img(cameraFront['imgDataString'])
            # print(img)
            if img is not None:
                cv2.imshow(air['keyName'], img)
                cv2.waitKey(1)
            else:
                print(img)
            pass
    pass


if __name__ == '__main__':
    print('PyCharm')
    r = requests.get('http://127.0.0.1:12566/ECU_HTTP/sendStringCmd?c=ping')
    print(r.status_code)
    print(r.text)
    print(json.loads(r.text))

    while True:
        r = requests.get('http://127.0.0.1:12566/ECU_HTTP/getAllAirplaneStatus')
        print(r.status_code)
        # print(r.text)
        j = json.loads(r.text)
        # print(j)
        # print(j['ok'])
        process_airplane_image(j)
        pass
