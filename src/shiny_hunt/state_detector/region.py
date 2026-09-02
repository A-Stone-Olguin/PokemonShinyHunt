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

  def crop(self, frame: np.ndarray) -> np.ndarray:
    return frame[
      self.y:self.y + self.height,
      self.x:self.x + self.width
    ]

  def draw(
    self,
    frame: np.ndarray,
    label: bool = True,
  ) -> None:
    cv2.rectangle(
      frame,
      (self.x, self.y),
      (self.x + self.width, self.y + self.height),
      self.color,
      2,
    )

    if label:
      cv2.putText(
        frame,
        self.name,
        (self.x, self.y-8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        self.color,
        2,
      )

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

  def draw(self, frame: np.ndarray):
    for region in self.regions.values():
      region.draw(frame)

  def save(self):
    data = {
      name: {
        "x": region.x,
        "y": region.y,
        "width": region.width,
        "height": region.height,
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
