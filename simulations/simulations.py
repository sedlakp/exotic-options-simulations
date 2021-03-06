
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

def asian_simulation_gbm_final(*,position_flag,initial_price, strike,
    simulations, steps, avg_steps , avg_values=[], group1, group2=(),
    border_price=np.inf, strike_type="fixed"):
    """
        Funkce vrátí celkový součet zisků ze všech simulací
        + všechny nasimulované cesty ve formě array
        + array všech cen jednotlivých simulací

        Parametry:
        * position_flag - "c" pro CALL, "p" pro PUT
        * initial_price - výchozí cena
        * strike
        * simulations - počet simulací
        * steps - počet kroků do expirace
        * avg_steps - počet korků v průměrovacím období
        * avg_values - už známé hodnoty průměrovacího období
        * group - vyžaduje tuple ve tvaru
                (loc,scale,distribution) nebo (loc,scale,df,distribution)
                Z určených rozdělení se generují hodnoty. Pokud je současná
                hodnota menší než border_price, používá se group1. V opačném
                případě se používá group2.

        * border_price - cenová mez rozdělující obě skupiny
        * strike_type - "floating" nebo "fixed"

        Funkci lze použít, i když se nepředpokládá změna parametrů pro
        generování hodnot při překročení cenové hranice (border_price).
        V takovém případě stačí poskytnout údaje pro group1 (border_price
        má výchozí hodnotu nekonečno, group2 se tedy nikdy nepoužije).
    """
    # výpočet počtu kroků, které nepatří do průměrovacího období
    non_avg_steps = steps - avg_steps
    # kontrola, jestli počet známých hodnot je stejný jako vypočítaná hodnota
    # pokud už je výchozí hodnota v průměrovacím období
    if non_avg_steps < 0:
        if -non_avg_steps != len(avg_values):
            raise ValueError(f"avg_values count ({len(avg_values)}) must be equal to {-non_avg_steps}")
    # inicializace proměnných pro výsledek simulace
    total = 0.0
    paths = []
    payoffs = []
    # funkce, která vrátí 1 pro "c" a -1 pro "p"
    position = owner_position(position_flag)

    # příprava počtu simulací pro for loop,
    # počet simulací a počet kroků každé simulace
    sim_range = range(1,simulations+1)
    step_range = range(1,steps+1)

    for _ in sim_range:
        # nastavení výchozí hodnoty
        path = [initial_price]
        st = initial_price
        for _ in step_range:
            # rozhodnutí o použití parametrů buď z první nebo druhé skupiny
            # podle porovnání současné hodnoty s hraniční hodnotou
            if st >= border_price:
                distribution = group2[-1]
                loc = group2[0]
                scale = group2[1]
                if distribution == "t":
                    df = group2[2]
            else:
                distribution = group1[-1]
                loc = group1[0]
                scale = group1[1]
                if distribution == "t":
                    df = group1[2]

            # vygenerování nové hodnoty a vynásobení současnou hodnotou
            # pro získání změny ceny
            if distribution == "n":
                ds = st * sps.norm.rvs(loc=loc,scale=scale)
            elif distribution == "c":
                ds = st * sps.cauchy.rvs(loc=loc,scale=scale)
            elif distribution == "l":
                ds = st * sps.laplace.rvs(loc=loc,scale=scale)
            elif distribution == "t":
                if df == None:
                    raise ValueError("Degrees of freedom (df) parameter has to be specified")
                ds = st * sps.t.rvs(df,loc=loc,scale=scale)
            else:
                raise ValueError("Distribution parameter must be: 'n'(normal - default) or 'c'(cauchy) or 'l'(laplace) or 't'(student's t)")
            # vytvoření nové aktuální hodnoty
            st = st + ds
            path.append(st)

        # po skončení generování kroků každé simulace spočítat průměr hodnot
        # z průměrovacího období
        if non_avg_steps>0:
            # +1 kvůli odstranění výchozí hodnoty
            avg_spot = np.average(path[non_avg_steps+1:])
        else:
            if len(avg_values) == -non_avg_steps:
                # 1: kvůli odstranění výchozí hodnoty
                # přidání už známých hodnot z průměrovacího období
                averaging_arr = [*avg_values, *path[1:]]
                avg_spot = np.average(averaging_arr)
            else:
                raise ValueError(f"Number of already known values for average ({len(avg_values)}) does not match expected number ({-non_avg_steps})")

        # výpočet hodnoty opce
        if strike_type == "fixed":
            payoff = max(position * (avg_spot-strike),0)
        elif strike_type == "floating":
            payoff = max(position * (st-avg_spot),0)
        else:
            raise Exception("Strike type can be either 'fixed' or 'floating'")
        # připočtení k celkovému součtu hodnot simulací
        total = total + payoff
        payoffs.append(payoff)
        paths.append(path)
    # vrácení hodnot z funkce po provedení všech simulací
    return total, paths, payoffs




#
# Simulation of spread option (e.g. calendar spread option)
# GBM model is used
#
#

def spread_simulation_gbm_final(*,position_flag,initial_price1, initial_price2,
        strike, simulations, steps, loc1, loc2, scale1, scale2, cor):
    """
    Funkce vrátí celkový součet zisků ze všech simulací
    + všechny nasimulované cesty ve formě array
    + array všech cen jednotlivých simulací

    Parametry:
    * position_flag - "c" pro CALL, "p" pro PUT
    * initial_price - výchozí cena
    * strike
    * simulations - počet simulací
    * steps - počet kroků do expirace
    * loc a scale - hodnoty určující normální rozdělení
    * cor - korelace mezi hodnotami obou kontraktů

    """
    # inicializace proměnných pro výsledky simulací
    total = 0.0
    paths1 = []
    paths2 = []
    payoffs = []

    # příprava počtu simulací pro for loop,
    # počet simulací a počet kroků každé simulace
    sim_range = range(1,simulations+1)
    step_range = range(1,steps+1)

    for _ in sim_range:
        # nastavení výchozích hodnot pro simulaci
        path1 = [initial_price1]
        path2 = [initial_price2]
        st1 = initial_price1
        st2 = initial_price2
        for _ in step_range:
            # generování hodnoty pro první podkladové aktivum
            noise1 = sps.norm.rvs(loc=0, scale=1)
            ds1 = st1 * (loc1 + scale1 * noise1)
            st1 = st1 + ds1
            path1.append(st1)
            # generování hodnoty pro druhé podkladové aktivum
            # s respektováním korelace
            noise2 = (( cor * noise1 ) +
                    ( sps.norm.rvs(loc=0,scale=1) * np.sqrt(1-cor**2) ))
            ds2 = st2 * (loc2 + scale2 * noise2)
            st2 = st2 + ds2
            path2.append(st2)
        # výpočet hodnoty opce po vygenerování všech kroků simulace
        if position_flag == "c":
            payoff = max(((st1-st2) - strike), 0)
        elif position_flag == "p":
            payoff = max((strike - (st1-st2)), 0)
        else:
            raise ValueException("Position can be either 'p' for put or 'c' for call")
        # připočtení k celkovému součtu hodnot simulací
        total = total + payoff
        paths1.append(path1)
        paths2.append(path2)
        payoffs.append(payoff)
    # vrácení hodnot z funkce po provedení všech simulací
    return total, [paths1,paths2], payoffs


#
# Simulation of asian option
# mean reverting model is used
#
#

def asian_simulation_mean_reverting_final(*,position_flag,initial_price, strike, simulations, steps,
                                avg_steps , avg_values=[], group=(), mean_value,reversion_speed, strike_type="fixed"):
    """
        Funkce vrátí celkový součet zisků ze všech simulací
        + všechny nasimulované cesty ve formě array
        + array všech cen jednotlivých simulací

        Parametry:
        * position_flag - "c" pro CALL, "p" pro PUT
        * initial_price - výchozí cena
        * strike
        * simulations - počet simulací
        * steps - počet kroků do expirace
        * avg_steps - počet korků v průměrovacím období
        * avg_values - už známé hodnoty průměrovacího období
        * group - vyžaduje tuple ve tvaru
                (loc,scale,distribution) nebo (loc,scale,df,distribution)
        * mean_value - dlouhodobá průměrná hodnota
        * reversion_speed - míra rychlosti návratu k průměrné hodnotě
        * strike_type - "floating" nebo "fixed"

    """
    # výpočet počtu kroků, které nepatří do průměrovacího období
    non_avg_steps = steps - avg_steps
    # kontrola, jestli počet známých hodnot je stejný jako vypočítaná hodnota
    # pokud už je výchozí hodnota v průměrovacím období
    if non_avg_steps < 0:
        if -non_avg_steps != len(avg_values):
            raise ValueError(f"avg_values count ({len(avg_values)}) must be equal to {-non_avg_steps}")
    # inicializace proměnných pro výsledek simulace
    total = 0.0
    paths = []
    payoffs = []
    # funkce, která vrátí 1 pro "c" a -1 pro "p"
    position = owner_position(position_flag)

    # příprava počtu simulací pro for loop,
    # počet simulací a počet kroků každé simulace
    sim_range = range(1,simulations+1)
    step_range = range(1,steps+1)

    # hodnoty pro upřesnění generovaných hodnot
    distribution = group[-1]
    loc = group[0]
    scale = group[1]
    if distribution == "t":
        df = group[2]

    for _ in sim_range:
        # nastavení výchozí hodnoty
        path = [initial_price]
        st = initial_price

        for _ in step_range:
            # vygenerování a výpočet změny ceny
            if distribution == "n":
                ds = (reversion_speed * (mean_value-st)
                        + sps.norm.rvs(loc=loc,scale=scale))
            elif distribution == "c":
                ds = (reversion_speed * (mean_value-st)
                        + sps.cauchy.rvs(loc=loc,scale=scale))
            elif distribution == "l":
                ds = (reversion_speed * (mean_value-st)
                        + sps.laplace.rvs(loc=loc,scale=scale))
            elif distribution == "t":
                if df == None:
                    raise ValueError("Degrees of freedom (df) parameter has to be specified")
                ds = (reversion_speed * (mean_value-st)
                        + sps.t.rvs(df,loc=loc,scale=scale))
            else:
                raise ValueError("Distribution parameter must be: 'n'(normal - default) or 'c'(cauchy) or 'l'(laplace) or 't'(student's t)")
            # vytvoření nové aktuální hodnoty
            st = st + ds
            path.append(st)

        # po skončení generování kroků každé simulace spočítat průměr hodnot
        # z průměrovacího období
        if non_avg_steps>0:
            # +1 kvůli odstranění výchozí hodnoty
            avg_spot = np.average(path[non_avg_steps+1:])
        else:
            if len(avg_values) == -non_avg_steps:
                # 1: kvůli odstranění výchozí hodnoty
                # přidání už známých hodnot z průměrovacího období
                averaging_arr = [*avg_values, *path[1:]]
                avg_spot = np.average(averaging_arr)
            else:
                raise ValueError(f"Number of already known values for average ({len(avg_values)}) does not match expected number ({-non_avg_steps})")

        # výpočet hodnoty opce
        if strike_type == "fixed":
            payoff = max(position * (avg_spot-strike),0)
        elif strike_type == "floating":
            payoff = max(position * (st-avg_spot),0)
        else:
            raise Exception("Strike type can be either 'fixed' or 'floating'")
        total = total + payoff
        payoffs.append(payoff)
        paths.append(path)
    # vrácení hodnot z funkce po provedení všech simulací
    return total, paths, payoffs
