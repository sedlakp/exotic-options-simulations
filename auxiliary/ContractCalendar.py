import requests
import pandas as pd

class ContractCalendar:
    """
    Calendar with settlement dates can be accessed by calling calendar variable
    """

    def __init__(self,url):
        """ Parameter is a URL of an Excel file"""
        self.url = url
        self.calendar = self._get_calendar()

    def _get_calendar(self):
        header = {
          "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
          "X-Requested-With": "XMLHttpRequest"
        }

        result = requests.get(self.url, headers=header)
        raw_data = pd.read_excel(result.content, sheet_name=0, header=4)
        raw_data = raw_data.iloc[:,:5]

        # change appropriate columns to datetime for easier handling
        for colname in raw_data.columns[2:]:
            raw_data[colname] = pd.to_datetime(raw_data.loc[:,colname])

        return raw_data

    @classmethod
    def wti_average_option(cls):
        return cls('https://www.cmegroup.com/CmeWS/mvc/ProductCalendar/Download.xls?productId=2767')

    @classmethod
    def wti_1m_spread_option(cls):
        return cls('https://www.cmegroup.com/CmeWS/mvc/ProductCalendar/Download.xls?productId=2952')
