from Game.Tetris import Tetris
from Solver.DQNAgent import DQNAgent

tetris = Tetris(auto_restart_on_lose = False)
DQN = DQNAgent(tetris)
tetris.run()

# DQN.solve(100000)

