import numpy as np
import pandas as pd
import scipy.stats as sps
from pandas.tseries.offsets import BDay

def owner_position(flag: str) -> int:
    if flag == "c":
        return 1
    elif flag == "p":
        return -1
    else:
        raise ValueError(f"Position can be either p or c, not {positionFlag}")


def asian_custom_mean_reverting_laplace(data,*,strike,position_flag="c",maturity=1,steps,simulations, discount_rate,history_length=None,reversion_rate):
    """
    Model is based on OU process

    Error term is in this case drawn from laplace distribution that best fits the data

    Parameters:

    data - time series of data (format must be DataFrame)

    strike - strike of the average option

    flag - c for call, p for put

    maturity - time remaining to maturity in years

    steps - number of steps into the future

    simulations - number of simulated paths

    discount_rate - discount rate

    history_length - past x steps of the inputted data to be used in calculation of parameters
        - if not specified, entire dataset is used

    reversion_rate - speed of mean reversion

    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("The input should be timeseries in pandas DataFrame")

    # Fix data to follow business day frequency, businessdays that do not have any entry (in case e.g. holidays) are filled with its preceding value
    data = data.squeeze()
    data = data.asfreq(BDay())
    data = data.fillna(method='ffill')

    initial_price = data[-1]

    if history_length == None:
        history_data = data
    else:
        history_data = data[-history_length:]

    mean_data = history_data.mean()
   # print(f"mean: {mean_data}")

    rets = (history_data/history_data.shift(1))
    rets = rets.dropna()
    lrets = np.log(rets)
    loc_d, scale_d = sps.laplace.fit(lrets)
    position = owner_position(position_flag)

    sum = 0.0
    paths = []

    sim_range = range(1,simulations+1)
    step_range = range(1,steps+1)

    for i in sim_range:
        path = [initial_price]
        st = initial_price
        for i in step_range:
            reversion_rate = reversion_rate
            ds = reversion_rate * (mean_data-st) + st * sps.laplace.rvs(loc=loc_d,scale=scale_d)
            st = st + ds
            path.append(st)
        avg_spot = np.average(path)
        # option payoff calculation
        payoff = max(position * (avg_spot-strike),0)
        sum = sum + payoff
        paths.append(path)

    return (np.exp(-discount_rate*maturity)/simulations)*sum, paths, range(0,steps+1)
