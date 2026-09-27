"""Depth-limited Minimax with alpha-beta pruning for one unscared ghost."""

from collections import deque

from pacman_module.game import Agent, Directions


class PacmanAgent(Agent):
    """Search four complete Pacman/ghost rounds with a heuristic cutoff."""

    def __init__(self):
        """Initialize the search depth and maze-distance cache."""
        super().__init__()
        self.depth = 4
        self.distances = {}
        self.walls = None
        self.table = {}

    def distance_map(self, start):
        """Return shortest walking distances from start using static walls."""
        if start not in self.distances:
            distances = {start: 0}
            queue = deque([start])
            while queue:
                x, y = queue.popleft()
                for point in ((x + 1, y), (x - 1, y),
                              (x, y + 1), (x, y - 1)):
                    nx, ny = point
                    if not (0 <= nx < self.walls.width and
                            0 <= ny < self.walls.height):
                        continue
                    if self.walls[nx][ny] or point in distances:
                        continue
                    distances[point] = distances[(x, y)] + 1
                    queue.append(point)
            self.distances[start] = distances
        return self.distances[start]

    def evaluate(self, state):
        """Estimate desirability from score, food distance and ghost danger.

        Terminal states dominate nonterminal estimates. The food term
        rewards progress; maze distances guide movement around walls.
        This heuristic is for one ghost and layouts without capsules.
        """
        score = state.getScore()
        if state.isWin():
            return 100000 + score
        if state.isLose():
            return -100000 + score

        distances = self.distance_map(state.getPacmanPosition())
        food = state.getFood()
        nearest = min(
            (distances.get((x, y), 1000)
             for x in range(food.width)
             for y in range(food.height) if food[x][y]),
            default=0,
        )
        ghost_distance = distances.get(state.getGhostPosition(1), 1000)
        danger = 12.0 / max(1, ghost_distance)
        return score - 20 * state.getNumFood() - 2 * nearest - danger

    def get_action(self, state):
        """Return the best legal move under a depth-limited worst case."""
        if state.getCapsules():
            raise ValueError("This agent supports layouts without capsules.")
        walls = state.getWalls()
        if self.walls != walls:
            self.walls = walls
            self.distances.clear()
        self.table = {}
        successors = state.generatePacmanSuccessors()
        successors.sort(key=lambda item: self.evaluate(item[0]), reverse=True)
        best_value = float("-inf")
        legal = state.getLegalActions(0)
        best_action = legal[0] if legal else Directions.STOP

        for child, action in successors:
            value = self.search(
                child, self.depth, 1, best_value, float("inf")
            )
            if value > best_value:
                best_value, best_action = value, action
        return best_action

    def search(self, state, depth, turn, alpha, beta):
        """Return a Minimax value or valid alpha-beta bound.

        Depth counts complete rounds and decreases after the ghost moves.
        Cache entries record exact values or bounds, never treating a
        pruned result as exact. Game successors use the required API.
        """
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluate(state)

        key = (
            state.getPacmanPosition(), state.getFood(),
            state.getGhostPosition(1), state.getGhostDirection(1),
            state.getScore(), depth, turn,
        )
        original_alpha, original_beta = alpha, beta
        if key in self.table:
            value, flag = self.table[key]
            if flag == "exact":
                return value
            if flag == "lower":
                alpha = max(alpha, value)
            else:
                beta = min(beta, value)
            if alpha >= beta:
                return value

        if turn == 0:
            successors = state.generatePacmanSuccessors()
        else:
            successors = state.generateGhostSuccessors(1)
        if not successors:
            return self.evaluate(state)
        successors.sort(
            key=lambda item: self.evaluate(item[0]), reverse=(turn == 0)
        )

        value = float("-inf") if turn == 0 else float("inf")
        for child, action in successors:
            child_value = self.search(
                child, depth - turn, 1 - turn, alpha, beta
            )
            if turn == 0:
                value = max(value, child_value)
                alpha = max(alpha, value)
            else:
                value = min(value, child_value)
                beta = min(beta, value)
            if alpha >= beta:
                break

        flag = "exact"
        if value <= original_alpha:
            flag = "upper"
        elif value >= original_beta:
            flag = "lower"
        self.table[key] = (value, flag)
        return value
