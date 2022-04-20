from typing import Dict
import sys

import requests
import json

from .config import remote_location


def ping():
    return send_cmd('ping')


def ping_volatile():
    return send_cmd_volatile('ping')


def start():
    return send_cmd_volatile('start')


def send_cmd(s: str):
    try:
        r = requests.get('http://' + remote_location + '/ECU_HTTP/sendStringCmd?c=' + s, timeout=10)
        print(r.status_code)
        print(r.text)
        j = json.loads(r.text)
        print(j)
        return (j['ok'], j['r'])
    except requests.exceptions.ReadTimeout as e:
        print('send_cmd ', s, ' ', 'Error Command Timeout')
        return (False, 'Timeout')
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError Cannot Connect to PhantasyIsland, Max retries exceeded.', file=sys.stderr)
        try:
            print('  ===>>>  ' + str(e.args[0].reason), file=sys.stderr)
        except:
            pass
        return (False, 'ConnectionError Cannot Connect to PhantasyIsland')


def send_cmd_volatile(s: str):
    try:
        r = requests.get('http://' + remote_location + '/ECU_HTTP/sendStringCmd?cc=' + s, timeout=10)
        print(r.status_code)
        print(r.text)
        j = json.loads(r.text)
        return (j['ok'], j['r'])
    except requests.exceptions.ReadTimeout as e:
        print('send_cmd_volatile ', s, ' ', 'Error Command Timeout')
        return (False, 'Timeout')
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError Cannot Connect to PhantasyIsland, Max retries exceeded.', file=sys.stderr)
        try:
            print('  ===>>>  ' + str(e.args[0].reason), file=sys.stderr)
        except:
            pass
        return (False, 'ConnectionError Cannot Connect to PhantasyIsland')


def get_all_airplane_status():
    error = None
    try:
        r = requests.get('http://' + remote_location + '/ECU_HTTP/getAllAirplaneStatus', timeout=5)
        # print(r.status_code)
        j = json.loads(r.text)
        return j
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError Cannot Connect to PhantasyIsland, Max retries exceeded.', file=sys.stderr)
        try:
            print('  ===>>>  ' + str(e.args[0].reason), file=sys.stderr)
        except:
            print(e, file=sys.stderr)
        error = e
        pass
    if error is not None:
        raise Exception('ConnectionError Cannot Connect to PhantasyIsland, Max retries exceeded.')


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
