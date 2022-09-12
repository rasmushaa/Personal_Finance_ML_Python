'''
Created on 2 Sep 2022

@author: rasmus
'''




import  os
import  json
from    utilis import MyWarningError

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
FILE = os.path.join(ROOT_DIR, 'files', 'application_settings.json')


class Settings():  
    def __init__(self):  
        try:            
            json                    = self.load_parameters(FILE)      
            self.google_api         = Google_api(**json['google_api'])
            self.transaction_types  = Transaction_types(**json['transaction_types'])
            
        except Exception as e:
            msg = "Settings could not be loaded!"
            raise MyWarningError(msg, e, fatal=True)
        
    def load_parameters(self, path):
        with open(path) as file:
            return json.load(file)
             
        
class Google_api():   
    def __init__(self, default_sheet, default_key):     
        self.default_sheet  = default_sheet
        self.default_key    = default_key
          
class Transaction_types():
    def __init__(self, expenditure_list, income_list):
        self.expenditure_list = expenditure_list
        self.income_list = income_list
        