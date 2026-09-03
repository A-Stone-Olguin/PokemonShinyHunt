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
    self.run_state_action()
    new_state = self.determine_state(observations)

    if new_state != self.state:
      self.transition_to(new_state)
    return self.state

  def determine_state(self, observations: dict[str, bool]) -> GameState:
    if self.state == GameState.RESETTING:
      if observations.get("profile", False) and observations.get("mystery_gift", False):
        return GameState.PROFILE_SELECT

    elif self.state == GameState.OVERWORLD:
      if observations.get("pokemon", False):
        return GameState.POKEMON


    return self.state

  def on_exit(self, state: GameState):
    return

  def on_enter(self, state: GameState):
    if state == GameState.PROFILE_SELECT:
      ## PUSH A
      self.transition_to(GameState.OVERWORLD)
    return

  def transition_to(self, new_state: GameState):
    self.on_exit(self.state)
    self.state = new_state
    self.on_enter(self.state)

  def run_state_action(self):
    if self.state == GameState.OVERWORLD:
      # Push up continuously
      return

    if self.state == GameState.RESETTING:
      # Push A every half second
      return
