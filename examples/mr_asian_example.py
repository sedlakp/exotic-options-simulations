import pathlib, sys
# make sure to have access to the path where simulations folder is
sys.path.append(str(pathlib.Path(__file__).parent.absolute()).replace("/examples",""))

import numpy as np
from simulations.asian_mean_reverting import mean_reverting_asian_fixed_strike
import matplotlib.pyplot as plt

np.random.seed(30)

k, paths, time_steps = mean_reverting_asian_fixed_strike(
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
