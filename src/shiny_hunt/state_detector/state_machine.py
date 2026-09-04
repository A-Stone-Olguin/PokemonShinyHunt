from enum import Enum, auto
import time
from shiny_hunt.controllers.arduino import ArduinoController

class GameState(Enum):
  UNKNOWN = auto()
  RESETTING = auto()
  PROFILE_SELECT = auto()
  OVERWORLD = auto()
  POKEMON = auto()
  SHINY_FOUND = auto()


class StateMachine:
  def __init__(self, controller: ArduinoController):
    self.state = GameState.UNKNOWN
    self.controller = controller
    self.last_action_time = 0
    self.overworld_set = 0

  def run(self, observations: dict[str, bool]):
    new_state = self.determine_state(observations)

    if new_state != self.state:
      self.state = new_state

    self.run_state_action()
    return self.state

  def determine_state(self, observations: dict[str, bool]) -> GameState:
    print("Observations", observations)
    if self.state != GameState.OVERWORLD:
      if observations.get("profile", False) and observations.get("mystery_gift", False):
        return GameState.PROFILE_SELECT
    else:
      # If we match the pokemon, that means it is a duplicate.
      # If we fail to match that means either false positive
      # Or shiny detected.
      if observations.get("pokemon", True):
        return GameState.POKEMON

    return self.state

  def run_state_action(self):
    now = time.monotonic()
    if self.state == GameState.PROFILE_SELECT:
      if now - self.last_action_time >= 0.5:
        # Push A every half second
        print("RESET: PUSH A")
        self.controller.press_a()
        self.last_action_time = now
      return

    if self.state == GameState.OVERWORLD:
      if self.overworld_set == 0:
        self.overworld_set = now
      self.controller.stick_up()
      return

    if self.state == GameState.RESETTING:
      if now - self.last_action_time >= 0.5:
        # Push A every half second
        print("RESET: PUSH A, RELEASE")
        self.controller.stick_release()
        self.controller.press_a()
        self.last_action_time = now
      return

    if self.state == GameState.POKEMON:
      # If no match found after 50 seconds, we are done
      if now - self.overworld_set >= 50:
        self.state == GameState.SHINY_FOUND
        print("FOUND SHINY!!!!")
        return

      # If we match
      if now - self.last_action_time >= 0.5:
        print("FOUND MATCH, RESETTING")
        self.overworld_set = 0
        self.controller.press_start()
        self.last_action_time = now
        self.state == GameState.RESETTING
      return
