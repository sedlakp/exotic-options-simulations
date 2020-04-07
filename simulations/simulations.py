
import numpy as np
import scipy.stats as sps
from simulations.toolbox import owner_position

##
##
## Simulation functions
##
##


#
# GMB simulation of asian option, possibility of choosing different distribution than normal
#

def asian_simulation_gbm(*,position_flag,initial_price, strike, simulations, steps, loc, scale, strike_type="fixed", distribution="n"):
    """
        Returns total payoff from all simulations and simulated paths
    """

    total = 0.0
    paths = []

    position = owner_position(position_flag)

    sim_range = range(1,simulations+1)
    step_range = range(1,steps+1)

    for _ in sim_range:
        path = [initial_price]
        st = initial_price
        for _ in step_range:

            if distribution == "n":
                ds = st * (loc + scale * sps.norm.rvs(loc=0,scale=1))
            elif distribution == "c":
                ds = st * (loc + scale * sps.cauchy.rvs(loc=0,scale=1))
            elif distribution == "l":
                ds = st * (loc + scale * sps.laplace.rvs(loc=0,scale=1))
            else:
                raise ValueError("Distribution parameter must be: 'n'(normal - default) or 'c'(cauchy) or 'l'(laplace) ")
            st = st + ds
            path.append(st)
        avg_spot = np.average(path)
        # option payoff calculation
        if strike_type == "fixed":
            payoff = max(position * (avg_spot-strike),0)
        elif strike_type == "floating":
            payoff = max(position * (st-avg_spot),0)
        else:
            raise Exception("Strike type can be either 'fixed' or 'floating'")
        total = total + payoff
        paths.append(path)
    return total, paths


#
# Simulation of spread option (e.g. calendar spread option)
# GBM model is used
#
# Distributions for both assests are assumed to be the same
#

def spread_simulation_gbm(*,position_flag,initial_price1, initial_price2, strike, simulations, steps, loc1, loc2, scale1, scale2, cor, distribution="n"):
    """
        Returns total payoff from all simulations and simulated paths
    """

    total = 0.0
    paths1 = []
    paths2 = []

    sim_range = range(1,simulations+1)
    step_range = range(1,steps+1)

    for _ in sim_range:
        path1 = [initial_price1]
        path2 = [initial_price2]
        st1 = initial_price1
        st2 = initial_price2
        for _ in step_range:

            if distribution == "n":
                noise1 = sps.norm.rvs(loc=0, scale=1)
            elif distribution == "c":
                noise1 = sps.norm.rvs(loc=0, scale=1)
            elif distribution == "l":
                noise1 = sps.norm.rvs(loc=0, scale=1)
            else:
                raise ValueError("Distribution parameter must be: 'n'(normal - default) or 'c'(cauchy) or 'l'(laplace) ")

            ds1 = st1 * (loc1 + scale1 * noise1)
            st1 = st1 + ds1
            path1.append(st1)

            if distribution == "n":
                noise2 = ( cor * noise1 ) + ( sps.norm.rvs(loc=0,scale=1) * np.sqrt(1-cor**2) )
            elif distribution == "c":
                noise2 = ( cor * noise1 ) + ( sps.cauchy.rvs(loc=0,scale=1) * np.sqrt(1-cor**2) )
            elif distribution == "l":
                noise2 = ( cor * noise1 ) + ( sps.laplace.rvs(loc=0,scale=1) * np.sqrt(1-cor**2) )
            else:
                raise ValueError("Distribution parameter must be: 'n'(normal - default) or 'c'(cauchy) or 'l'(laplace) ")

            ds2 = st2 * (loc2 + scale2 * noise2)
            st2 = st2 + ds2
            path2.append(st2)

        # option payoff calculation
        # https://www.cmegroup.com/content/dam/cmegroup/rulebook/NYMEX/3/397.pdf
        if position_flag == "c":
            payoff = max(((st1-st2) - strike), 0)
        elif position_flag == "p":
            payoff = max((strike - (st1-st2)), 0)
        else:
            raise ValueException("Position can be either 'p' for put or 'c' for call")

        total = total + payoff
        paths1.append(path1)
        paths2.append(path2)
    return total, [paths1,paths2]
