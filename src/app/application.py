'''
Created on 10 Sep 2022

@author: rasmus
'''




from .functionality import Categories
from .functionality import DataFrame
from .functionality import GoogleAPI
from .functionality import AI



class Application():
    def __init__(self):
        super().__init__()
        self.categories = Categories()       
        self.google_api = GoogleAPI(self)
        self.data_frame = DataFrame(self)
        self.ai = AI(self)
        