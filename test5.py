from src.PhantasyIslandPythonRemoteControl.airplane_manager import get_airplane_manager

m = get_airplane_manager()

m.flush()
m.start()
m.flush()

a = m.get_airplane('COM3')
m.sleep(1)

a.mode(4)
m.sleep(1)

a.speed(70)
m.sleep(1)

a.takeoff(100)
m.sleep(3)

a.led(0, 255, 0)
m.sleep(1)

a.goto(50, 50, 200)
m.sleep(3)
