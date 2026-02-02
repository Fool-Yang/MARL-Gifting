from .game import Game

class StagHunt(Game):

    name = "stag_hunt"

    def __init__(self, max_t=1):
        self.players = [0, 1]
        self.t = 0
        self.max_t = max_t
        self.reward_matrix = (
            ((1, 1), (0.1, 0.8)),
            ((0.8, 0.1), (0.5, 0.5))
        )

    """
    Get legal actions for each player
    Return:
        lists of actions for each player
    """
    def get_legal_actions(self):
        # (stag, hare)
        return [(0, 1) for player in self.players]

    """
    Move the game to the next turn
    Args:
        actions: a list of actions the players will make
    Return:
        whether the game is running and the rewards list
    """
    def step(self, actions):
        rewards = self.reward_matrix[actions[0]][actions[1]]
        self.t += 1
        return self.t < self.max_t, rewards

    """
    Copy the game
    Return:
        a deep copy of the game
    """
    def copy(self):
        game_copy = StagHunt(max_t=self.max_t)
        game_copy.t = self.t
        return StagHunt()
