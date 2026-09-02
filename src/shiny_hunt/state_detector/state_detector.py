from shiny_hunt.camera.camera import Camera
class StateDetector:
  def __init__(self, camera: Camera):
    self.camera = camera

  def detect(self):
    frame = self.camera.get_game_frame()
    if frame is None:
      print("failed to get frame")
      return

    return self.detect_frame(frame)

  def detect_frame(self, frame):
    return