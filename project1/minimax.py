"""Exact graph Minimax for one ghost and layouts without capsules."""

from collections import defaultdict, deque

from pacman_module.game import Agent, Directions


def state_key(state, turn):
    """Identify a state and player, excluding the accumulated score.

    Ghost direction determines its legal moves. Terminal flags distinguish
    a collision from an otherwise similar nonterminal configuration.
    """
    return (
        state.getPacmanPosition(),
        state.getFood(),
        state.getGhostPosition(1),
        state.getGhostDirection(1),
        state.isWin(),
        state.isLose(),
        turn,
    )


class PacmanAgent(Agent):
    """Compute MAX/MIN values on the reachable game graph.

    Values represent future score changes. In this capsule-free game,
    every cycle costs time and cannot gain food indefinitely. Starting
    from terminal nodes and propagating improvements handles cycles
    without a depth cutoff or a heuristic evaluation function.
    """

    def __init__(self):
        """Initialize a policy mapping game states to Pacman actions."""
        super().__init__()
        self.policy = {}

    def get_action(self, state):
        """Return a legal Minimax action for a nonterminal game state."""
        current_key = state_key(state, 0)
        if current_key not in self.policy:
            self.solve(state)

        legal = state.getLegalActions(0)
        action = self.policy.get(current_key, Directions.STOP)
        if action in legal:
            return action
        return legal[0] if legal else Directions.STOP

    def solve(self, initial):
        """Build the reachable graph and solve its Minimax equations.

        Args:
            initial: A game state with exactly one ghost and no capsules.

        Each edge stores the immediate score change. Terminal states
        have zero future reward. MAX selects the greatest total reward;
        MIN selects the least. Unavoidable infinite play has value -inf.
        The resulting optimal Pacman actions are stored in self.policy.
        """
        if initial.getCapsules():
            raise ValueError("This agent supports layouts without capsules.")

        root = state_key(initial, 0)
        frontier = deque([(initial, 0, root)])
        seen = {root}
        edges = {}
        parents = defaultdict(set)
        values = {}
        terminals = []

        while frontier:
            state, turn, node = frontier.popleft()
            edges[node] = []
            values[node] = float("-inf")

            if state.isWin() or state.isLose():
                values[node] = 0
                terminals.append(node)
                continue

            if turn == 0:
                successors = state.generatePacmanSuccessors()
            else:
                successors = state.generateGhostSuccessors(1)

            for child, action in successors:
                child_key = state_key(child, 1 - turn)
                reward = child.getScore() - state.getScore()
                edges[node].append((child_key, action, reward))
                parents[child_key].add(node)
                if child_key not in seen:
                    seen.add(child_key)
                    frontier.append((child, 1 - turn, child_key))

        pending = deque(terminals)
        queued = set(terminals)

        while pending:
            child_key = pending.popleft()
            queued.remove(child_key)
            for node in parents[child_key]:
                candidates = [
                    reward + values[child]
                    for child, action, reward in edges[node]
                ]
                value = max(candidates) if node[-1] == 0 else min(candidates)
                if value > values[node]:
                    values[node] = value
                    if node not in queued:
                        pending.append(node)
                        queued.add(node)

        for node, choices in edges.items():
            if node[-1] == 0 and choices:
                best = max(choices, key=lambda edge: edge[2] + values[edge[0]])
                self.policy[node] = best[1]
