import pandas as pd
import numpy as np
from pandas.tseries.offsets import BDay

#
#
# Contains functions of various purpose
#
#

def owner_position(flag: str) -> int:
    if flag == "c":
        return 1
    elif flag == "p":
        return -1
    else:
        raise ValueError(f"Position can be either p or c, not {positionFlag}")

def prepare_data(data):
    if not isinstance(data, pd.DataFrame):
        raise ValueError("The input should be timeseries in pandas DataFrame")
    data = data.squeeze()
    data = data.asfreq(BDay())
    data = data.fillna(method='ffill').dropna()
    return data

def change_to_logrets(data):
    rets = (data/data.shift(1))
    rets = rets.dropna()
    lrets = np.log(rets)
    return lrets
