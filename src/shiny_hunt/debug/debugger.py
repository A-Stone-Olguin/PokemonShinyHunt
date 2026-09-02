import sys
import cv2

from PySide6.QtWidgets import (
  QApplication,
  QMainWindow,
  QWidget,
  QHBoxLayout,
  QVBoxLayout,
  QLabel,
  QListWidget,
  QPushButton,
)

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap

from shiny_hunt.camera.camera import Camera

class Debugger(QMainWindow):
  def __init__(self, camera: Camera):
    super().__init__()
    self.camera = camera

    self.setWindowTitle("Pokemon Shiny Hunt - Debugger")
    self.resize(1400, 800)

    self.setup_ui()
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.update_frame)
    self.timer.start(30)

  def update_frame(self):
    frame = self.camera.get_game_frame()
    if frame is None:
      return
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    height, width, channels = frame.shape
    bytes_per_line = channels * width
    self.camera_label.frame_size = (width, height)
    image = QImage(
      frame.data,
      width,
      height,
      bytes_per_line,
      QImage.Format_RGB888,
    )

    pixmap = QPixmap.fromImage(image)
    self.camera_label.setPixmap(
      pixmap.scaled(
        self.camera_label.size(),
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation
      )
    )

  def setup_ui(self):
    central_widget = QWidget()
    self.setCentralWidget(central_widget)
    layout = QHBoxLayout(central_widget)

    # Camera
    self.camera_label = CameraView()
    self.camera_label.setMinimumSize(800, 600)

    # Sidebar
    sidebar = QVBoxLayout()

    sidebar.addWidget(QLabel("Regions"))
    self.region_list = QListWidget()
    sidebar.addWidget(self.region_list)

    self.add_region_button = QPushButton("Add Region")
    sidebar.addWidget(self.add_region_button)

    self.save_button = QPushButton("Save")
    sidebar.addWidget(self.save_button)

    sidebar.addStretch()

    layout.addWidget(self.camera_label)
    layout.addLayout(sidebar)

def run_debugger(camera: Camera):
  app = QApplication(sys.argv)

  debugger = Debugger(camera)
  debugger.show()

  sys.exit(app.exec())