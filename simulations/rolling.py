
from pandas.tseries.offsets import BDay
import pandas as pd
import numpy as np


def asian_custom_fixed_inefficient(data,*,strike,position_flag="c",maturity=1,steps,simulations, discount_rate,rolling=30):
    """
    Model is based on Geometrical Brownian Motion, both drift and shock are calculated from rolling historical data

    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("The input should be timeseries in pandas DataFrame")


    # better variance where mean is removed from the logreturns? or do I assume that the mean should always be ~0
    # lrets_mean_rm = selected_ti-rm
    # rs = flat_ti.rolling(roll).std()
    data = data.squeeze()
    data = data.asfreq(BDay())
    data = data.fillna(method='ffill')

    position = owner_position(position_flag)

    sum = 0.0
    paths = []

    sim_range = range(1,simulations+1)
    step_range = range(1,steps+1)

    initial_price = data[-1]

    for i in sim_range:
        path = [initial_price]
        st = initial_price
        _rolling_data = data[-(rolling+1):]
        for _ in step_range:
            #calculate drift and volatility for this step
            rets = (_rolling_data/_rolling_data.shift(1))
            rets = rets.dropna()
            lrets = np.log(rets)

            rolling_mean = lrets.rolling(rolling).mean()[-1]
            rolling_var = lrets.rolling(rolling).std()[-1]
            print(rolling_mean, rolling_var)

            #inputted standard deviation and drift strength are calculated from daily! evaluates
            # dt is for these then 1, so no adjustment isnt neccessary
            ds = st * (rolling_mean + rolling_var * np.random.normal(0,1))
            st = st + ds
            path.append(st)
            _rolling_data = _rolling_data.append(pd.Series(st, index=[_rolling_data.index[-1]+BDay()]))
        avg_spot = np.average(path)
        # option payoff calculation
        payoff = max(position * (avg_spot-strike),0)
        sum = sum + payoff
        paths.append(path)

    return (np.exp(-discount_rate*time_to_maturity)/simulations)*sum, paths, range(0,steps+1)



def asian_custom_mean_reverting(data,*,strike,position_flag="c",maturity=1,steps,simulations, discount_rate,rolling):
    """
    Model is based on O-U process, both drift and shock are calculated from rolling historical data

    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("The input should be timeseries in pandas DataFrame")

    # Fix data to follow business day frequency, businessdays that do not have any entry (in case e.g. holidays) are filled with its preceding value
    data = data.squeeze()
    data = data.asfreq(BDay())
    data = data.fillna(method='ffill')

    position = owner_position(position_flag)

    sum = 0.0
    paths = []

    sim_range = range(1,simulations+1)
    step_range = range(1,steps+1)

    initial_price = data[-1]

    for i in sim_range:
        path = [initial_price]
        st = initial_price
        _rolling_data = data.copy()
        #print(f"SImulation: {i}")
        for _ in step_range:
            #calculate drift and volatility for this step
            roll_mean = _rolling_data.rolling(roll).mean()[-1]
            _roll_data_mean_removed = _rolling_data - roll_mean
            roll_std = _roll_data_mean_removed.rolling(roll).std()[-1]
            #print(roll_mean, roll_std)
            reversion_rate = 0.01

            #inputted standard deviation and drift strength are calculated from daily! evaluates
            # dt is for these then 1, so no adjustment isnt neccessary
            #ds = st * (rolling_mean + rolling_var * np.random.normal(0,1))

            ds = reversion_rate * (roll_mean-st) + roll_std * laplace.rvs(loc=0,scale=0.1)#np.random.normal(0,1)

            st = st + ds
            path.append(st)
            _rolling_data = _rolling_data.append(pd.Series(st, index=[_rolling_data.index[-1]+BDay()]))
        avg_spot = np.average(path)
        # option payoff calculation
        payoff = max(position * (avg_spot-strike),0)
        sum = sum + payoff
        paths.append(path)

    return (np.exp(-discount_rate*time_to_maturity)/simulations)*sum, paths, range(0,steps+1)
