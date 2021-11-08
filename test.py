from cv2 import cv2

from PhantasyIslandPythonRemoteControl.airplane_manager import AirplaneManager

if __name__ == '__main__':
    m = AirplaneManager()

    print('airplanes_table', m.airplanes_table)

    m.flush()

    print('airplanes_table', m.airplanes_table)

    a = m.get_airplane('COM3')

    if a:
        while True:
            cv2.imshow('get_camera_front_img', a.get_camera_front_img())
            cv2.imshow('get_camera_down_img', a.get_camera_down_img())
            cv2.waitKey(50)
            m.flush()
        pass

    pass
