
import scipy.stats as sps
import pandas as pd

def distribution_fit(data):
    """
    Estimate the parameters for distributions based on inputted data

    Distributions fitted:
        * Normal
        * Cauchy
        * Laplace

    Returns dataframe of all fitted distributions' parameters
    """

    normal_params = sps.norm.fit(data)
    cauchy_params = sps.cauchy.fit(data)
    laplace_params = sps.laplace.fit(data)
    print("Parameters are in this format: (location, scale)")
    print(normal_params)
    print(cauchy_params)
    print(laplace_params)

    parameters = pd.DataFrame({"Normal":normal_params,
                               "Cauchy": cauchy_params,
                               "Laplace": laplace_params},
                               index=["Loc","Scale"]
                               )

    # test which distribution fits the data best (looking for largest p-value)
    res_n = sps.kstest(lrets, "norm", args=(normal_params))
    res_c = sps.kstest(lrets, "cauchy", args=(cauchy_params))
    res_l = sps.kstest(lrets, "laplace", args=(laplace_params))

    print("\nThe larger the p-value, the better")
    print("Normal: ",res_n)
    print("Cauchy: ",res_c)
    print("Laplace: ",res_l)

    return parameters
