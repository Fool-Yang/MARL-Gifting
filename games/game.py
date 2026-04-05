class Game:

    name = "game"
    action_names = tuple()

    def __init__(self, max_t=1):
        self.players = []
        self.max_t = max_t
        self.t = 0

    """
    Get game and player ids
    Return:
        a list of player's id
    """
    def get_ids(self):
        return self.players

    """
    Get legal actions for each player
    Return:
        lists of actions for each player
    """
    def get_legal_actions(self):
        return [[] for player in self.players]

    """
    Move the game to the next turn
    Args:
        actions: a list of actions the players will make
    Return:
        whether the game is running and the rewards list
    """
    def step(self, actions):
        rewards = [0, 0]
        self.t += 1
        return self.t < self.max_t, rewards
