import games
from MCFS import *
from time import time

experiments = 1
iterations = 2000

# list of game classes to create game objects
Games = (
    games.FreeMoney,
    games.Prisoners,
    games.StagHunt
)

for game in Games:
    record_file = "record_" + game.name + ".stats"
    f = open(record_file, 'w')
    f.close()
    t0 = time()
    for i in range(experiments):
        g = game()
        mcf = MonteCarloForest(g, recording=True)
        game_running = True
        while game_running:
            actions = mcf.search(iterations)
            game_running, rewards = g.step(actions)
        f = open(record_file, 'a')
        f.write(str(mcf.W) + '\n')
        f.write(str(mcf.N) + '\n\n')
        f.close()
    print("Game", g.name, "ended. Total time:", time() - t0)

# plot
import numpy as np
import matplotlib.pyplot as plt

for game in Games:
    record_file = "record_" + game.name + ".stats"
    f = open(record_file, 'r')
    data = f.read().strip().split('\n\n')
    f.close()
    format_example = data[0].split('\n')
    total_estimated_rewards = eval(format_example[0])
    total_empirical_distributions = eval(format_example[1])
    # clear data
    for agent_id in total_estimated_rewards:
        for action in total_estimated_rewards[agent_id]:
            total_estimated_rewards[agent_id][action] = np.zeros(len(total_estimated_rewards[agent_id][action]))
            total_empirical_distributions[agent_id][action] = np.zeros(len(total_empirical_distributions[agent_id][action]))
    for game_run in data:
        W, N = map(eval, game_run.split('\n'))
        for agent_id in W:
            for action in W[agent_id]:
                total_rewards = np.array(W[agent_id][action])
                count = np.array(N[agent_id][action])
                total_estimated_rewards[agent_id][action] += total_rewards/count
                total_empirical_distributions[agent_id][action] += count/np.array(range(1, len(count) + 1))
    # take average
    for agent_id in total_estimated_rewards:
        for action in total_estimated_rewards[agent_id]:
            total_estimated_rewards[agent_id][action] /= len(data)
            total_empirical_distributions[agent_id][action] /= len(data)
    # plot
    for agent_id in total_estimated_rewards:
        # reward
        fig_reward, ax_reward = plt.subplots()
        ax_reward.set_xlabel("iteration")
        ax_reward.set_ylabel("average reward")
        ax_reward.set_title(game.name + ": agent " + str(agent_id))
        # strategy
        fig_strategy, ax_strategy = plt.subplots()
        ax_strategy.set_xlabel("iteration")
        ax_strategy.set_ylabel("empirical distribution")
        ax_strategy.set_title(game.name + ": agent " + str(agent_id))
        for action in total_estimated_rewards[agent_id]:
            ax_reward.plot(total_estimated_rewards[agent_id][action], label = game.action_names[agent_id][action])
            ax_reward.legend(loc='best')
            ax_strategy.plot(total_empirical_distributions[agent_id][action], label = game.action_names[agent_id][action])
            ax_strategy.legend(loc='best')
plt.show()
