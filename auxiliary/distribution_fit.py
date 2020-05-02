
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
    t_params = sps.t.fit(data)
    cauchy_params = sps.cauchy.fit(data)
    laplace_params = sps.laplace.fit(data)
    print("Parameters are in this format: (location, scale)")
    print(normal_params)
    print(t_params)
    print(cauchy_params)
    print(laplace_params)

    # test which distribution fits the data best (looking for largest p-value)
    res_n = sps.kstest(data, "norm", args=(normal_params))
    res_t = sps.kstest(data, "t", args=(t_params))
    res_c = sps.kstest(data, "cauchy", args=(cauchy_params))
    res_l = sps.kstest(data, "laplace", args=(laplace_params))

    print("\nThe larger the p-value, the better")
    print("Normal: ",res_n[1])
    print("Student t", res_t)
    print("Cauchy: ",res_c)
    print("Laplace: ",res_l)

    print("TE ",[*normal_params ,res_n[1]])
    parameters = pd.DataFrame({"Normal": [*normal_params, res_n[1]],
                               "T": [*t_params[1:],res_t[1]],
                               "Cauchy": [*cauchy_params, res_c[1]],
                               "Laplace": [*laplace_params, res_l[1]]},
                               index=["Loc","Scale","p (KSTest)"]
                               )

    return parameters
