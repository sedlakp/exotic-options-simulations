
import math
import numpy as np

def mean_reverting_asian_fixed_strike(s,x,*,positionFlag="c",
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

        simulation of asian fixed strike put and call options

        plot with simulation paths is created as well

        s - initial(current) price
        x - strike
        kappa - mean reversion strength
        theta - long term average price to which the price reverts to
        v - volatility
        r - discount rate
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
        avg_spot = np.average(path)
        # option payoff calculation
        payoff = max(position * (avg_spot-x),0)
        sum = sum + payoff
        paths.append(path)

    return (math.exp(-r*time_to_maturity)/simulations)*sum, paths, range(0,steps)


def mean_reverting_asian_floating_strike(s,x,*,positionFlag="c",
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

        simulation of asian floating strike put and call options

        plot with simulation paths is created as well

        s - initial(current) price
        x - strike
        kappa - mean reversion strength
        theta - long term average price to which the price reverts to
        v - volatility
        r - discount rate
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
        avg_spot = np.average(path)
        # option payoff calculation
        payoff = max(position * (st-avg_spot),0)
        sum = sum + payoff
        paths.append(path)

    return (math.exp(-r*time_to_maturity)/simulations)*sum, paths, range(0,steps)
