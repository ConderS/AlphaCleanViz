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
    def __init__(self, data, columns, ):
        self.logger = logging.getLogger('main')
        self.data = data
        self.columns = columns
        self.spec = None


class BarChart(Chart):

    def build(self):
        self.logger.info('Building Vega Specification for a bar chart...')

        skel_file = open(SKELETONS['BarChart']).read()
        self.spec = json.loads(skel_file)

        # Fills in data values
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
   def build(self):
        self.logger.info('Building Vega Specification for a scatter plot...')

        skel_file = open(SKELETONS['ScatterPlot']).read()
        self.spec = json.loads(skel_file)

        # Fills in data values
        updateNestedDictByVal(self.spec, None, self.data)

        # Alternates between columns to fill in relevant X and Y fields in Vega's scale, title, and marks specifications
        for i in range(1, 11):
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