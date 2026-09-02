from shiny_hunt.camera.camera import Camera
from shiny_hunt.debug.detector_debugger import DetectorDebugger
from shiny_hunt.debug.debugger import run_debugger

def main():
  camera = Camera("3DS", "./calibration.json")
  # camera.open()
  # debugger = DetectorDebugger(camera)
  # debugger.open()
  run_debugger(camera)


if __name__ == "__main__":
  main()