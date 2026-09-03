from dataclasses import dataclass
import numpy as np
import cv2
import json

@dataclass
class Region:
  name: str
  x: int
  y: int
  width: int
  height: int
  color: tuple = tuple([0, 255, 0]) #green
  threshold: int = 0.85
  template: np.ndarray | None = None # The reference template

  def crop(self, frame: np.ndarray) -> np.ndarray:
    return frame[
      self.y:self.y + self.height,
      self.x:self.x + self.width
    ]

  def draw(
    self,
    frame: np.ndarray,
    label: bool = True,
    selected: bool = False,
  ) -> None:
    thickness = 3 if selected else 2
    cv2.rectangle(
      frame,
      (self.x, self.y),
      (self.x + self.width, self.y + self.height),
      self.color,
      thickness,
    )

    if label:
      cv2.putText(
        frame,
        self.name,
        (self.x, self.y-8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        self.color,
        thickness,
      )

  def add_template(self, template: np.ndarray):
    self.template = template

  def matches(self, frame: np.ndarray) -> bool:
    if self.template is None:
      return False

    current = self.crop(frame)

    result = cv2.matchTemplate(
      current,
      self.template,
      cv2.TM_CCOEFF_NORMED,
    )
    score = result[0][0]
    print("DEBUG:", "region", self.name, "score", score)
    return score >= self.threshold

class RegionManager:
  SAVED_PATH = "./config/regions.json"
  def __init__(self):
    self.regions: dict[str, Region] = {}

  def add(self, region: Region):
    self.regions[region.name] = region

  def get(self, name: str) -> Region | None:
    try:
      return self.regions[name]
    except KeyError:
      print("Region name not found")
      return None

  def draw(self, frame: np.ndarray, selected: str | None = None):
    for i, region in enumerate(self.regions.values()):
      region.draw(frame, selected=(region.name == selected))

      cv2.putText(
        frame,
        str(i),
        (region.x, region.y + region.height + 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        region.color,
        2
      )

  def save(self):
    data = {
      name: {
        "x": region.x,
        "y": region.y,
        "width": region.width,
        "height": region.height,
        "template": region.template,
      }
      for name, region in self.regions.items()
    }
    with open(self.SAVED_PATH, "w") as f:
      json.dump(data, f, indent=2)

  def load(self):
    with open(self.SAVED_PATH, "r") as f:
      data = json.load(f)

    for name, values in data.items():
      self.add(
        Region(
          name=name,
          **values,
        )
      )

  def remove(self, name: str):
    if name in self.regions:
      del self.regions[name]

  def detect(self, frame: np.ndarray):
    return [region.matches(self, frame) for region in self.regions.values()]

  def add_template(self, name: str, template: np.ndarray):
    if name in self.regions:
      self.regions[name].add_template(template)
