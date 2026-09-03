from enum import Enum, auto


class GameState(Enum):
  UNKNOWN = auto()
  STARTUP = auto()
  OVERWORLD = auto()
  ENCOUNTER = auto()
  SHINY_CHECK = auto()
  RESETTING = auto()
  BATTLE = auto()
  LOADING = auto()


class StateMachine:
  def __init__(self):
    self.state = GameState.UNKNOWN

  def update(self, observations):
    new_state = self.determine_state(observations)

    if new_state != self.state:
      self.on_exit(self.state)
      self.state = new_state
      self.on_enter(self.state)

  def determine_state(self, observations) -> GameState:
    return GameState.UNKNOWN

  def on_exit(state: GameState):
    return

  def on_enter(state: GameState):
    return