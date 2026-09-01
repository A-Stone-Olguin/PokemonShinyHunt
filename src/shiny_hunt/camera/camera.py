import cv2
import json
import numpy as np

class Camera:

  def __init__(self, frame_name, calibration_file):
    self.frame_name = frame_name
    self.points = []
    self.width = 1920
    self.height = 1080
    self.calibration_color = (0, 255, 0) # Green
    try: 
      self.camera = cv2.VideoCapture(0)
    except:
      err_msg = "Could not detect camera. Please ensure one is plugged in"
      print(err_msg)
      raise Exception(err_msg)

    self.load_calibration(calibration_file)
    

  def open(self):
    while True:
      frame = self.get_game_frame()

      if frame is None:
        print("Could not read webcam")
        break

      cv2.imshow(self.frame_name, frame)

      if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    self.camera.release()
    cv2.destroyAllWindows()

  def load_calibration(self, json_file):
    try:
      with open(json_file, "r") as f:
        d = json.load(f)
    except FileNotFoundError:
      print("No calibration found. Prompting user to create")
      self.save_calibration(json_file)
      with open(json_file, "r") as f:
        d = json.load(f)

    # TODO: Assert calibration values

    source = np.float32([
      d["top_left"],
      d["top_right"],
      d["bottom_right"],
      d["bottom_left"]
    ])

    destination = np.float32([
      [0, 0],
      [self.width -1, 0],
      [self.width-1, self.height-1],
      [0, self.height -1],
    ])
    self.matrix = cv2.getPerspectiveTransform(source, destination)
    return

  def mouse_callback(self, event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
      if len(self.points) < 4:
        self.points.append((x, y))
        print(f"Point {len(self.points)}: ({x}, {y})")

  def save_calibration(self, json_file):
    self.points.clear()
    window_name = "Calibration"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, self.mouse_callback)

    while True:
      ret, frame = self.camera.read()
      if not ret:
          print("Failed to capture frame from camera")
          break
      display = frame.copy()

      self.draw_selected_points(display)
      self.draw_lines(display)
      cv2.imshow(window_name, display)

      key = cv2.waitKey(1) & 0xFF
      # Enter => Accept
      if key == 13 and len(self.points) == 4:
        break

      # R => reset
      if key == ord("r"):
        self.points.clear()
        print("points reset")

      # ESC => Quit
      if key == 27:
        self.points.clear()
        break

    cv2.destroyAllWindows()

    if len(self.points) == 4:
      calibration = {
        "top_left": self.points[0],
        "top_right": self.points[1],
        "bottom_right": self.points[2],
        "bottom_left": self.points[3],
      }

      with open(json_file, "w") as f:
        json.dump(calibration, f, indent=4)

      print("calibration saved!")
    return

  def draw_selected_points(self, display):
    for i, (x, y) in enumerate(self.points):
      cv2.circle(display, (x, y), 8, self.calibration_color, -1)
      cv2.putText(
        display,
        str(i+1),
        (x + 10, y -10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        self.calibration_color,
        2,
      )

  def draw_lines(self, display):
    if len(self.points) >= 2:
      for i in range(len(self.points) - 1):
        cv2.line(display, self.points[i], self.points[i + 1], self.calibration_color, 2)

    if len(self.points) == 4:
      cv2.line(display, self.points[3], self.points[0], self.calibration_color, 2)

  def get_game_frame(self):
      ret, frame = self.camera.read()

      if not ret:
        print("Could not read webcam")
        return

      return cv2.warpPerspective(
        frame,
        self.matrix,
        (self.width, self.height),
      )