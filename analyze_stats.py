import numpy as np
import matplotlib.pyplot as plt

inp = input("Enter game name {matching_pennies, prisoners, free_money, rps, biased_rps, stag_hunt, stag_hunt_with_gifting}:")
record_file = "record_" + inp + ".stats"
f = open(record_file, 'r')
data = f.read().strip().split('\n\n')
f.close()

if inp == "matching_pennies":
    action_name = ["heads", "tails"]
elif inp == "prisoners":
    action_name = ["coop", "betray"]
elif inp == "free_money":
    action_name = ["no", "yes"]
elif inp == "rps" or inp == "biased_rps":
    action_name = ["R", "P", "S"]
elif inp == "stag_hunt":
    action_name = ["stag", "hare"]
elif inp == "stag_hunt_with_gifting":
    action_name = ["stag", "hare"]

format_example = data[0].split('\n')
total_estimated_rewards = eval(format_example[0])
total_empirical_distributions = eval(format_example[1])
# clear data
for agent_id in total_estimated_rewards:
    for action in total_estimated_rewards[agent_id]:
        total_estimated_rewards[agent_id][action] = np.zeros(len(total_estimated_rewards[agent_id][action]))
        total_empirical_distributions[agent_id][action] = np.zeros(len(total_empirical_distributions[agent_id][action]))
for game in data:
    W, N = map(eval, game.split('\n'))
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
    ax_reward.set_title(inp + ": agent " + str(agent_id))
    # strategy
    fig_strategy, ax_strategy = plt.subplots()
    ax_strategy.set_xlabel("iteration")
    ax_strategy.set_ylabel("empirical distribution")
    ax_strategy.set_title(inp + ": agent " + str(agent_id))
    for action in total_estimated_rewards[agent_id]:
        ax_reward.plot(total_estimated_rewards[agent_id][action], label = action_name[action])
        ax_reward.legend(loc='best')
        ax_strategy.plot(total_empirical_distributions[agent_id][action], label = action_name[action])
        ax_strategy.legend(loc='best')
'''
for game in data:
    W, N = map(eval, game.split('\n'))
    for agent_id in W:
        # reward
        fig_reward, ax_reward = plt.subplots()
        ax_reward.set_xlabel("iteration")
        ax_reward.set_ylabel("estimated reward")
        ax_reward.set_title("agent: " + str(agent_id))
        # strategy
        fig_strategy, ax_strategy = plt.subplots()
        ax_strategy.set_xlabel("iteration")
        ax_strategy.set_ylabel("empirical distribution")
        ax_strategy.set_title("agent: " + str(agent_id))
        for action in W[agent_id]:
            total_rewards = np.array(W[agent_id][action])
            count = np.array(N[agent_id][action])
            estimated_rewards = total_rewards/count
            empirical_distributions = count/np.array(range(1, len(count) + 1))
            ax_reward.plot(estimated_rewards, label = "action: " + str(action))
            plt.legend(loc='best')
            ax_strategy.plot(empirical_distributions, label = "action: " + str(action))
            plt.legend(loc='best')
    break
'''
plt.show()
