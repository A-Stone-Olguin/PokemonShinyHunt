from shiny_hunt.hardware.arduino import ArduinoConnector
class ArduinoController:
  def __init__(self, connector: ArduinoConnector):
    self.connector = connector

  def press(self, button: str, duration: float = 0.1):
    self.connector.send(f"PRESS {button} {duration}")

  def release(self, button: str):
    self.connector.send(f"RELEASE {button}")

  def press_a(self):
    self.press("A")

  def press_b(self):
    self.press("B")

  def press_up(self):
    self.press("UP")

  def press_down(self):
    self.press("DOWN")

  def press_left(self):
    self.press("LEFT")

  def press_right(self):
    self.press("RIGHT")