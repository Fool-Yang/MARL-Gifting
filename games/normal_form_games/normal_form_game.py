from ..game import Game

class NormalFormGame(Game):

    def __init__(self):
        dim = self._dim(self.reward_matrix)
        self.players = tuple(range(dim[-1]))
        self.legal_actions = tuple(tuple(range(dim[i])) for i in range(len(dim) - 1))
        self.t = 0

    """
    Auxiliary method to calculate the dimensions of a list.
    This is used to define the action spaces of players.
    """
    def _dim(self, reward_matrix):
        tp = type(reward_matrix)
        if tp == tuple or tp == list:
            return [len(reward_matrix)] + self._dim(reward_matrix[0])
        return []

    def get_legal_actions(self):
        return self.legal_actions

    def step(self, actions):
        rewards = self.reward_matrix[actions[0]][actions[1]]
        self.t += 1
        return self.t < self.max_t, rewards
