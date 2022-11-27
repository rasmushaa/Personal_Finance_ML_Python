'''
Created on 10 Sep 2022

@author: rasmus
'''




from transactions import Categories
from file_parsing import DataFrame
from google_api import GoogleAPI
from ai import AI



class Application():
    def __init__(self):
        super().__init__()
        self.categories = Categories()       
        self.google_api = GoogleAPI(self)
        self.data_frame = DataFrame(self)
        self.ai = AI(self)
        