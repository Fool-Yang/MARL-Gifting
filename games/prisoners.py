class Game:

    def __init__(self):
        self.players = [0, 1]
        return

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
        # (cooperate, betray) = (0, 1)
        return [(0, 1) for player in self.players]

    """
    Move the game to the next turn
    Args:
        moves: a list of moves the players will make
    Return:
        whether the game is running and the rewards list
    """
    def tic(self, moves):
        rewards = [0, 0]
        if moves[0] == 0:
            if moves[1] == 0:
                rewards[0] = 2
                rewards[1] = 2
            else:
                rewards[0] = 0
                rewards[1] = 3
        else:
            if moves[1] == 0:
                rewards[0] = 3
                rewards[1] = 0
            else:
                rewards[0] = 1
                rewards[1] = 1
        return False, rewards

    """
    Copy the game
    Return:
        a deep copy of the game
    """
    def copy(self):
        return Game()
