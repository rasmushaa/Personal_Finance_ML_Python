'''
Created on 2 Sep 2022

@author: rasmus
'''




import os
import json
from utilis.error_handling import MyWarningError

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
FILE = os.path.join(ROOT_DIR, 'files', 'settings.json')


class Settings():  
    def __init__(self):  
        try:            
            json                    = self.load_parameters(FILE)      
            self.application        = Application(**json['application'])
            self.google_api         = Google_api(**json['google_api'])
            self.machine_learning   = Machine_learning(**json['machine_learning'])
            self.transaction_types  = Transaction_types(**json['transaction_types'])
            
        except Exception as e:
            msg = "Settings could not be loaded!"
            raise MyWarningError(msg, e, fatal=True)
        
    def load_parameters(self, path):
        with open(path) as file:
            return json.load(file)
      
        
class Application():  
    def __init__(self, window, title):       
        self.window = window
        self.title = title
        
        
class Google_api():   
    def __init__(self, default_sheet, default_key):     
        self.default_sheet  = default_sheet
        self.default_key    = default_key
        

class Machine_learning():
    def __init__(self):
        pass
    
    
class Transaction_types():
    def __init__(self, expenditure_list, income_list):
        self.expenditure_list = expenditure_list
        self.income_list = income_list
        