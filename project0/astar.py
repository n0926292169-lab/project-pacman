"""A* search agent for the ghost-free Pacman project."""

import heapq
from collections import deque
from itertools import count

from pacman_module.game import Agent
from pacman_module.pacman import Directions


def key(state):
    """Return position, remaining food and capsules as a state key."""
    return (
        state.getPacmanPosition(),
        state.getFood(),
        tuple(sorted(state.getCapsules())),
    )


def heuristic(state):
    """Return a lower bound on the remaining movement cost.

    The Manhattan distance to the farthest remaining food cannot
    exceed the steps required to collect all remaining food.
    Walls and capsule penalties are ignored for this lower bound.
    """
    food = state.getFood()
    pacman_x, pacman_y = state.getPacmanPosition()
    farthest = 0

    for x in range(food.width):
        for y in range(food.height):
            if food[x][y]:
                distance = abs(x - pacman_x) + abs(y - pacman_y)
                farthest = max(farthest, distance)

    return farthest


class PacmanAgent(Agent):
    """Plan a winning route using A* with nonnegative costs."""

    def __init__(self, args):
        """Store command-line arguments and initialize the plan."""
        self.args = args
        self.moves = deque()
        self.planned = False

    def get_action(self, state):
        """Return the next legal action for the current state."""
        if not self.planned:
            self.moves = deque(self.astar(state))
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

    def astar(self, state):
        """Return a minimum-cost winning path, or [] if none exists.

        Each move costs 1, plus 5 for each capsule consumed.
        Among winning routes in a ghost-free maze, minimizing this
        cost maximizes the score because food and win rewards are fixed.
        """
        frontier = []
        order = count()
        best_cost = {key(state): 0}

        heapq.heappush(
            frontier,
            (heuristic(state), next(order), 0, state, []),
        )

        while frontier:
            _, _, cost, current, path = heapq.heappop(frontier)
            current_key = key(current)

            # Ignore entries superseded by a cheaper route.
            if cost != best_cost.get(current_key):
                continue

            if current.isWin():
                return path

            capsule_count = len(current.getCapsules())

            for next_state, action in current.generatePacmanSuccessors():
                capsules_eaten = (
                    capsule_count - len(next_state.getCapsules())
                )
                next_cost = cost + 1 + 5 * capsules_eaten
                next_key = key(next_state)

                if next_cost >= best_cost.get(next_key, float("inf")):
                    continue

                best_cost[next_key] = next_cost
                priority = next_cost + heuristic(next_state)

                heapq.heappush(
                    frontier,
                    (
                        priority,
                        next(order),
                        next_cost,
                        next_state,
                        path + [action],
                    ),
                )

        return []
