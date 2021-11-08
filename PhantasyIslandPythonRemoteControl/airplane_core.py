import dataclasses
from typing import Dict

from .image_process import read_b64_img

@dataclasses.dataclass()
class AirplaneFlyStatus(object):
    landing: bool
    isStop: bool
    x: float
    y: float
    h: float
    rX: float
    rY: float
    rZ: float
    pass


def make_AirplaneFlyStatus(
        fly_status: Dict[str, any]
):
    return AirplaneFlyStatus(
        landing=fly_status['landing'],
        isStop=fly_status['isStop'],
        x=fly_status['x'],
        y=fly_status['y'],
        h=fly_status['h'],
        rX=fly_status['rX'],
        rY=fly_status['rY'],
        rZ=fly_status['rZ'],
    )
    pass


@dataclasses.dataclass()
class AirplaneCore(object):
    keyName: str
    typeName: str
    updateTimestamp: int
    status: AirplaneFlyStatus
    cameraFront: str
    cameraDown: str

    def get_camera_front_img(self):
        return read_b64_img(self.cameraFront)
        pass

    def get_camera_down_img(self):
        return read_b64_img(self.cameraDown)
        pass

    pass
