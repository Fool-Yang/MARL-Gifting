import games
from MCFS import *
from time import time
from parameters import *

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
