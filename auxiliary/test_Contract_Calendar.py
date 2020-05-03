import unittest
import pandas as pd

from ContractCalendar import ContractCalendar


class ContractCalendarTestCase(unittest.TestCase):

    def test_fetched_data_columns(self):
        option = ContractCalendar.wti_average_option()
        data_columns = ['Contract Month', 'Product Code', 'First Trade', 'Last Trade',
       'Settlement']
        data_columns_length = len(data_columns)
        self.assertEqual(len(option.calendar.columns),data_columns_length)

    def test_fetched_data_rows(self):
        option = ContractCalendar.wti_average_option()
        rows = len(option.calendar.index)
        has_rows = rows > 0
        self.assertEqual(has_rows, True)

    def test_number_of_business_days(self):
        business_days = ContractCalendar.get_business_days(start="2020-3-20",end="2020-3-27")
        number_of_days = len(business_days)
        self.assertEqual(number_of_days, 6)

    def test_number_of_business_days_in_a_month(self):
        end_date = pd.to_datetime("2020-4-30")
        business_days = ContractCalendar.get_business_days_in_month(end_of_month=end_date)
        number_of_days = len(business_days)
        # https://hr.uiowa.edu/pay/payroll-services/payroll-calendars/working-day-payroll-calendar-2020
        self.assertEqual(number_of_days, 22)


unittest.main()
