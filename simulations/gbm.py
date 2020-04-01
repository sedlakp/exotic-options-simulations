
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



def asian_gbm_laplace(
                    data,
                    *,
                    strike,
                    position_flag="c",
                    maturity=1,
                    steps,
                    simulations,
                    discount_rate,
                    history_length=None,
                    strike_type="fixed"
                    ):
    """
    Model is based on GBM process

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

    strike_type - fixed or floating, when floating is chosen, strike parameter will not be used

    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("The input should be timeseries in pandas DataFrame")

    if strike_type == "floating":
        print("Inputted strike will not be used, floating strike is calculated form average price values")
    # Fix data to follow business day frequency, businessdays that do not have any entry (in case e.g. holidays) are filled with its preceding value
    data = data.squeeze()
    data = data.asfreq(BDay())
    data = data.fillna(method='ffill')

    initial_price = data[-1]

    if history_length == None:
        history_data = data
    else:
        history_data = data[-history_length:]

    # fit returns to a laplace distribution
    rets = (history_data/history_data.shift(1))
    rets = rets.dropna()
    lrets = np.log(rets)
    loc_d, scale_d = sps.laplace.fit(lrets)
    print(loc_d, "////",scale_d)

    position = owner_position(position_flag)

    sum = 0.0
    paths = []

    sim_range = range(1,simulations+1)
    step_range = range(1,steps+1)

    for _ in sim_range:
        path = [initial_price]
        st = initial_price
        for _ in step_range:
            # GMB model with laplace distribution
            ds = st * (loc_d + sps.laplace.rvs(loc=0,scale=scale_d))
            st = st + ds
            path.append(st)
        avg_spot = np.average(path)
        # option payoff calculation
        if strike_type == "fixed":
            payoff = max(position * (avg_spot-strike),0)
        elif strike_type == "floating":
            payoff = max(position * (st-avg_spot),0)
        else:
            raise Exception("Strike type can be either fixed or floating")
        sum = sum + payoff
        paths.append(path)

    return (np.exp(-discount_rate*maturity)/simulations)*sum, paths, range(0,steps+1)
