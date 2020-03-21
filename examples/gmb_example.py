
import pathlib, sys
# make sure to have access to the path where simulations folder is
# this does not work for jupyter notebook, so the notebooks have to be on top level in the repo
sys.path.append(str(pathlib.Path(__file__).parent.absolute()).replace("/examples",""))

from simulations.gbm import asian_gbm_fixed
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(30)

k, paths, steps = asian_gbm_fixed(
                            42,
                            40,
                            position_flag="c",
                            time_to_maturity=1,
                            steps=255,
                            simulations=100,
                            drift_strength=0,
                            v=0.2,
                            r=0.1
                        )


print("Simulated option price: ",k)

for path in paths:
    plt.plot(steps, path)
plt.show()
