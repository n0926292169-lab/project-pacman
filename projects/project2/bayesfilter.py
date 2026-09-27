# Complete this class for all parts of the project

from pacman_module.game import Agent
import numpy as np
from pacman_module import util
from scipy.stats import binom


class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

        """
            Variables to use in 'update_belief_state' method.
            Initialization occurs in 'get_action' method.

            XXX: DO NOT MODIFY THE DEFINITION OF THESE VARIABLES
            # Doing so will result in a 0 grade.
        """

        # Current list of belief states over ghost positions
        self.beliefGhostStates = None

        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None

        # Hyper-parameters
        self.ghost_type = self.args.ghostagent
        self.sensor_variance = self.args.sensorvariance

        self.p = 0.5
        self.n = int(self.sensor_variance/(self.p*(1-self.p)))

        # XXX: Your code here
        # NB: Adding code here is not necessarily useful, but you may.
        # XXX: End of your code

    def _get_sensor_model(self, pacman_position, evidence):
        """Return P(evidence | ghost cell) as a [width, height] array.

        Evidence equals Manhattan distance plus B - n*p, where
        B is binomial(n, p). Wall cells have likelihood zero.
        """
        width, height = self.walls.width, self.walls.height
        x, y = np.indices((width, height))
        distance = (abs(x - pacman_position[0]) +
                    abs(y - pacman_position[1]))
        successes = evidence - distance + self.n * self.p
        likelihood = binom.pmf(successes, self.n, self.p)
        for x in range(width):
            for y in range(height):
                if self.walls[x][y]:
                    likelihood[x, y] = 0.0
        return likelihood

    def _get_transition_model(self, pacman_position):
        """Return T[new_x, new_y, old_x, old_y] for one ghost move.

        Legal orthogonal moves, including reversals, receive weight
        1, 2 or 8 when moving away from Pacman for confused, afraid or
        scared ghosts, respectively. Other moves receive weight 1.
        Normalize separately at each free source cell; walls have zero
        mass. An isolated free cell has a self-transition of probability 1.
        """
        width, height = self.walls.width, self.walls.height
        transition = np.zeros((width, height, width, height))
        away_weight = {"confused": 1.0, "afraid": 2.0, "scared": 8.0}
        weight = away_weight[self.ghost_type]
        px, py = pacman_position
        for x in range(width):
            for y in range(height):
                if self.walls[x][y]:
                    continue
                old_distance = abs(x - px) + abs(y - py)
                moves = []
                for nx, ny in ((x + 1, y), (x - 1, y),
                               (x, y + 1), (x, y - 1)):
                    if not (0 <= nx < width and 0 <= ny < height):
                        continue
                    if self.walls[nx][ny]:
                        continue
                    new_distance = abs(nx - px) + abs(ny - py)
                    value = weight if new_distance >= old_distance else 1.0
                    moves.append((nx, ny, value))
                if not moves:
                    transition[x, y, x, y] = 1.0
                    continue
                total = sum(value for nx, ny, value in moves)
                for nx, ny, value in moves:
                    transition[nx, ny, x, y] = value / total
        return transition

    def _get_updated_belief(self, belief, evidences, pacman_position,
                            ghosts_eaten):
        """Predict, condition on evidence, and normalize each ghost belief.

        Args:
            belief: List of previous [width, height] probability arrays.
            evidences: One noisy Manhattan distance per ghost.
            pacman_position: Current (x, y) Pacman coordinates.
            ghosts_eaten: One Boolean per ghost; True means already eaten.

        Returns:
            Fresh probability arrays, normalized for active ghosts and
            identically zero for eaten ghosts. If evidence has zero
            probability under the predicted prior, reinitialize using
            its likelihood over free cells; if that too is impossible,
            retain the normalized prediction (or uniform free-cell prior).
        """
        transition = self._get_transition_model(pacman_position)
        free = np.array([
            [not self.walls[x][y] for y in range(self.walls.height)]
            for x in range(self.walls.width)
        ], dtype=float)
        updated = []
        for prior, evidence, eaten in zip(belief, evidences, ghosts_eaten):
            if eaten:
                updated.append(np.zeros_like(free))
                continue
            predicted = np.einsum("ijxy,xy->ij", transition, prior)
            sensor = self._get_sensor_model(pacman_position, evidence)
            posterior = predicted * sensor
            total = posterior.sum()
            if total <= 0:
                posterior = sensor.copy()
                total = posterior.sum()
            if total <= 0:
                posterior = predicted * free
                total = posterior.sum()
            if total <= 0:
                posterior = free.copy()
                total = posterior.sum()
            updated.append(posterior / total)
        return updated

    def update_belief_state(self, evidences, pacman_position, ghosts_eaten):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `evidences`: list of distances between
          pacman and ghosts at state x_{t}
          where 't' is the current time step
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step
        - `ghosts_eaten`: list of booleans indicating
          whether ghosts have been eaten or not

        Return:
        -------
        - A list of Z belief states at state x_{t}
          as N*M numpy mass probability matrices
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        XXX: DO NOT MODIFY THIS FUNCTION !!!
        Doing so will result in a 0 grade.
        """
        belief = self._get_updated_belief(self.beliefGhostStates, evidences,
                                          pacman_position, ghosts_eaten)
        self.beliefGhostStates = belief
        return belief

    def _get_evidence(self, state):
        """
        Computes noisy distances between pacman and ghosts.

        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.


        Return:
        -------
        - A list of Z noised distances in real numbers
          where Z is the number of ghosts.

        XXX: DO NOT MODIFY THIS FUNCTION !!!
        Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        pacman_position = state.getPacmanPosition()
        noisy_distances = []

        for pos in positions:
            true_distance = util.manhattanDistance(pos, pacman_position)
            noise = binom.rvs(self.n, self.p) - self.n*self.p
            noisy_distances.append(true_distance + noise)

        return noisy_distances

    def _record_metrics(self, belief_states, state):
        """Append metrics for each active ghost to self.metrics.

        Each record contains step, ghost index, entropy in bits, expected
        Manhattan error against the true position, and true-cell mass.
        Ground truth is used only here, never for the filtering update.
        These in-memory records can be exported by an experiment runner.
        """
        if not hasattr(self, "metrics"):
            self.metrics = []
            self.metric_step = 0
        for index, belief in enumerate(belief_states):
            if belief.sum() <= 0:
                continue
            positive = belief[belief > 0]
            entropy = -np.sum(positive * np.log2(positive))
            gx, gy = state.getGhostPosition(index + 1)
            x, y = np.indices(belief.shape)
            error = np.sum(belief * (abs(x - gx) + abs(y - gy)))
            self.metrics.append({
                "step": self.metric_step,
                "ghost": index + 1,
                "entropy_bits": float(entropy),
                "expected_error": float(error),
                "true_cell_probability": float(belief[int(gx), int(gy)]),
            })
        self.metric_step += 1

    def get_action(self, state):
        """
        Given a pacman game state, returns a belief state.

        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.

        Return:
        -------
        - A belief state.
        """

        """
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()

        evidence = self._get_evidence(state)
        newBeliefStates = self.update_belief_state(evidence,
                                                   state.getPacmanPosition(),
                                                   state.data._eaten[1:])
        self._record_metrics(self.beliefGhostStates, state)

        return newBeliefStates, evidence
