from cv2 import cv2

from PhantasyIslandPythonRemoteControl import AirplaneManager

if __name__ == '__main__':
    m = AirplaneManager()

    # print('airplanes_table', m.airplanes_table)

    m.flush()

    # print('airplanes_table', m.airplanes_table)

    a = m.get_airplane('COM3')

    if a:
        cv2.namedWindow(f'{a.keyName} front', cv2.WINDOW_NORMAL)
        cv2.namedWindow(f'{a.keyName} down', cv2.WINDOW_NORMAL)

        while True:
            cv2.imshow(f'{a.keyName} front', a.get_camera_front_img())
            cv2.imshow(f'{a.keyName} down', a.get_camera_down_img())
            cv2.waitKey(50)
            m.flush()
        pass

    pass
