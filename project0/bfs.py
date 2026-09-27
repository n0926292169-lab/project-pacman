# Breadth-first search agent for Project 0.

from collections import deque

from pacman_module.game import Agent
from pacman_module.pacman import Directions


def key(state):
    """Return a hashable key for a ghost-free search state."""
    return (
        state.getPacmanPosition(),
        state.getFood(),
        tuple(sorted(state.getCapsules())),
    )


class PacmanAgent(Agent):
    """Find a winning path using breadth-first search."""

    def __init__(self, args):
        """Store arguments and initialize the planned moves."""
        self.args = args
        self.moves = deque()
        self.planned = False

    def get_action(self, state):
        """Return the next legal move for the current game state."""
        if not self.planned:
            self.moves = deque(self.bfs(state))
            self.planned = True

        legal_actions = state.getLegalActions(0)

        if self.moves:
            action = self.moves.popleft()
            if action in legal_actions:
                return action
            self.moves.clear()
            self.planned = False

        if Directions.STOP in legal_actions:
            return Directions.STOP

        return legal_actions[0] if legal_actions else Directions.STOP

    def bfs(self, state):
        """Return a shortest winning action list, or [] if none exists."""
        frontier = deque([(state, [])])
        visited = {key(state)}

        while frontier:
            current_state, path = frontier.popleft()

            if current_state.isWin():
                return path

            successors = current_state.generatePacmanSuccessors()

            for next_state, action in successors:
                next_key = key(next_state)

                if next_key in visited:
                    continue

                visited.add(next_key)
                frontier.append((next_state, path + [action]))

        return []
