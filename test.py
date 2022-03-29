from cv2 import cv2

from PhantasyIslandPythonRemoteControl import get_airplane_manager
from PhantasyIslandPythonRemoteControl.airplane_manager import AirplaneManager
from PhantasyIslandPythonRemoteControl.control_command import AirplaneController


def keyPressEvent(k: int, a: AirplaneController, m: AirplaneManager, ):
    if k == -1:  # no press
        return
    elif k == 119:  # w
        a.forward(100)
        return
    elif k == 97:  # a
        a.left(100)
        return
    elif k == 115:  # s
        a.back(100)
        return
    elif k == 100:  # d
        a.right(100)
        return
    elif k == 113:  # q
        a.rotate(90)
    elif k == 101:  # e
        a.rotate(-90)
        return
    elif k == 114:  # r
        a.up(100)
    elif k == 102:  # f
        a.down(100)
        return
    elif k == 32:  # Space
        a.takeoff(100)
        return
    elif k == 27:  # ESC
        a.land()
        return
    elif k == 13:  # Enter
        m.start()
        return

    pass


if __name__ == '__main__':
    m: AirplaneManager = get_airplane_manager()

    # print('airplanes_table', m.airplanes_table)

    m.flush()

    # print('airplanes_table', m.airplanes_table)

    a: AirplaneController = m.get_airplane('COM3')

    print(m.start())

    if a:
        cv2.namedWindow(f'{a.keyName} front', cv2.WINDOW_NORMAL)
        cv2.namedWindow(f'{a.keyName} down', cv2.WINDOW_NORMAL)

        a.use_fast_mode(True)

        while True:
            cv2.imshow(f'{a.keyName} front', a.get_camera_front_img())
            cv2.imshow(f'{a.keyName} down', a.get_camera_down_img())
            keyPressEvent(cv2.waitKey(50), a, m)
            m.flush()
        pass

    pass
