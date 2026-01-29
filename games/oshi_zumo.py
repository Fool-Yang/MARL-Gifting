class Game:

    def __init__(self, length, coins, truce=False, show=False):
        self.players = [0, 1]
        self.state = [coins, coins, 0, length]
        self.truce = truce
        self.show = show
        if show:
            self.replay_file = "replay_zumo.rep"
            f = open(self.replay_file, 'w')
            f.close()
        self.game_length = 0

    """
    Get visible state information for all players
    Return:
        a list of visible state information for each player
    """
    def get_states(self):
        mirror_state = [0]*4
        mirror_state[0] = self.state[1]
        mirror_state[1] = self.state[0]
        mirror_state[2] = -self.state[2]
        mirror_state[3] = self.state[3]
        return [self.state, mirror_state]

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
        # number of coins to bid
        if self.truce:
            return [tuple((i for i in range(self.state[player] + 1))) for player in self.players]
        else:
            return [tuple((i for i in range(1, self.state[player] + 1))) for player in self.players]

    """
    Move the game to the next turn
    Args:
        moves: a list of moves the players will make
        show: weather to draw the game board in "replay.rep"
    Return:
        whether the game is running and the rewards list
    """
    def tic(self, moves):
        if self.show:
            self.draw()
        self.game_length += 1
        rewards = [0, 0]
        # consume coins
        self.state[0] -= moves[0]
        self.state[1] -= moves[1]
        # return rewards if the game ends
        if moves[0] > moves[1]:
            self.state[2] += 1
            if self.state[2] > self.state[3]:
                rewards[0] = 1
                rewards[1] = -1
                if self.show:
                    self.draw()
                return False, rewards
        elif moves[1] > moves[0]:
            self.state[2] -= 1
            if self.state[2] < -self.state[3]:
                rewards[0] = -1
                rewards[1] = 1
                if self.show:
                    self.draw()
                return False, rewards
        elif moves[0] == 0: # and moves[1] == 0
            if self.state[2] > 0:
                rewards[0] = 1
                rewards[1] = -1
                if self.show:
                    self.draw()
                return False, rewards
            elif self.state[2] < 0:
                rewards[0] = -1
                rewards[1] = 1
                if self.show:
                    self.draw()
                return False, rewards
            else:
                if self.show:
                    self.draw()
                return False, rewards
        if self.state[0] == 0 or self.state[1] == 0:
            self.state[2] += self.state[0]
            self.state[2] -= self.state[1]
            if self.state[2] > 0:
                rewards[0] = 1
                rewards[1] = -1
                if self.show:
                    self.draw()
                return False, rewards
            elif self.state[2] < 0:
                rewards[0] = -1
                rewards[1] = 1
                if self.show:
                    self.draw()
                return False, rewards
            else:
                if self.show:
                    self.draw()
                return False, rewards
        # return None if the game continues
        return True, rewards

    """
    Copy the game
    Args:
        subgame_id: the game id of the created copy
    Return:
        a deep copy of the game
    """
    def copy(self):
        # subgames don't spawn food
        game = Game(self.state[3], 0, self.truce)
        game.state[0] = self.state[0]
        game.state[1] = self.state[1]
        game.state[2] = self.state[2]
        game.game_length = self.game_length
        return game

    """
    Draw the game board in "replay.osrep"
    """
    def draw(self):
        board = ['_']*(2*self.state[3] + 1)
        board[len(board)//2 + self.state[2]] = '%'

        f = open(self.replay_file, 'a')
        f.write(str(self.state[:2]) + '\n')
        f.write(str(board) + '\n')
        f.write('\n')
        f.close()
