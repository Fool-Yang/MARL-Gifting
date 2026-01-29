from MCFS import *
from games import free_money
from time import time
from parameters import *

record_file = "record_free_money.stats"
f = open(record_file, 'w')
f.close()
t0 = time()
for i in range(experiments):
    g = free_money.Game()
    mcf = MonteCarloForest(g, recording=True)
    game_running = True
    while game_running:
        actions = mcf.search(iterations)
        game_running, rewards = g.tic(actions)
    f = open(record_file, 'a')
    f.write(str(mcf.W) + '\n')
    f.write(str(mcf.N) + '\n\n')
    f.close()
print("Game Ended. Total time:", time() - t0)
