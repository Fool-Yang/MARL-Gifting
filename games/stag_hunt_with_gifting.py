class Game:

    def __init__(self):
        self.players = [0, 1]
        self.last_rewards = [0, 0]
        self.game_length = 0
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
        # (stag, hare) = (0, 1)
        if self.game_length == 0:
            return [(0, 1) for player in self.players]
        else:
            return [list(range(11)) for player in self.players]

    """
    Move the game to the next turn
    Args:
        moves: a list of moves the players will make
    Return:
        whether the game is running and the rewards list
    """
    def tic(self, moves):
        rewards = [0, 0]
        if self.game_length == 0:
            if moves[0] == 0:
                if moves[1] == 0:
                    rewards[0] = 1
                    rewards[1] = 1
                else:
                    rewards[0] = 0.1
                    rewards[1] = 0.8
            else:
                if moves[1] == 0:
                    rewards[0] = 0.8
                    rewards[1] = 0.1
                else:
                    rewards[0] = 0.5
                    rewards[1] = 0.5
        else:
            rewards[0] = moves[1]/10*self.last_rewards[1] - moves[0]/10*self.last_rewards[0]
            rewards[1] = -rewards[0]
        self.last_rewards = rewards
        self.game_length += 1
        return self.game_length < 2, rewards

    """
    Copy the game
    Return:
        a deep copy of the game
    """
    def copy(self):
        game = Game()
        game.last_rewards = self.last_rewards
        game.game_length = self.game_length
        return game
