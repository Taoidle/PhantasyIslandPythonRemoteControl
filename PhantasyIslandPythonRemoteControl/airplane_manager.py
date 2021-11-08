import dataclasses
from typing import Dict, Optional

from .http_layer import getAllAirplaneStatus, process_airplane
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
class Airplane(object):
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


class AirplaneManager(object):
    airplanes_table: Dict[str, Airplane] = {}

    def get_airplane(self, id: str) -> Optional[Airplane]:
        return self.airplanes_table.get(id)
        pass

    def flush(self):
        airplane_status: Dict[str, Dict[str, any]] = process_airplane(getAllAirplaneStatus())
        if airplane_status is not None:
            # print('airplane_status', airplane_status)
            for k, status in airplane_status.items():
                # print('k', k)
                if self.airplanes_table.get(k) is None:
                    self.airplanes_table[k] = Airplane(
                        keyName=status['keyName'],
                        typeName=status['typeName'],
                        updateTimestamp=status['updateTimestamp'],
                        status=status['status'],
                        cameraFront=status['cameraFront'],
                        cameraDown=status['cameraDown'],
                    )
                else:
                    a: Airplane = self.airplanes_table.get(k)
                    a.keyName = status['keyName']
                    a.typeName = status['typeName']
                    a.updateTimestamp = status['updateTimestamp']
                    a.status = make_AirplaneFlyStatus(status['status'])
                    a.cameraFront = status['cameraFront']
                    a.cameraDown = status['cameraDown']
                pass
            pass
        else:
            return None

    pass


airplane_manager_singleton = AirplaneManager()


def get_airplane_manager():
    return airplane_manager_singleton
