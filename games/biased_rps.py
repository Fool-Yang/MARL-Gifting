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
        # (rock, paper, scissors) = (0, 1, 2)
        return [(0, 1, 2) for player in self.players]

    """
    Move the game to the next turn
    Args:
        moves: a list of moves the players will make
    Return:
        whether the game is running and the rewards list
    """
    def tic(self, moves):
        rewards = [0, 0]
        # if player 0 win
        if moves[0] == 0:
            if moves[1] == 0:
                rewards[0] = 50
                rewards[1] = 50
            elif moves[1] == 1:
                rewards[0] = 25
                rewards[1] = 75
            else: # moves[1] == 2
                rewards[0] = 100
                rewards[1] = 0
        # if player 1 win
        elif moves[0] == 1:
            if moves[1] == 0:
                rewards[0] = 75
                rewards[1] = 25
            elif moves[1] == 1:
                rewards[0] = 50
                rewards[1] = 50
            else: # moves[1] == 2
                rewards[0] = 45
                rewards[1] = 55
        # tie
        else: # moves[0] == 2
            if moves[1] == 0:
                rewards[0] = 0
                rewards[1] = 100
            elif moves[1] == 1:
                rewards[0] = 55
                rewards[1] = 45
            else: # moves[1] == 2
                rewards[0] = 50
                rewards[1] = 50
        return False, rewards

    """
    Copy the game
    Return:
        a deep copy of the game
    """
    def copy(self):
        return Game()
