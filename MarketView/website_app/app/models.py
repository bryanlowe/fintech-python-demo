from __future__ import unicode_literals
from pymongo import MongoClient

# Create your models here.

# base model
class Model():

    def __init__(self, dataset, request):
        self.client = MongoClient()
        self.database = self.client.market_view
        self.collection = self.database[dataset]
        self.pipeline = []
        self.build_pipleine(request)

    # constructs the pipeline
    def build_pipleine(self, request):
        # unwind sale statement
        self.pipeline.append({"$unwind": "$sale_statement"})

        # perform projections
        projection = {'$project' : {'_id': 0}}
        projection = self.project_data_type(projection, request['data_type'])
        projection = self.project_time_frame(projection, request['time_frame'])
        projection['$project']['brand'] = 1
        self.pipeline.append(projection)

        # sort by time_frame
        sort = {'$sort': {'sale_statement.time_frame.iso_date': 1}}
        self.pipeline.append(sort)

        # group by brand, time frame and data value
        group = self.group_data(request)
        self.pipeline.append(group)

        # sort by brand
        sort = {'$sort': {'_id.brand': 1, 'iso_date': 1}}
        self.pipeline.append(sort)

    # perform projection on data type
    def project_data_type(self, projection, data_type):
        if data_type == 'units':
            projection['$project']['sale_statement.units'] = 1
        else:
            projection['$project']['sale_statement.revenue'] = 1
        return projection

    # perform projection on time frame
    def project_time_frame(self, projection, time_frame):
        # project just the time_frame needed
        if time_frame == "month":
            projection['$project']['sale_statement.time_frame.month_start'] = 1
        elif time_frame == "week":
            projection['$project']['sale_statement.time_frame.week_start'] = 1
        elif time_frame == "year":
            projection['$project']['sale_statement.time_frame.year_start'] = 1
        projection['$project']['sale_statement.time_frame.iso_date'] = 1
        return projection

    # groups data into a matrix
    def group_data(self, request):
        group = {'$group': {'_id': {'brand': '$brand'}, 'value': {}, 'iso_date': {}}}

        # set the time frame into the id
        if request['time_frame'] == 'month':
            group['$group']['_id']['time_frame'] = '$sale_statement.time_frame.month_start'
        elif request['time_frame'] == 'year':
            group['$group']['_id']['time_frame'] = '$sale_statement.time_frame.year_start'
        else:
            group['$group']['_id']['time_frame'] = '$sale_statement.time_frame.week_start'

        # group values together
        group['$group']['value']['$sum'] = {}
        if request['data_type'] == 'units':
            group['$group']['value']['$sum'] = '$sale_statement.units'
        else:
            group['$group']['value']['$sum'] = '$sale_statement.revenue'

        # include first iso date
        group['$group']['iso_date']['$first'] = '$sale_statement.time_frame.iso_date'
        return group

    # get the aggregate data
    def get_data(self):
        result = list(self.collection.aggregate(self.pipeline, allowDiskUse=True, useCursor=False))
        return result

    # creates a table for the view
    def create_database_table(self, response_data, dataset):
        current_brand = ''
        response_data['thead'] = []
        response_data['tbody'] = []

        # gather sale period
        sale_period = list(set(item['iso_date'] for item in dataset))
        sale_period.sort()
        trow = []
        set_time_header = False

        # create the table body with values
        for item in dataset:
            # add brand as a tbody entry
            if current_brand != item['_id']['brand']:
                if (len(trow) > 0):
                    response_data['tbody'].append(trow)
                    trow = []
                trow.append(item['_id']['brand'])
                current_brand = item['_id']['brand']
            for time in sale_period:
                if item['iso_date'] == time:
                    # add the current value to trow
                    trow.append(item['value'])

                    # add time to the thead
                    if set_time_header == False:
                        response_data['thead'].append(item['_id']['time_frame'])
                        if len(response_data['thead']) == len(sale_period):
                            set_time_header = True
        return response_data

# brand share model
class BrandShare(Model):

    def __init__(self, dataset, request):
        super(BrandShare, self).__init__(dataset, request)

# sales growth model
class SalesGrowth(Model):

    def __init__(self, dataset, request):
        super(SalesGrowth, self).__init__(dataset, request)

# industry model
class Industry(Model):

    def __init__(self, dataset, request):
        super(Industry, self).__init__(dataset, request)

# product trends model
class ProductTrends(Model):

    def __init__(self, dataset, request):
        super(ProductTrends, self).__init__(dataset, request)

# pricing model
class Pricing(Model):

    def __init__(self, dataset, request):
        super(Pricing, self).__init__(dataset, request)