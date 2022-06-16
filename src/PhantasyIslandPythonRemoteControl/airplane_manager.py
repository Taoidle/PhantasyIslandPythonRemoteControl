from typing import Dict, Optional
from time import sleep

from .airplane_core import make_AirplaneFlyStatus
from .control_command import AirplaneController
from .http_layer import get_all_airplane_status, process_airplane, ping, ping_volatile, start, start_volatile


class AirplaneManager(object):
    airplanes_table: Dict[str, AirplaneController] = {}

    def ping(self):
        return ping()

    def ping_volatile(self):
        return ping_volatile()

    def start(self):
        return start()

    def start_volatile(self):
        return start_volatile()

    def get_airplane(self, id: str) -> Optional[AirplaneController]:
        return self.airplanes_table.get(id)
        pass

    def sleep(self, time):
        sleep(time)
        pass

    def flush(self):
        airplane_status: Dict[str, Dict[str, any]] = process_airplane(get_all_airplane_status())
        if airplane_status is not None:
            # print('airplane_status', airplane_status)
            for k, status in airplane_status.items():
                # print('k', k)
                if self.airplanes_table.get(k) is None:
                    self.airplanes_table[k] = AirplaneController(
                        keyName=status['keyName'],
                        typeName=status['typeName'],
                        updateTimestamp=status['updateTimestamp'],
                        status=status['status'],
                        cameraFront=status['cameraFront'],
                        cameraDown=status['cameraDown'],
                    )
                else:
                    a: AirplaneController = self.airplanes_table.get(k)
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
