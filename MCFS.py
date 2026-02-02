import numpy as np
from math import log as ln

class Node:

    def __init__(self, parent, action):
        # tree structure
        self.parent = parent
        self.children = {}
        # incoming action
        self.action = action
        # MCTS stats
        self.w = 0
        self.n = 0

    """
    Select a child node based on the stats
    Args:
        legal_actions: a list of moves the player can make
        iteration_count: the current iteration count
    Return:
        a pair (whether this node expanded, the selected child node)
    """
    def select(self, legal_actions, iteration_count):
        # Q-values (average return)
        q_values = np.zeros(len(legal_actions))
        # for each legal action
        for i, action in enumerate(legal_actions):
            try:
                # calculate Q-values using stats of the child node for that action
                child = self.children[action]
                q_values[i] = child.w/child.n
            except KeyError:
                # action has no corresponding child node yet; create one
                return (True, self.expand(action))
        # pi is a distribution of actions based on the Q-values
        raised = np.exp(q_values*ln(iteration_count))
        pi = raised/np.sum(raised)
        # sample an action from pi
        return (False, self.children[np.random.choice(legal_actions, p=pi)])

    """
    Expand the node (add a new child)
    Args:
        action: the action the new child stands for
    Return:
        the created child node
    """
    def expand(self, action):
        child = Node(self, action)
        self.children[action] = child
        return child

    """
    Backpropagation: update tree stats
    Args:
        reward: the reward received
    """
    def backup(self, reward):
        curr = self
        while curr is not None:
            curr.w += reward
            curr = curr.parent

class MonteCarloForest:

    # stats recording is only available for single stage games (or turn one for extensive form games)
    def __init__(self, game, recording=False):
        self.game = game
        self.recording = recording
        if recording:
            self.W = {}
            self.N = {}
            self.agents = game.get_ids()
            self.legal_actions = game.get_legal_actions()
            for agent_id, actions in zip(self.agents, self.legal_actions):
                self.W[agent_id] = {}
                self.N[agent_id] = {}
                for action in actions:
                    self.W[agent_id][action] = []
                    self.N[agent_id][action] = []
        self.roots = {}
        for agent_id in game.get_ids():
            self.roots[agent_id] = Node(None, None)

    """
    Monte Carlo Forest Search for many iterations
    Args:
        iteration: the total number of MCFS iterations to run
    Return:
        the recommended action
    """
    def search(self, iteration):
        active_agents = self.game.get_ids()
        # for each iteration
        for t in range(1, iteration + 1):
            # make a copy of the game to run the simulation
            game_copy = self.game.copy()
            # set the current node of each agent
            current = {agent_id: self.roots[agent_id] for agent_id in active_agents}
            # run the game until a new node is created
            game_running = True
            no_one_expanded = True
            while game_running and no_one_expanded:
                copy_active_agents = game_copy.get_ids()
                actions = [None]*len(copy_active_agents)
                legal_actions = game_copy.get_legal_actions()
                # for each agent
                for i, agent_id in enumerate(copy_active_agents):
                    # select the action to explore
                    is_expanded, node = current[agent_id].select(legal_actions[i], t)
                    actions[i] = node.action
                    # update the agent's current position in its tree
                    current[agent_id] = node
                    node.n += 1
                    if is_expanded:
                        no_one_expanded = False
                # tic the game forward using the actions of each agent
                game_running, rewards = game_copy.step(actions)
                # add intermediate reward to the stats
                for agent_id in active_agents:
                    current[agent_id].backup(rewards[agent_id])
            # evaluate the current game state for backpropagation
            if game_running:
                Q_values = self.evaluate(game_copy)
                for agent_id in active_agents:
                    current[agent_id].backup(Q_values[agent_id])
            # record stats for the iteration
            if self.recording and ("game_length" not in self.game.__dict__ or self.game.game_length < 1):
                for agent_id, actions in zip(self.agents, self.legal_actions):
                    root = self.roots[agent_id]
                    for action in actions:
                        try:
                            self.W[agent_id][action].append(root.children[action].w)
                            self.N[agent_id][action].append(root.children[action].n)
                        except KeyError:
                            # root.children[action] not created yet
                            self.W[agent_id][action].append(0)
                            self.N[agent_id][action].append(0)
        # choose an action after all search iterations are done
        best_actions = [None]*len(active_agents)
        best_values = [float("-inf")]*len(active_agents)
        legal_actions = self.game.get_legal_actions()
        for i, agent_id in enumerate(active_agents):
            root = self.roots[agent_id]
##            print("Agent", agent_id, end=" values: ")
            for action in legal_actions[i]:
                child = root.children[action]
                value = child.w/child.n
                if value > best_values[i]:
                    best_actions[i] = action
                    best_values[i] = value
##                print(round(value, 3), ':', child.n, sep='', end=' ')
##            print()
            # inherit the tree for next turn
            self.roots[agent_id] = self.roots[agent_id].children[best_actions[i]]
            self.roots[agent_id].parent = None
##        print("----------------------------------------------")
        return best_actions

    """
    Evaluate the current game state: can be a rollout or a neural network
    Args:
        game: the game to be evaluated
    Return:
        the estimated reward of the game
    """
    def evaluate(self, game):
        total_rewards = np.array([0.0 for agent in game.get_ids()])
        game_running = True
        while game_running:
            actions = [np.random.choice(legal) for legal in game.get_legal_actions()]
            game_running, rewards = game.step(actions)
            total_rewards += np.array(rewards)
        return total_rewards
