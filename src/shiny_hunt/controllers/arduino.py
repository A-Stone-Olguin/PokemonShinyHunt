from shiny_hunt.hardware.arduino import ArduinoConnector
class ArduinoController:
  def __init__(self, connector: ArduinoConnector):
    self.connector = connector
    connector.connect()

  def press(self, button: str):
    self.connector.send(f"PRESS_{button}")

  def stick(self, direction: str):
    self.connector.send(f"STICK_{direction}")

  def release(self, button: str):
    self.connector.send(f"RELEASE_{button}")

  def press_a(self):
    self.press("A")

  def press_b(self):
    self.press("B")

  def press_start(self):
    self.press("START")

  def stick_up(self):
    self.stick("UP")

  def stick_release(self):
    self.stick("RELEASE")

   #### FOR D-PAD
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