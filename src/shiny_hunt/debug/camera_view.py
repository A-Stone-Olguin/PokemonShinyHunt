from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QLabel


class CameraView(QLabel):
  def __init__(self):
    super().__init__()

    self.start_point = None
    self.end_point = None
    self.selecting = False

    self.setMouseTracking(True)

  def mousePressEvent(self, event):
    if event.button() != Qt.MouseButton.LeftButton:
      return

    self.start_point = event.position().toPoint()
    self.end_point = self.start_point
    self.selecting = True

    self.update()

  def mouseMoveEvent(self, event):
    if not self.selecting:
      return

    self.end_point = event.position().toPoint()
    self.update()

  def mouseReleaseEvent(self, event):
    if event.button() != Qt.MouseButton.LeftButton:
      return

    self.end_point = event.position().toPoint()
    self.selecting = False

    self.update()

  def paintEvent(self, event):
    super().paintEvent(event)

    if self.start_point is None or self.end_point is None:
      return

    rectangle = QRect(
        self.start_point,
        self.end_point,
    ).normalized()

    painter = QPainter(self)
    painter.setPen(QPen(Qt.GlobalColor.green, 2))
    painter.drawRect(rectangle)