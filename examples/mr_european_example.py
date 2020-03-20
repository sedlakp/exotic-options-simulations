
import pathlib, sys
# make sure to have access to the path where simulations folder is
sys.path.append(str(pathlib.Path(__file__).parent.absolute()).replace("/examples",""))

import numpy as np
from simulations.first_simulation import mean_reverting_european
import matplotlib.pyplot as plt

# test

# select seed to generate pseudorandom numbers, allows comparison
np.random.seed(30)

k, paths, time_steps = mean_reverting_european(
    42,
    40,
    positionFlag="c",
    time_to_maturity=1,
    steps=250,
    simulations=100,
    kappa=0.0001,
    theta=45,
    v=2,
    r=0.1)


print("Simulated option price: ",k)

for path in paths:
    plt.plot(time_steps, path)
plt.show()
