import math
import numpy as np
import matplotlib.pyplot as plt

def mean_reverting(s,x,*,positionFlag="c",
                        time_to_maturity=1,
                        steps=10,
                        simulations=100,
                        kappa,
                        theta,
                        v,
                        r):
    """
        monte carlo of mean reversion written in python based on VBA code in
        the complete guide to option pricing formulas

        simulation of european put and call vanilla options

        plot with simulation paths is created as well
    """

    dt = time_to_maturity/steps
    position = 0
    if positionFlag == "c":
        position = 1
    elif positionFlag == "p":
        position = -1
    else:
        raise ValueError(f"Position can be either p or c, not {positionFlag}")

    sum=0.0

    paths = []

    for i in range(1,simulations):
        path = []
        st = s
        for _ in range(0,steps):
            # https://math.stackexchange.com/questions/345773/how-the-ornstein-uhlenbeck-process-can-be-considered-as-the-continuous-time-anal
            ds = kappa * (theta-st) * dt + v * math.sqrt(dt) * np.random.normal(0,1)
            st = st + ds
            path.append(st)
        sum = sum + max(position * (st - x),0)
        paths.append(path)

    return (math.exp(-r*time_to_maturity)/simulations)*sum, paths, range(0,steps)

k, paths, time_steps = mean_reverting(
    42,
    40,
    positionFlag="c",
    time_to_maturity=0.5,
    steps=50,
    simulations=100,
    kappa=0.0001,
    theta=45,
    v=0.2,
    r=0.1)


print(k)

for path in paths:
    plt.plot(time_steps, path)
plt.show()
