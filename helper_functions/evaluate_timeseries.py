
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.gofplots import qqplot
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.stattools import jarque_bera

def evaluate_ts_data(data):
    """
    Function takes time series data and evaluates with various tests whether the data is
    normally distributed and checks for autocorrelation between given and lagged entries

    Tests for normality:
        * Q-Q plot
        * Jarque Bera test
    Test for autocorrelation:
        * Autocorrelation function
        * Partial autocorrelation function
        * Ljung-Box test

    """
    # Tests
    jb_score, jb_pvalue, jb_skew, jb_kurtosis = jarque_bera(rets1)
    jb_s = pd.DataFrame({'Score': [jb_score], 'p value': [jb_pvalue]})
    print("\nJarque Bera test (tests for normality of data)")
    print(jb_s)

    lb_result = acorr_ljungbox(rets1, lags=[30], boxpierce=False, return_df=True)
    print("\nLjung-Box test ( tests autocorrelation)")
    print(lb_result)

    # Plot graphs
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10,5))

    plot_acf(data,ax=ax1)
    ax1.set_title('Autocorrelation function')

    plot_pacf(data,ax=ax2)
    ax2.set_title('Partial autocorrelation function')

    qqplot(data,ax=ax3,line="s")
    ax3.set_title('Q-Q plot')

    ax4.hist(data,bins=50)
    ax4.set_title('Data histogram')

    plt.tight_layout()
