import games
from MCFS import *
from time import time

experiments = 50
# iterations must be >= the number of actions on turn one or the stats won't work
# because you need at least one sample of each action to get the stats
iterations = 1000

# list of game classes to create game objects
Games = [
##    games.BiasedRPS,
##    games.FreeMoney,
##    games.PeerRewardingWrapper(games.FreeMoney),
##    games.BeKind,
##    games.PeerRewardingWrapper(games.BeKind),
##    games.Prisoners,
##    games.PeerRewardingWrapper(games.Prisoners),
##    games.StagHunt(2, 2),
##    games.PeerRewardingWrapper(games.StagHunt(2, 2)),
]

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
        f.write(str(mcf.Q) + '\n')
        f.write(str(mcf.P) + '\n\n')
        f.close()
    print("Game", g.name, "ended. Total time:", time() - t0)

# plot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

for game in Games:
    record_file = "record_" + game.name + ".stats"
    f = open(record_file, 'r')
    data = f.read().strip().split('\n\n')
    f.close()
    for agent_id in eval(data[0].split('\n')[0]):
        rows_Q = []
        rows_P = []
        for trial, game_run in enumerate(data):
            Q, P = map(eval, game_run.split('\n'))
            for action in Q[agent_id]:
                action_name = game.action_names[agent_id][action]
                for i in range(len(Q[agent_id][action])):
                    rows_Q.append({
                        "action": action_name,
                        "trial": trial,
                        "iteration": i,
                        "average reward": Q[agent_id][action][i]
                        })
                    rows_P.append({
                        "action": action_name,
                        "trial": trial,
                        "iteration": i,
                        "policy": P[agent_id][action][i]
                        })
        df_Q = pd.DataFrame(rows_Q)
        df_P = pd.DataFrame(rows_P)
        fig_reward, ax_reward = plt.subplots()
        sns.lineplot(data=df_Q, x="iteration", y="average reward", hue="action", errorbar="ci", n_boot=200)
        ax_reward.set_title(game.name + ": agent " + str(agent_id))
        fig_strategy, ax_strategy = plt.subplots()
        sns.lineplot(data=df_P, x="iteration", y="policy", hue="action", errorbar="ci", n_boot=200)
        ax_strategy.set_title(game.name + ": agent " + str(agent_id))
plt.show()

Games = []
##for n_players in range(2, 11):
##    for n_actions in range(2, 11):
##        Games.append(games.StagHunt(n_players, n_actions))
##        Games.append(games.PeerRewardingWrapper(games.StagHunt(n_players, n_actions)))

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
        f.write(str(mcf.Q) + '\n')
        f.write(str(mcf.P) + '\n\n')
        f.close()
    print("Game", g.name, "ended. Total time:", time() - t0)
