
import numpy as np
import pandas as pd
import scipy.stats as sps
from pandas.tseries.offsets import BDay
from simulations.simulations import asian_simulation_gbm, spread_simulation_gbm
from simulations.toolbox import prepare_data, change_to_logrets

##
##
## This file contains functions that return option price.
##
##

##
## asian option fixed strike
## Model: GBM
## Distribution: Normal
##

def asian_gbm_fixed(
                    *,
                    initial_price,
                    strike,
                    position_flag="c",
                    maturity=1,
                    steps,
                    simulations,
                    discount_rate,
                    drift_strength,
                    sigma
                    ):
    """
    Standard asian option fixed strike

    """

    params = pd.DataFrame(
                        {"Params":[initial_price,0, strike, 0, maturity, steps, 0, discount_rate * 100, (sigma * np.sqrt(252) * 100)]},
                        index=["S","SA","X","t","Maturity","n","m","r","sigma"]
                        )

    total, paths = asian_simulation_gbm(position_flag=position_flag,
                                    initial_price=initial_price,
                                    strike=strike,
                                    simulations=simulations,
                                    steps=steps,
                                    loc=drift_strength,
                                    scale=sigma,
                                    distribution="l")

    return (np.exp(-discount_rate*maturity)/simulations)*total, paths, range(0,steps+1), params



##
##
## Simulate option price of asian option
## Model: GBM
## Used distribution: Laplace
##

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

    params = pd.DataFrame(
                        {"Params":[initial_price,0, strike, 0, maturity, steps, 0, discount_rate * 100, (sigma * np.sqrt(252) * 100)]},
                        index=["S","SA","X","t","Maturity","n","m","r","sigma"]
                        )

    total, paths = asian_simulation_gbm(position_flag=position_flag,
                                    initial_price=initial_price,
                                    strike=strike,
                                    simulations=simulations,
                                    steps=steps,
                                    loc=loc_d,
                                    scale=scale_d,
                                    strike_type=strike_type,
                                    distribution="l")

    return (np.exp(-discount_rate*maturity)/simulations)*total, paths, range(0,steps+1), params


##
## Simulate option price of calendar spread option
## Model: GBM
## Used distribution: Laplace
##

def calendar_spread_gbm(
            data,*,
            strike,
            position_flag,
            maturity=1,
            steps,
            simulations,
            discount_rate,
            history_length=None,
            ):
    """
    Function to simulate paths and calculate option price of a calendar spread option

    The distribution used is normal

    data should be a dataframe with two columns that contain historical data
    """

    data1 = prepare_data(data)

    initial_price1 = data1.iloc[-1,0]
    initial_price2 = data1.iloc[-1,1]

    if history_length == None:
        history_data1 = data1
    else:
        history_data1 = data1[-history_length:]

    lrets = change_to_logrets(history_data1)
    # fit normal distribution, scale is std
    # also, the scale is daily std!
    loc_d1, scale_d1 = sps.norm.fit(lrets[lrets.columns[0]])
    print("loc and std (1st asset)", loc_d1, scale_d1)

    loc_d2, scale_d2 = sps.norm.fit(lrets[lrets.columns[1]])
    print("loc and std (2nd asset)", loc_d2, scale_d2)

    cor = np.corrcoef(lrets[lrets.columns[0]],lrets[lrets.columns[1]])[1,0]
    print(f"corr coef: {cor}")

    # Prepare parameters for formula
    # the daily standard deviations have to be tranfromed into yearly volatilities
    # (std multiplied by square root of 252, which is generally accepted average number of
    # business days in a year and finally multply by 100 to get percentage)
    # risk free rate is supposed to be in % as well
    params = pd.DataFrame(
                        {"Params":[initial_price1, initial_price2, strike, maturity, discount_rate * 100, scale_d1 * np.sqrt(252) * 100, scale_d2 * np.sqrt(252) * 100, cor]},
                        index=["S1","S2","X","Maturity","r","sigma1","sigma2","cor"]
                        )

    total, paths = spread_simulation_gbm(position_flag=position_flag,
                                     initial_price1=initial_price1,
                                     initial_price2=initial_price2,
                                     strike=strike,
                                     simulations=simulations,
                                     steps=steps,
                                     loc1=loc_d1,
                                     loc2=loc_d2,
                                     scale1=scale_d1,
                                     scale2=scale_d2,
                                     cor=cor
                                    )

    return (np.exp(-discount_rate*maturity)/simulations)*total, paths, range(0,steps+1), params
