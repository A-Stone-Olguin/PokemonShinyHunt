from dataclasses import dataclass
import numpy as np
import cv2

@dataclass
class Region:
  name: str
  x: int
  y: int
  width: int
  height: int
  color: tuple = tuple(0, 255, 0) #green

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