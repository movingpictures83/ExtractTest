import pandas as pd
import os
import json
import PyPluMA

class ExtractTestPlugin:
    def input(self, filename):
        self.parameters = dict()
        infile = open(filename, 'r')
        for line in infile:
           contents = line.strip().split('\t')
           self.parameters[contents[0]] = contents[1]

        data_path = PyPluMA.prefix()+"/"+self.parameters["inputfile"]
        self.data = pd.read_csv(data_path, index_col=0, parse_dates=True)

        meta_information_path = PyPluMA.prefix()+"/"+self.parameters["metainformation"]
        with open(meta_information_path, 'r') as file: 
           self.meta_information = json.load(file)

    def run(self):
        test_start = self.meta_information['test_start']

        loc_end = self.data.index.get_loc(test_start)
        self.data_test = self.data.iloc[loc_end-100:]

    def output(self, filename):
        #os.makedirs('data_raw/elect_prediction/',exist_ok=True)
        self.data_test.iloc[:400].to_csv(filename)
