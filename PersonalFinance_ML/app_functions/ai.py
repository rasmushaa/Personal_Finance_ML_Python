'''
Created on 11 Sep 2022

@author: rasmus
'''




from    utilis import   MyWarningError
import                  os
import                  pandas as pd
import                  joblib


MODEL_NAME  = "trained_model.pkl"


class AI():
    
    def __init__(self):
        self._model = None
        self._load_model()
        
        
    def predict_category(self, X: type[pd.DataFrame]) -> list:
        '''
        .predict returns list containing class for
        each X, even in case of one row data frame.
        '''
        category = self._model.predict(X)
        return category
    
    
    def predict_proba(self, X: type[pd.DataFrame]) -> list:
        '''
        .predict_proba returns list containing values for
        every class of trained model, and thus 
        .max() value is the predicted category
        '''
        probabs = self._model.predict_proba(X)
        probabs = [max(classes) for classes in probabs]
        return probabs
    
    
    def seted_up(self) -> bool:
        if self._model == None:
            return False
        else:
            return True
    
    
    def get_info_str(self):
        msg = str(self._model)
        return msg
    
    
    def _load_model(self):
        
        try:
            ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
            FILE = os.path.join(ROOT_DIR, 'files', MODEL_NAME)
            with open(FILE , 'rb') as file:
                model_pipeline = joblib.load(file)
                self._model = model_pipeline
            
        except Exception as e:
            msg = ("Machine learning model could not be loaded!\nProceeding without the module...")
            raise MyWarningError(msg, e, fatal=False)
        
        
        