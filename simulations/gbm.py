
import numpy as np

def owner_position(flag: str) -> int:
    if flag == "c":
        return 1
    elif flag == "p":
        return -1
    else:
        raise ValueError(f"Position can be either p or c, not {positionFlag}")

def asian_gbm_fixed(
            s,x,*,position_flag="c",
            time_to_maturity=1,
            steps,
            simulations,
            drift_strength, # has to be daily (calculated from daily changes)
            v, # assumed to be daily
            r):
    dt = time_to_maturity/steps
    position = owner_position(position_flag)

    sum = 0.0
    paths = []

    sim_range = range(1,simulations+1)
    step_range = range(1,steps+1)

    for i in sim_range:
        path = [s]
        st = s
        for _ in step_range:
            #inputted standard deviation and drift strength are calculated from daily! evaluates
            # dt is for these then 1, so no adjustment isnt neccessary
            ds = st * (drift_strength + v * np.random.normal(0,1))
            st = st + ds
            path.append(st)
        avg_spot = np.average(path)
        # option payoff calculation
        payoff = max(position * (avg_spot-x),0)
        sum = sum + payoff
        paths.append(path)

    return (np.exp(-r*time_to_maturity)/simulations)*sum, paths, range(0,steps+1)

def asian_gbm_floating():
    pass


def spread_gbm():
    pass
