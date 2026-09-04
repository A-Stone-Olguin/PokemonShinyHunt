from shiny_hunt.camera.camera import Camera
from shiny_hunt.debug.detector_debugger import DetectorDebugger
from shiny_hunt.controllers.arduino import ArduinoController, ArduinoConnector
import time

def main():
  # camera = Camera("3DS", "./calibration.json")
  # camera.open()
  # camera = Camera("3DS", "./calibration.json")
  # debugger = DetectorDebugger(camera)
  # debugger.open()
  arduino = ArduinoController(ArduinoConnector("/dev/ttyACM0"))
  while True:
    arduino.press_start()
    time.sleep(1)
    arduino.ping()


if __name__ == "__main__":
  main()