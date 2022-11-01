import cv2
from typing import NamedTuple
import collections

from multiprocessing import Process, Queue

from src.PhantasyIslandPythonRemoteControl import get_airplane_manager
from src.PhantasyIslandPythonRemoteControl.airplane_manager import AirplaneManager
from src.PhantasyIslandPythonRemoteControl.control_command import AirplaneController


def process_recive_keyPressEvent(Q):
    """
    The process_recive_keyPressEvent function is a function that runs in a separate process.
    It receives key presses from the main thread and sends them to the AirplaneController object.


    :param Q: Send the key press event to the airplanecontroller
    :return: A tuple containing a boolean value and two airplanecontroller objects
    :doc-author: Jeremie
    """
    while True:
        # (k: int, a: AirplaneController, m: AirplaneManager, )
        (exit, k, a, m) = Q.get()
        if exit is True:
            break
        keyPressEvent(k, a, m)
    pass


def process_call_keyPressEvent(Q: Queue, k: int, a: AirplaneController, m: AirplaneManager, ):
    """
    The process_call_keyPressEvent function is a function that takes in an integer key and a queue.
    It run in main thread, then puts the key into the queue to be processed by another thread.

    :param Q:Queue: Pass the queue to the process_call_keypressevent function
    :param k:int: Get the key that was pressed
    :param a:AirplaneController: Access the airplane controller
    :param m:AirplaneManager: Access the airplanemanager object
    :param : Pass the key pressed by the user to the airplanecontroller
    :return: A tuple with the following values:
    :doc-author: Jeremie
    """
    Q.put((False, k, a, m))


def process_exit_keyPressEvent(Q: Queue):
    """
    The process_exit_keyPressEvent function is a helper function that puts a tuple of three values into the queue.
    The first value in the tuple indicates that the user has pressed 'q' to quit, and this process should be terminated.
    The second value in the tuple is None, because we do not need any information from this event. The third and fourth
    values are also None because they are not needed for this event.

    :param Q:Queue: Pass the queue to the function
    :return: A tuple containing a boolean, an integer, a string and an object
    :doc-author: Jeremie
    """
    Q.put((True, None, None, None))


def process_Show(port: str, m: AirplaneManager, ):
    """
    The process_Show function is used to show the front and down camera of the airplane.
    It will also record the key press event from user.
    It's running in main thread.


    :param port:str: Specify the port of the AirplaneController object
    :param m:AirplaneManager: the AirplaneManager object
    :param : Get the key pressed by user
    :return: None
    :doc-author: Jeremie
    """

    m.flush()
    a: AirplaneController = m.get_airplane(port)
    a.status
    if a:
        Q = Queue()
        cv2.namedWindow(f'{a.keyName} front', cv2.WINDOW_NORMAL)
        cv2.namedWindow(f'{a.keyName} down', cv2.WINDOW_NORMAL)
        a.use_fast_mode(False)
        p = Process(target=process_recive_keyPressEvent, args=(Q,))
        p.start()
        while True:
            cv2.imshow(f'{a.keyName} front', a.get_camera_front_img())
            cv2.imshow(f'{a.keyName} down', a.get_camera_down_img())
            process_call_keyPressEvent(Q, cv2.waitKey(50), a, m)
            m.flush()
        pass
    else:
        print(f'port {port} get error')
    pass


def keyPressEvent(k: int, a: AirplaneController, m: AirplaneManager, ):
    """
    The keyPressEvent function is called whenever a key is pressed.
    It takes two arguments: k, the key that was pressed, and a, the AirplaneController object.
    The function then calls one of several functions in AirplaneController depending on which key was pressed.
    It's running in main thread.

    :param k:int: Get the key pressed by the user
    :param a:AirplaneController:
    :param m:AirplaneManager:
    :param : Control the speed of the airplane
    :return: The key that was pressed
    :doc-author: Trelent
    """

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

    print(m.start())

    m.flush()
    # a: AirplaneController = m.get_airplane('COM3')
    # print('ping', m.ping())
    # print('ping', type(m.ping()))
    # print('ping_volatile', m.ping_volatile())
    # print('ping_volatile', type(m.ping_volatile()))
    # print('start', m.start())
    # print('start', type(m.start()))
    # print('start', len(m.start()))
    # print('start', m.start()[0])
    # print('start', type(m.start()[1]))
    # print('start....', (False, ''))
    # print('start....', type((False, '')))
    #
    #
    # class Te(NamedTuple):
    #     ok: bool
    #     r: str | None
    #     m: str | None
    #
    #
    # print('Te', Te(False, '', None))
    # print('Te', type(Te(False, '', None)))
    #
    # TTe = collections.namedtuple('TTe', ['ok', 'r', 'm'])
    # print('TTe', TTe(False, '', None))
    # print('TTe', type(TTe(False, '', None)))
    #
    # print('ccc', type({
    #     'ok': False,
    #     'r': '',
    #     'm': None,
    # }))
    # print('ccc', {
    #     'ok': False,
    #     'r': '',
    #     'm': None,
    # })

    # m.ping()
    # m.ping_volatile()
    # m.start()

    for port in ['COM3']:
        p = Process(target=process_Show, args=(port, m,))
        p.start()

    # p = Process(target=process_Show, args=('COM3', m,))
    # p.start()
    # p.join()



