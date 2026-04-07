from .game import Game

# Decorate a game to include peer rewarding
def PeerRewardingWrapper(game_class):

    class WrappedGame(Game):

        name = game_class.name + "_peer_rewarding"
        action_names = game_class.action_names

        """
        division: this is the number of portions the reward is divided into
            to make discrete action for giving rewards, the rewards are divided into finite amount of pieces
            if we divide a reward into 10 portions, then {0, 1, ..., 10} represents giving 0%, 10%, ..., 100%
        """
        def __init__(self, division=10, *args, **kwargs):
            self.t = 0
            self.game = game_class(*args, **kwargs)
            self.still_running = True
            self.peer_rewarding_action_space = tuple(range(division + 1))
            self.portion_size = 1/division
            self.last_rewards = [0 for player in self.game.get_ids()]

        """
        Get game and player ids
        Return:
            a list of player's id
        """
        def get_ids(self):
            return self.game.get_ids()

        """
        Get legal actions for each player
        Return:
            lists of actions for each player
        """
        def get_legal_actions(self):
            if self.t%2:
                return [self.peer_rewarding_action_space for player in self.game.players]
            else:
                return self.game.get_legal_actions()

        """
        Move the game to the next turn
        Args:
            actions: a list of actions the players will make
        Return:
            whether the game is running and the rewards list
        """
        def step(self, actions):
            players = self.game.get_ids()
            rewards = [0 for player in players]
            if self.t%2:
                sharing_pool = 0
                for i in range(len(actions)):
                    give = actions[i]*self.portion_size*self.last_rewards[i]
                    receive = give/(len(players) - 1)
                    sharing_pool += receive
                    rewards[i] = self.last_rewards[i] - give - receive
                for i in range(len(rewards)):
                    rewards[i] += sharing_pool
                still_running = self.still_running
            else:
                self.still_running, rewards = self.game.step(actions)
                self.last_rewards = rewards
                still_running, rewards = True, [0 for player in players]
            self.t += 1
            return still_running, rewards
    return WrappedGame
