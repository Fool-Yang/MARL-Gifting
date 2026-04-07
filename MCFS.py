import numpy as np
from math import log as ln
from copy import deepcopy

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
        self.q = 0

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
                q_values[i] = child.q
            except KeyError:
                # action has no corresponding child node yet; create one
                return (True, self.expand(action))
        # pi is a distribution of actions based on the Q-values
        pi = self.get_pi(q_values, iteration_count)
        # sample an action from pi
        return (False, self.children[np.random.choice(legal_actions, p=pi)])

    """
    Compute the policy based on the Q-values
    Args:
        q_values: a list of the Q-values, one for each action
        iteration_count: the current MCFS iteration number
    Return:
        the policy pi
    """
    def get_pi(self, q_values, iteration_count):
        raised = np.exp(q_values*ln(iteration_count))
        pi = raised/np.sum(raised)
        return pi

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
            curr.q = curr.w/curr.n
            curr = curr.parent

class MonteCarloForest:

    # stats recording is only available for normal form games (or turn one for extensive form games)
    def __init__(self, game, recording=False):
        self.game = game
        self.roots = {agent_id: Node(None, None) for agent_id in game.get_ids()}
        # record stats
        self.recording = recording
        if recording:
            self.Q = {}
            self.P = {}
            self.agents = game.get_ids()
            self.legal_actions = game.get_legal_actions()
            for agent_id, actions in zip(self.agents, self.legal_actions):
                self.Q[agent_id] = {}
                self.P[agent_id] = {}
                for action in actions:
                    self.Q[agent_id][action] = []
                    self.P[agent_id][action] = []

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
            game_copy = deepcopy(self.game)
            # set the current node of each agent
            current = {}
            for agent_id in active_agents:
                current[agent_id] = self.roots[agent_id]
                current[agent_id].n += 1
            # run the game until the game ends or a new node is created
            game_running = True
            no_one_expanded = True
            while game_running and no_one_expanded:
                copy_active_agents = game_copy.get_ids()
                legal_actions = game_copy.get_legal_actions()
                actions = [None]*len(copy_active_agents)
                # for each agent
                for i, agent_id in enumerate(copy_active_agents):
                    # select an action to explore
                    expanded, node = current[agent_id].select(legal_actions[i], t)
                    actions[i] = node.action
                    # update the agent's current position in its tree
                    current[agent_id] = node
                    node.n += 1
                    if expanded:
                        no_one_expanded = False
                # tic the game forward using the actions of each agent
                game_running, rewards = game_copy.step(actions)
                # add intermediate reward to the stats
                for agent_id in active_agents:
                    current[agent_id].backup(rewards[agent_id])
            # evaluate the current game state for backpropagation
            if game_running:
                q_values = self.evaluate(game_copy)
                for agent_id in active_agents:
                    current[agent_id].backup(q_values[agent_id])
            # record stats for the iteration
            if self.recording and self.game.t < 1:
                for agent_id, actions in zip(self.agents, self.legal_actions):
                    root = self.roots[agent_id]
                    q_values = np.zeros(len(actions))
                    empirical_distribution = [0]*len(actions)
                    # for each legal action
                    for i, action in enumerate(actions):
                        try:
                            # calculate Q-values using stats of the child node for that action
                            child = root.children[action]
                            q_values[i] = child.q
                            empirical_distribution[i] = root.children[action].n/root.n
                        except KeyError:
                            # action has no corresponding child node yet
                            q_values[i] = 0
                            empirical_distribution[i] = 0
                    for i, action in enumerate(actions):
                        self.Q[agent_id][action].append(q_values[i])
                        self.P[agent_id][action].append(empirical_distribution[i])
        # choose an action after all search iterations are done
        best_actions = [None]*len(active_agents)
        legal_actions = self.game.get_legal_actions()
        for i, agent_id in enumerate(active_agents):
            actions = legal_actions[agent_id]
            root = self.roots[agent_id]
            pi = np.zeros(len(actions))
            # for each legal action
            for j, action in enumerate(actions):
                try:
                    # calculate Q-values using stats of the child node for that action
                    child = root.children[action]
                    # do not do pi[j] = child.n/root.n
                    # because from the second level of the tree, root.n = sum([child.n]) + 1
                    # 1 extra n when the root has no children yet
                    pi[j] = child.n
                except KeyError:
                    # action has no corresponding child node yet
                    pi[j] = 0
            pi = pi/sum(pi)
            best_actions[i] = np.random.choice(actions, p=pi)
            # inherit the tree for next turn
            self.roots[agent_id] = self.roots[agent_id].children[best_actions[i]]
            self.roots[agent_id].parent = None
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
