import datetime as dt
import pyexcel as pe
from . import DataSet


class NPD_DataSet(DataSet):


    def __init__(self, dataset):
        super(NPD_DataSet, self).__init__(dataset)
        self.data_file = None
        self.product_data = {}
        self.unit_data = {}
        self.revenue_data = {}
        self.date_range_data = []
        self.MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 5, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    # sets the data file to be parsed
    def set_data_file(self, data_file):
        self.data_file = pe.get_sheet(file_name=data_file)

    # cleans the raw data set from The NPD Group, Inc.
    def clean_data(self):
        if not self.data_file:
            return False
        self.data_file.delete_rows([0, 1])

        # collect information about product spec offsets
        self.product_data['max_columns'] = self.data_file.row[1].index('Units') - 1
        self.product_data['product_info'] = []
        for i in range(1, (self.product_data['max_columns'] + 1)):
            self.product_data['product_info'].append({'spec': self.data_file[1, i], 'index': i})

        # collect information about the unit data offsets
        self.unit_data['max_columns'] = self.data_file.row[0].count('Units')
        self.unit_data['start_column'] = self.data_file.row[0].index('Units')
        self.unit_data['end_column'] = (self.unit_data['max_columns'] + self.unit_data['start_column']) - 1

        # collect information about the revenue data offsets
        self.revenue_data['max_columns'] = self.data_file.row[0].count('Dollars')
        self.revenue_data['start_column'] = self.data_file.row[0].index('Dollars')
        self.revenue_data['end_column'] = (self.revenue_data['max_columns'] + self.data_file.row[0].index(
            'Dollars')) - 1

        # parse out the date information
        self.date_range_data = [self.parse_date_data(self.data_file.row[1][i]) for i in
                                range(self.unit_data['start_column'], (self.unit_data['end_column'] + 1))]

        # clean the data by deleting the text at the bottom of the file
        self.data_file.delete_rows(
            [0, 1, 2, (self.data_file.number_of_rows() - 1), (self.data_file.number_of_rows() - 2),
             (self.data_file.number_of_rows() - 3), (self.data_file.number_of_rows() - 4),
             (self.data_file.number_of_rows() - 5), (self.data_file.number_of_rows() - 6),
             (self.data_file.number_of_rows() - 7), (self.data_file.number_of_rows() - 8),
             (self.data_file.number_of_rows() - 9)])
        return True

    # saves a market report to the database collection Market View
    def save_report(self):
        # format data for processing
        for entry in self.data_file:
            self.add_report(self.parse_units_and_revenue(entry))


    # parse date into dict
    def parse_date_data(self, date):
        result = {}
        result['week_start'] = date.split(' - ')[0]
        result['week_end'] = date.split(' - ')[1]
        result['month_start'] = result['week_start'].split(' ')[0] + ' ' + result['week_start'].split(' ')[2]
        result['month_end'] = result['week_end'].split(' ')[0] + ' ' + result['week_end'].split(' ')[2]
        result['year_start'] = result['month_start'].split(' ')[1]
        result['year_end'] = result['month_end'].split(' ')[1]
        result['iso_date'] = dt.datetime(int(result['year_start']), self.MONTHS[result['week_start'].split(' ')[0]], int(result['week_start'].split(' ')[1]), 0, 0, 0)
        return result

    # parse the unit and revenue data into a dict
    def parse_units_and_revenue(self, data):
        result = {}
        result['brand'] = data[0]
        result['product'] = []
        for i in range(len(self.product_data['product_info'])):
            result['product'].append({'spec_type': self.product_data['product_info'][i]['spec'], 'spec_value': data[self.product_data['product_info'][i]['index']]})
        units = [{'units': data[i]} for i in range(self.unit_data['start_column'], (self.unit_data['end_column'] + 1))]
        revenue = [
            {'revenue': data[i], 'time_frame': self.date_range_data[i - self.revenue_data['start_column']]} for i in
            range(self.revenue_data['start_column'], (self.revenue_data['end_column'] + 1))]
        result['sale_statement'] = [dict(ele[0], **ele[1]) for ele in zip(units, revenue)]
        return result






