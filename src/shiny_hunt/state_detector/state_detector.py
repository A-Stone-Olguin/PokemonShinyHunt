from shiny_hunt.camera.camera import Camera
from shiny_hunt.state_detector.state_machine import StateMachine
from shiny_hunt.region.region import RegionManager
class StateDetector:
  def __init__(self, camera: Camera):
    self.camera = camera
    self.region_manager = RegionManager()
    self.state_machine = StateMachine()

  def detect(self):
    frame = self.camera.get_game_frame()
    if frame is None:
      print("failed to get frame")
      return

    return self.state_machine.run(
      self.region_manager.detect(frame)
    )
