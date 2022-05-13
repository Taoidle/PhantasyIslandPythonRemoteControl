from src.PhantasyIslandPythonRemoteControl.ph0apy import FH0A

fh = FH0A()

# fh.airs.flush()
# fh.airs.start()
# fh.airs.flush()

a = "COM3"

fh.add_uav(a)
fh.sleep(1)

fh.mode(a, 4)
fh.sleep(1)

fh.speed(a, 70)
fh.sleep(1)

fh.takeoff(a, 100)
fh.sleep(3)

fh.led(a, 0, 255, 0)
fh.sleep(1)

fh.goto(a, 50, 50, 200)
fh.sleep(3)
