class Game:

    name = "game"

    def __init__(self, max_t=1):
        self.players = []
        self.t = 0
        self.max_t = max_t

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

    """
    Copy the game
    Return:
        a deep copy of the game
    """
    def copy(self):
        game_copy = Game(max_t=self.max_t)
        game_copy.t = self.t
        return game_copy
