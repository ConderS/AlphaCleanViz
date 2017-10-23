import logging

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

formatString = '%(asctime)s %(levelname)-8.8s [%(module)s] [%(funcName)s:%(lineno)4s] %(message)s'
formatter = logging.Formatter(formatString)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler('application-log.txt')
fh.setFormatter(formatter)
logger.addHandler(fh)

import traceback
import time
import sys
import argparse
import json
import csv

import model

CHART_MAPPING = {
    'bar'       : model.BarChart,
    'scatter'   : model.ScatterPlot,
    'line'      : model.LineChart
}

class Pipeline(object):

    def __init__(self):
        self.chart_type = None
        self.chart = None
        self.vega_json = None

    def convert_csv_to_dict(self, data_file, columns):
        reader = csv.DictReader(open(data_file, encoding='utf-8-sig'))
        data = []

        for line in reader:
            data.append(line)

        if columns:
            return data, columns

        columns = []
        for k, _ in data[0]:
            columns.append(k)
        return data, columns


    def run(self, data_file, columns, chart_type):
        self.chart_type = chart_type
        data, columns = self.convert_csv_to_dict(data_file, columns)
        self.chart = CHART_MAPPING[chart_type](data, columns)
        self.vega_json = self.chart.build()

        output_file = 'spec.json'
        vega_spec = open(output_file, 'w')
        json.dump(self.vega_json, vega_spec)
        logger.info('Vega specification outputted as: ' + output_file)

    

if __name__ == '__main__':
    logger.info('Starting Script')

    parser = argparse.ArgumentParser(description='Vega Generator')

    parser.add_argument('--data',
        type = str,
        dest = 'data_file',
        default = None,
        help = 'Respective location of data file')

    parser.add_argument('--columns',
        type = str,
        default = None,
        dest = 'columns',
        nargs = '+',
        help = 'Columns to be plotted')

    parser.add_argument('--chart_type',
        type = str,
        dest = 'chart_type',
        default = 'bar',
        help = 'Specifies the type of viz generated')

    args = parser.parse_args()

    if len(sys.argv) < 3:
        print('Not enough args')
        sys.exit()

    try:
        pipeline = Pipeline()
        pipeline.run(data_file = args.data_file,
                     columns = args.columns,
                     chart_type = args.chart_type,)
    except:
        fatalMessage = traceback.format_exc()
        logger.error("[Unknown Error] %s", fatalMessage)
        logger.info("Ending Script Unsuccessfully")