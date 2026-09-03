import cv2

from shiny_hunt.camera.camera import Camera
from shiny_hunt.region.region import Region, RegionManager
from shiny_hunt.state_detector.state_detector import StateDetector

class DetectorDebugger:
  WINDOW_NAME = "Pokemon shiny hunt - Debugger"

  def __init__(self, camera: Camera):
    self.camera = camera
    self.regions = RegionManager()
    self.show_regions = True
    self.selected_region: str | None = None
    self.selected_region: str | None = None
    self.region_window: str | None = None

    # Debug
    self.state_detector = StateDetector(camera)

  def open(self):
    cv2.namedWindow(self.WINDOW_NAME)

    while True:
      frame = self.camera.get_game_frame()

      if frame is None:
        print("Failed to get frame")
        break

      debug_frame = frame.copy()
      status = (
        f"Selected: {self.selected_region}"
        if self.selected_region is not None
        else "Selected: None"
      )

      cv2.putText(
        debug_frame,
        status,
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
      )

      if self.show_regions:
        self.regions.draw(debug_frame, selected=self.selected_region)

      cv2.imshow(self.WINDOW_NAME, debug_frame)
      if self.selected_region is not None:
        region = self.regions.get(self.selected_region)

        if region is not None:
          cv2.imshow(
            self.region_window,
            region.crop(frame),
          )

      state = self.state_detector.detect()
      print("Current state", state)
        

      key = cv2.waitKey(1) & 0xFF

      if key == ord("q"):
        break
      elif key == ord("r"):
        self.add_region()
      elif key == ord("d"):
        self.show_regions = not self.show_regions
      elif key == ord("s"):
        self.regions.save()
        print("Regions saved")
      elif key == ord("l"):
        self.regions.load()
        print("Regions loaded")
      elif key in range(ord("0"), ord("9")):
        index = key - ord("0")

        if index < len(self.regions.regions):
          if self.region_window is not None:
            cv2.destroyWindow(self.region_window)

          self.selected_region = list(self.regions.regions.keys())[index]
          self.region_window = f"Region: {self.selected_region}"
      elif key == ord("x"): #eXit selection
        if self.region_window is not None:
          cv2.destroyWindow(self.region_window)
          self.region_window = None
        self.selected_region = None
      elif key == ord("e"): # erase
        if self.selected_region is not None:
          self.regions.remove(self.selected_region)
          if self.region_window is not None:
            cv2.destroyWindow(self.region_window)
            self.region_window = None
          self.selected_region = None
      elif key == ord("c"): # Crop and template
        if self.selected_region is None:
          continue
        region = self.regions.get(self.selected_region)
        if region is not None:
          crop = region.crop(frame)

          print(f"Region size: {crop.shape[1]}x{crop.shape[0]}")
          average_color = crop.mean(axis=(0, 1))
          print(f"Average BGR: {average_color.astype(int)}")

          fname = f"./debug/{region.name}.png"
          cv2.imwrite(
            fname,
            crop
          )
          self.regions.add_template(region.name, crop)
          print("Saved to", fname)
      elif key == ord("f"):
        fname = "./debug/full.png"
        cv2.imwrite(fname)
        print("Saved ", fname)
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