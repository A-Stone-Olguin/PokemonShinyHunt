import serial

class ArduinoConnector:
  def __init__(self, port: str, baudrate: int = 115200):
    self.port = port
    self.baudrate = baudrate
    self.serial = None

  def connect(self):
    self.serial = serial.Serial(
      self.port,
      self.baudrate,
      timeout=1,
    )

  def disconnect(self):
    if self.serial and self.serial.is_open:
      self.serial.close()

  def send(self, command: str):
    if not self.serial or not self.serial.is_open:
      raise RuntimeError("Arduino is not connected")

    self.serial.write(f"{command}\n".encode())

  def read(self):
    if not self.serial or not self.serial.is_open:
      raise RuntimeError("Arduino is not connected")

    return self.serial.readline().decode().strip()