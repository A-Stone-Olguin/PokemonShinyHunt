from shiny_hunt.hardware.arduino import ArduinoConnector
class ArduinoController:
  def __init__(self, connector: ArduinoConnector):
    self.connector = connector
    connector.connect()

  def press(self, button: str):
    self.connector.send(f"PRESS_{button}")

  def release(self, button: str):
    self.connector.send(f"RELEASE_{button}")

  def press_a(self):
    self.press("A")

  def press_b(self):
    self.press("B")

  def press_start(self):
    self.press("START")

  def press_up(self):
    self.press("UP")

  def press_down(self):
    self.press("DOWN")

  def press_left(self):
    self.press("LEFT")

  def press_right(self):
    self.press("RIGHT")

  def ping(self):
    self.connector.send("PING")