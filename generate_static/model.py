import logging
import json
from enum import Enum
import heapq as hpq
import numpy as np

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

class BarChart(Chart):

    def build(self):
        self.logger.info('Building Vega Specification for a bar chart...')

        skel_file = open(SKELETONS['BarChart']).read()
        self.spec = json.loads(skel_file)

        # Defines data values in-line
        updateNestedDictByVal(self.spec, None, self.data)

        # Alternates between columns to fill in relevant X and Y fields in Vega's scale, title, and marks specifications
        for idx in range(0, 6):
            if idx % 2:
                val = self.columns[1]
            else:
                val = self.columns[0]
            updateNestedDictByVal(self.spec, None, val)

        self.logger.info('Done Building')

        return self.spec



class ScatterPlot(Chart):

    def get_domain(self):
        x_title = self.columns[0]
        y_title = self.columns[1]
        y_data = []

        x_max_domain = -float('inf')

        for record in self.data:
            for key, value in record.items():
                if (key is not None) and (value != 'null'):
                    if key == x_title:
                        x_max_domain = max(x_max_domain, float(value)) 
                    if key == y_title:
                        hpq.heappush(y_data, float(value))

        return x_max_domain, np.percentile(y_data, 99.5) 

    def build(self):
        self.logger.info('Building Vega Specification for a scatter plot...')

        skel_file = open(SKELETONS['ScatterPlot']).read()
        self.spec = json.loads(skel_file)

        # Fills in data values
        updateNestedDictByVal(self.spec, "_data_values", self.data)

        x_max_domain, y_high_range = self.get_domain()
        x_domain = [0, x_max_domain]
        y_domain = [0, y_high_range]
        updateNestedDictByVal(self.spec, "_x_domain", x_domain)
        updateNestedDictByVal(self.spec, "_y_domain", y_domain)

        # Alternates between columns to fill in relevant X and Y fields in Vega's scale, title, and marks specifications
        for i in range(3, 11):
            if not i % 3:
                val = self.columns[2]
            elif i % 3 == 2:
                val = self.columns[1]
            else:
                val = self.columns[0]
            updateNestedDictByVal(self.spec, None, val)

        self.logger.info('Done Building')

        return self.spec




class LineChart(Chart):
    pass