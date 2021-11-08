from typing import Dict

import requests
import json
import cv2

from .config import remote_location
from .image_process import read_b64_img


def ping():
    r = requests.get('http://' + remote_location + '/ECU_HTTP/sendStringCmd?c=ping')
    print(r.status_code)
    print(r.text)
    return r.text


def getAllAirplaneStatus():
    r = requests.get('http://' + remote_location + '/ECU_HTTP/getAllAirplaneStatus')
    # print(r.status_code)
    j = json.loads(r.text)
    return j


def process_airplane(j: Dict[str, any]):
    if j['ok'] is True:
        airplanes = j['airplanes']
        # print(airplanes)
        airplaneStatus: Dict[str, Dict[str, any]] = {}
        for air in airplanes:
            # print(air)
            status: Dict[str, any] = {}
            # print(air['keyName'])
            # print(air['typeName'])
            # print(air['updateTimestamp'])
            # print(air['status'])
            status['keyName'] = air['keyName']
            status['typeName'] = air['typeName']
            status['updateTimestamp'] = air['updateTimestamp']
            status['status'] = air['status']
            # print(air['cameraDown'])
            # print(air['cameraFront'])
            camera_front = air['cameraFront']
            camera_front_img_data_string = camera_front['imgDataString']
            status['cameraFront'] = camera_front_img_data_string
            camera_down = air['cameraDown']
            camera_down_img_data_string = camera_down['imgDataString']
            status['cameraDown'] = camera_down_img_data_string
            # # print(cameraFront['imgDataString'])
            # img = read_b64_img(cameraFront['imgDataString'])
            # # print(img)
            # if img is not None:
            #     cv2.imshow(air['keyName'], img)
            #     cv2.waitKey(1)
            # else:
            #     print(img)
            # pass
            airplaneStatus[status['keyName']] = status
            pass
        return airplaneStatus
    else:
        return None
    pass
