import cv2
import numpy as np

from src.PhantasyIslandPythonRemoteControl import get_airplane_manager
from src.PhantasyIslandPythonRemoteControl.airplane_manager import AirplaneManager
from src.PhantasyIslandPythonRemoteControl.control_command import AirplaneController


def control_rotate(a: AirplaneController, count: int):
    if count <= 0:
        if a.rotate(1) is not None:
            # cv2.waitKey(10)
            return True
        else:
            return False
    else:
        return False


def control_hor(a: AirplaneController, count: int, h_img: np.array):
    if 0 < count < 600:
        h_img = hor_project(h_img)[::, h_img.shape[1] - 2::]
        h_count = cv2.countNonZero(cv2.bitwise_not(h_img))
        if 0 < h_count < 60:
            for i in range(h_img.shape[0] - 1):
                if (h_img[i - 1, 0] > 0) and (h_img[i, 0] == 0):
                    # print("hor_i", i)
                    # print('h_img[i, 0]', h_img[i, 0])
                    # print('h_img[i + 1, 0]', h_img[i + 1, 0])
                    # print('h_img.shape[0] // 2:', h_img.shape[0] // 2, '\t', 'i:', i)
                    # print("(i + h_count + i) // 2", (i + h_count + i) // 2)
                    # print("(h_img.shape[0] + 10", (h_img.shape[0] + 10) // 2)
                    # print("(h_img.shape[0] - 10", (h_img.shape[0] - 10) // 2)
                    # print()
                    if 100 <= ((i + h_count + i) // 2) <= 140:
                        return False
                    elif ((i + h_count + i) // 2) < 100:
                        # print(f"now is {i}: up")
                        if a.up(5) is not None:
                            break
                    elif ((i + h_count + i) // 2) > 140:
                        # print(f"now is {i}: down")
                        if a.down(5) is not None:
                            break
                    else:
                        break
            # cv2.waitKey(10)
        return True
    else:
        return False


def control_ver(a: AirplaneController, count: int, v_img: np.array):
    if 0 < count < 600:
        v_img = ver_project(v_img)[v_img.shape[0] - 2::, ::]
        v_count = cv2.countNonZero(cv2.bitwise_not(v_img))
        if 0 < v_count < 70:
            for i in range(v_img.shape[1] - 1):
                if (v_img[0, i - 1] > 0) and (v_img[0, i] == 0):
                    # print("ver_i", i)
                    # print('v_img[0, i]', v_img[0, i])
                    # print('v_img[0, i - 1]', v_img[0, i - 1])
                    # print('v_img.shape[1] // 2:', v_img.shape[1] // 2, '\t', 'i:', i)
                    # print()
                    if 140 <= ((i + v_count + i) // 2) <= 180:
                        return False
                    elif ((i + v_count + i) // 2) < 140:
                        # print(f"now is {i}: left")
                        if a.left(5) is not None:
                            break
                    elif ((i + v_count + i) // 2) > 180:
                        # print(f"now is {i}: right")
                        if a.right(5) is not None:
                            break
                    else:
                        break
            # cv2.waitKey(10)
            return True
    else:
        return False


def control_forward(a: AirplaneController, count: int):
    if 0 < count < 500:
        if a.forward(5) is not None:
            # cv2.waitKey(10)
            return True
    else:
        return False


def hor_project(binary):
    h, w = binary.shape
    h_projection = np.zeros(binary.shape, dtype=np.uint8)

    h_h = [0] * h
    for j in range(h):
        for i in range(w):
            if binary[j, i] == 0:
                h_h[j] += 1
    for j in range(h):
        for i in range(h_h[j]):
            h_projection[j, i] = 255

    return h_projection


def ver_project(binary):
    h, w = binary.shape
    v_projection = np.zeros(binary.shape, dtype=np.uint8)

    w_w = [0] * w
    for i in range(w):
        for j in range(h):
            if binary[j, i] == 0:
                w_w[i] += 1

    for i in range(w):
        for j in range(w_w[i]):
            v_projection[j, i] = 255

    return v_projection


if __name__ == '__main__':
    m: AirplaneManager = get_airplane_manager()
    m.flush()
    m.start()
    for port in ['COM3']:
        m.flush()
        a: AirplaneController = m.get_airplane(port)
        if a:
            a.takeoff(50)
            cv2.namedWindow(f'{a.keyName} front', cv2.WINDOW_NORMAL)
            cv2.namedWindow(f'{a.keyName} down', cv2.WINDOW_NORMAL)
            a.use_fast_mode(False)
            while True:
                f_img = a.get_camera_front_img()
                cv2.imshow(f'{a.keyName} front', f_img)
                cv2.imshow(f'{a.keyName} down', a.get_camera_down_img())
                cv2.waitKey(20)
                b, g, r = cv2.split(f_img)
                br = cv2.subtract(b, r)
                t, br_t = cv2.threshold(br, 127, 255, cv2.THRESH_BINARY)
                # cv2.imshow("br_t", br_t)
                count = cv2.countNonZero(br_t)
                hor_flag = control_rotate(a, count)
                # print("count", count)
                # print(br_t.shape)
                if not hor_flag:
                    ver_flag = control_hor(a, count, br_t)
                    forward_flag = control_ver(a, count, br_t)
                    # print("forward_flag", forward_flag)
                    if (not forward_flag) or (not forward_flag):
                        final_flag = control_forward(a, count)
                        # print(final_flag)
                m.flush()
            pass
        else:
            print(f'port {port} get error')
        pass

    pass
