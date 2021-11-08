from .airplane_core import AirplaneCore
from .http_layer import send_cmd


class AirplaneController(AirplaneCore):
    count: int = 1

    def _next_count(self):
        self.count = self.count * 2 + 1
        return self.count

    def _prepare_command(self, command: str) -> str:
        return self.keyName + ' ' + str(self._next_count()) + ' ' + command

    def _send_cmd(self, command: str) -> str:
        return send_cmd(self._prepare_command(command))

    def takeoff(self, high: int):
        """
        takeoff函数用于控制无人机起飞
        :param high: 起飞到指定高度
        :return:
        """
        return self._send_cmd(f"takeoff {high}")

    def land(self):
        """
        land函数用于控制无人机降落
        """
        return self._send_cmd(f"land")

    def emergency(self):
        return self._send_cmd(f"emergency")

    def up(self, distance: int):
        """
        up 向上移动
        :param distance:移动距离（厘米）
        """
        return self._send_cmd(f"up {distance}")

    def down(self, distance: int):
        """
        down 向下移动
        :param distance:移动距离（厘米）
        """
        return self._send_cmd(f"down {distance}")

    def forward(self, distance: int):
        """
        forward 向前移动
        :param distance:移动距离（厘米）
        """
        return self._send_cmd(f"forward {distance}")

    def back(self, distance: int):
        """
        back 向后移动
        :param distance:移动距离（厘米）
        """
        return self._send_cmd(f"back {distance}")

    def left(self, distance: int):
        """
        left 向左移动
        :param distance:移动距离（厘米）
        """
        return self._send_cmd(f"left {distance}")

    def right(self, distance: int):
        """
        right 向右移动
        :param distance:移动距离（厘米）
        """
        return self._send_cmd(f"right {distance}")

    def goto(self, x: int, y: int, h: int):
        """
        goto 函数用于控制无人机到达指定位置
        :param x: x轴方向位置（厘米）
        :param y: y轴方向位置（厘米）
        :param h: 高度（厘米）
        """
        return self._send_cmd(f"goto {x} {y} {h}")

    def rotate(self, degree: int):
        """
        rotate函数用于控制无人机旋转
        :param degree: 自转方向和角度（正数顺时针，负数逆时针，单位为度数）
        """
        return self._send_cmd(f"rotate {degree}")

    def cw(self, degree: int):
        """
        cw 控制无人机顺时针自转
        :param degree: 自转角度度数
        """
        return self._send_cmd(f"cw {degree}")

    def ccw(self, degree: int):
        """
        ccw 函数用于控制无人机逆时针自转
        :param degree: 自转角度度数
        """
        return self._send_cmd(f"ccw {degree}")

    def high(self, high: int):
        """
        high用于控制无人机飞行高度
        :param high: 飞行到指定高度
        :return:
        """
        return self._send_cmd(f"high {high}")

    def speed(self, speed: int):
        """
        speed函数用于控制无人机飞行速度
        :param speed: 飞行速度（0-200厘米/秒）
        """
        return self._send_cmd(f"setSpeed {speed}")

    def led(self, r: int, g: int, b: int):
        """
        led函数控制无人机灯光为指定颜色
        :param r: 灯光颜色R通道
        :param g: 灯光颜色G通道
        :param b: 灯光颜色B通道
        """
        return self._send_cmd(f"light {r} {g} {b}")

    def bln(self, r: int, g: int, b: int):
        """
        led函数控制无人机灯光，呼吸灯
        :param r: 灯光颜色R通道
        :param g: 灯光颜色G通道
        :param b: 灯光颜色B通道
        """
        return self._send_cmd(f"bln {r} {g} {b}")

    def rainbow(self, r: int, g: int, b: int):
        """
        led函数控制无人机灯光，七彩变换
        :param r: 灯光颜色R通道
        :param g: 灯光颜色G通道
        :param b: 灯光颜色B通道
        """
        return self._send_cmd(f"rainbow {r} {g} {b}")

    def stop(self):
        return self.hover()

    def hover(self):
        """
        hover 函数用于控制无人机悬停
        """
        return self._send_cmd(f"hover")

    pass
