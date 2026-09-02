import cv2

from shiny_hunt.camera.camera import Camera
from shiny_hunt.state_detector.region import Region, RegionManager

class DetectorDebugger:
  WINDOW_NAME = "Pokemon shiny hunt - Debugger"

  def __init__(self, camera: Camera):
    self.camera = camera
    self.regions = RegionManager()
    self.show_regions = True

  def open(self):
    cv2.namedWindow(self.WINDOW_NAME)

    while True:
      frame = self.camera.get_game_frame()

      if frame is None:
        print("Failed to get frame")
        break

      debug_frame = frame.copy()

      if self.show_regions:
        self.regions.draw(debug_frame)

      cv2.imshow(self.WINDOW_NAME, debug_frame)

      key = cv2.waitKey(1) & 0xFF

      if key == ord("q"):
        break
      elif key == ord("r"):
        self.add_region()
      elif key == ord("d"):
        self.show_regions = not self.show_regions
      elif key == ord("s"):
        self.regions.save()
      elif key == ord("l"):
        self.regions.load()
    cv2.destroyAllWindows()


  def add_region(self):
    print("Select a region with your mouse")
    frame = self.camera.get_game_frame()
    if frame is None:
      return
    region = cv2.selectROI(
      self.WINDOW_NAME,
      frame,
      fromCenter=False,
      showCrosshair=True
    )
    x, y, width, height = region
    if width == 0 or height == 0:
      return
    name = input("Region name: ")

    self.regions.add(
      Region(
        name=name,
        x=x,
        y=y,
        width=width,
        height=height
      )
    )