from .normal_form_game import NormalFormGame

def StagHunt(n_players, n_actions):

    class StagHuntConstructor(NormalFormGame):

        name = "stag_hunt_" + str(n_players) + "x" + str(n_actions)
        action_names = (("safe",) + tuple("risk-" + str(i) for i in range(1, n_actions + 1)),)*n_players

        def __init__(self, max_t=1):
            # self.reward_matrix = ()
            # super().__init__(max_t)
            # not using a matrix do define the reward function
            # as the dimensions explode due to O(m^n) space complexity
            self.players = tuple(range(n_players))
            self.legal_actions = (tuple(range(n_actions)),)*n_players
            self.reward_value = (0.25/n_actions,) + tuple(action_id/n_actions for action_id in range(1, n_actions + 1))
            self.max_t = max_t
            self.t = 0

        def get_legal_actions(self):
            return self.legal_actions

        def step(self, actions):
            rewards = [0]*len(self.players)
            bins = [set() for _ in self.legal_actions[0]]
            for player, action in zip(self.get_ids(), actions):
                bins[action].add(player)
            for player in bins[0]:
                rewards[player] = self.reward_value[0]
            for action_id in range(1, len(bins)):
                players = bins[action_id]
                n_players = len(players)
                if n_players > 0:
                    if n_players > 1:
                        reward = self.reward_value[action_id]/n_players
                        for player in players:
                            rewards[player] = reward
                    else:
                        rewards[players.pop()] = 0
            self.t += 1
            return self.t < self.max_t, rewards

    return StagHuntConstructor
