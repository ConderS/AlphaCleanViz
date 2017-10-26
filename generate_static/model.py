import logging
import json
from enum import Enum

from utils import updateNestedDictByVal

_root = "skeletons/"

SKELETONS = {
    'BarChart' : _root + "barchart.json",
    'ScatterPlot' : _root + "scatterplot.json",
    'LineChart' : _root + "linechart.json"
}
    

class Chart(object):
    def __init__(self, data, columns):
        self.logger = logging.getLogger('main')
        self.data = data
        self.columns = columns
        self.spec = None

    def build(self):
        pass

    def get_domain(self):
        pass

    def update_data(self, data_fields, new_values):
        for counter, field in enumerate(data_fields):
            updateNestedDictByVal(self.spec, field, new_values[counter])
        
        self.logger.info('Done Building')


class BarChart(Chart):

    def build(self):
        self.logger.info('Building Vega Specification for a bar chart...')

        skel_file = open(SKELETONS['BarChart']).read()
        self.spec = json.loads(skel_file)

        data_fields = ['_data_values', '_x_title', '_y_title']
        new_values = [self.data, self.columns[0], self.columns[1]]

        self.update_data(data_fields, new_values)

        return self.spec

class ScatterPlot(Chart):

    def get_domain(self):
        x_title = self.columns[0]
        y_title = self.columns[1]

        x_max_domain = -float('inf')
        x_min_domain = float('inf')
        y_max_domain = -float('inf')
        y_min_domain = float('inf')

        for record in self.data:
            for key, value in record.items():
                if (key is not None) and (value != 'null'):
                    if key == x_title:
                        x_max_domain = max(x_max_domain, float(value)) 
                        x_min_domain = min(x_min_domain, float(value))
                    if key == y_title:
                        y_max_domain = max(y_max_domain, float(value)) 
                        y_min_domain = min(y_min_domain, float(value)) 

        x_domain = [x_min_domain, x_max_domain]
        y_domain = [y_min_domain, y_max_domain]

        return x_domain, y_domain


    def build(self):
        self.logger.info('Building Vega Specification for a scatter plot...')

        skel_file = open(SKELETONS['ScatterPlot']).read()
        self.spec = json.loads(skel_file)

        data_fields = ['_data_values', '_x_domain', '_y_domain', '_x_title', '_y_title', '_z_title']

        x_domain, y_domain = self.get_domain()
        x_domain[0] = min(0, x_domain[0])
        y_domain[0] = min(0, y_domain[0])
        
        new_values = [self.data, x_domain, y_domain, self.columns[0], self.columns[1], self.columns[2]]

        self.update_data(data_fields, new_values)

        return self.spec


class LineChart(Chart):

    def build(self):
        self.logger.info('Building Vega Specification for a scatter plot...')
        skel_file = open(SKELETONS['LineChart']).read()
        self.spec = json.loads(skel_file)

        data_fields = ['_data_values', '_x_title', '_y_title', '_color']
        new_values = [self.data, self.columns[0], self.columns[1], self.columns[2]]

        self.update_data(data_fields, new_values)

        return self.spec

