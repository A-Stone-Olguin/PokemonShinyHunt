import cv2

class Camera:

  def __init__(self, frame_name):
    self.frame_name = frame_name
    try: 
      self.camera = cv2.VideoCapture(0)
    except:
      err_msg = "Could not detect camera. Please ensure one is plugged in"
      print(err_msg)
      raise Exception(err_msg)

  def open(self):
    while True:
      ret, frame = self.camera.read()

      if not ret:
        print("Could not read webcam")
        break

      cv2.imshow(self.frame_name, frame)

      if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    self.camera.release()
    cv2.destroyAllWindows()