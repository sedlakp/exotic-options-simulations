import pathlib, sys
# make sure to have access to the path where simulations folder is
# this does not work for jupyter notebook, so the notebooks have to be on top level in the repo
sys.path.append(str(pathlib.Path(__file__).parent.absolute()).replace("/examples",""))

from simulations.spreads import mean_reverting_calendar_spread
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(25)

k, paths1, paths2, time_steps = mean_reverting_calendar_spread(
                                    42,
                                    41,
                                    0.5,
                                    position_flag="c",
                                    time_to_maturity=1,
                                    steps=10,
                                    simulations=1,
                                    kappa1=0.0001,
                                    kappa2=0.0001,
                                    theta1 = 45,
                                    theta2 = 45,
                                    v1 = 2,
                                    v2 = 2,
                                    r = 0.1,
                                    rho = 0.5)


print("Simulated option price: ",k)

for path1, path2 in list(zip(paths1, paths2)):
    plt.plot(time_steps, path1, ls="--")
    plt.plot(time_steps, path2)
plt.show()
