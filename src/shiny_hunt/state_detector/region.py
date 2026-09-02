@dataclass
class Region:
  name: str
  x: int
  y: int
  width: int
  height: int

  def __init__(self, name, x, y, width, height):
    self.name = name
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    pass

  def crop(self, frame):
    return frame[
      self.y:self.y + self.height,
      self.x:self.x + self.width
    ]