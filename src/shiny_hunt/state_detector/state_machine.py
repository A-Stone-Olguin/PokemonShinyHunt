from enum import Enum, auto

class GameState(Enum):
  UNKNOWN = auto()
  RESETTING = auto()
  PROFILE_SELECT = auto()
  OVERWORLD = auto()
  POKEMON = auto()
  SHINY_FOUND = auto()


class StateMachine:
  def __init__(self):
    self.state = GameState.UNKNOWN

  def run(self, observations: dict[str, bool]):
    new_state = self.determine_state(observations)

    if new_state != self.state:
      self.state = new_state

    self.run_state_action()
    return self.state

  def determine_state(self, observations: dict[str, bool]) -> GameState:
    if self.state == GameState.RESETTING:
      if observations.get("profile", False) and observations.get("mystery_gift", False):
        return GameState.PROFILE_SELECT

    elif self.state == GameState.OVERWORLD:
      if observations.get("pokemon", False):
        return GameState.POKEMON


    return self.state

  def run_state_action(self):
    if self.state == GameState.PROFILE_SELECT:
      ## PUSH A
      self.state = GameState.OVERWORLD
      return

    if self.state == GameState.OVERWORLD:
      # Push up continuously
      return

    if self.state == GameState.RESETTING:
      # Push A every half second
      return

    if self.state == GameState.POKEMON:
      # Determine if shiny over next few frames
      # if not shiny, transition to RESETTING
      # If shiny transition to SHINY_FOUND
      return
