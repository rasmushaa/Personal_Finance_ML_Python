'''
Created on 10 Sep 2022

@author: rasmus
'''




from    app_functions.settings          import Settings
from    app_functions.file_parsing      import  DataFrame
from    app_functions.google_api        import  GoogleAPI



class Application():
    def __init__(self):
        super().__init__()
        self.settings       = Settings()        
        self.google_api     = GoogleAPI()
        self.pf_dataFrame   = DataFrame()
        
                             
    def predict_category(self):
        pass