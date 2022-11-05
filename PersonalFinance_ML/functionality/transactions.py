'''
Created on 2 Sep 2022

@author: rasmus
'''




import os
import json
from utilis import MyWarningError


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
FILE = os.path.join(ROOT_DIR, "files", "gategories.json")


class Categories():  
    def __init__(self):  
        try:            
            json = self.load_parameters(FILE)      
            self.expenditures = json["transaction_types"]["expenditure_list"]
            self.incomes = json["transaction_types"]["income_list"]
            
        except Exception as e:
            msg = "Settings could not be loaded!"
            raise MyWarningError(msg, e, fatal=True)
        
    def load_parameters(self, path):
        with open(path) as file:
            return json.load(file)