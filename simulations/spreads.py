
import math
import numpy as np

def owner_position(flag: str) -> int:
    if flag == "c":
        return 1
    elif flag == "p":
        return -1
    else:
        raise ValueError(f"Position can be either p or c, not {positionFlag}")

def mean_reverting_calendar_spread(
                        s1,
                        s2,
                        x,
                        *,
                        position_flag="c",
                        time_to_maturity=1,
                        steps=10,
                        simulations=100,
                        kappa1,
                        kappa2,
                        theta1,
                        theta2,
                        v1,
                        v2,
                        r,
                        rho):

    dt = time_to_maturity/steps
    position = owner_position(position_flag)

    payoff_sum = 0.0
    paths1 = []
    paths2 = []

    for i in range(1,simulations+1):
        path1 = []
        path2 = []
        st1 = s1
        st2 = s2

        for _ in range(1,steps+1):
            # discrete model
            stoch1 = np.random.normal(0,1)
            stoch2 = (rho * stoch1) + np.random.normal(0,1) * math.sqrt(1-(rho**2))

            ds1 = kappa1 * (theta1-st1) * dt + v1 * math.sqrt(dt) * stoch1
            ds2 = kappa2 * (theta2-st2) * dt + v2 * math.sqrt(dt) * stoch2

            st1 = st1 + ds1
            st2 = st2 + ds2

            path1.append(st1)
            path2.append(st2)
        # payoff
        # this option is not path dependent, only prices at expiration matter
        spread = st1 - st2
        payoff = max(0,position * (spread - x))
        payoff_sum = payoff_sum + payoff
        paths1.append(path1)
        paths2.append(path2)

        #return simulated dataframe instead of three variables, date can be as another column if applicable as well
    return (math.exp(-r*time_to_maturity)/simulations)*payoff_sum, paths1, paths2, range(1,steps+1)
