from shiny_hunt.camera.camera import Camera

def main():
  camera = Camera("3DS", "./calibration.json")
  camera.open()

if __name__ == "__main__":
  main()