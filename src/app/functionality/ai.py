'''
Created on 11 Sep 2022

@author: rasmus
'''




from utilis import MyWarningError
import pandas as pd
import numpy as np
import os
import joblib
import queue
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

MODEL_NAME  = "_trained_model.pkl"
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
FILE = os.path.join(ROOT_DIR, 'files', MODEL_NAME)


class AI():
    
    def __init__(self, app):
        self._app = app
        self._model = None
        self._active = True
               
    def predict_category(self, X: type[pd.DataFrame]) -> list:
        '''
        .predict returns list containing class for
        each X, even in case of one row data frame.
        '''
        if self._active and self._model is None:
            self._load_model()
        if self._active:
            category = self._model.predict(X)
            return category
       
    def predict_proba(self, X: type[pd.DataFrame]) -> list:
        '''
        .predict_proba returns list containing values for
        every class of trained model, and thus 
        .max() value is the predicted category
        '''
        if self._active and self._model is None:
            self._load_model()
        if self._active:
            probabs = self._model.predict_proba(X)
            probabs = [max(classes) for classes in probabs]
            return probabs
      
    def seted_up(self) -> bool:
        if self._active:
            return True
        else:
            return False
       
    def get_info_str(self):
        msg = str(self._model)
        return msg
      
    def _load_model(self):       
        try:
            with open(FILE , 'rb') as file:
                model_pipeline = joblib.load(file)
                self._model = model_pipeline
        except Exception as e:
            self._active = False
            msg = ("AI module could not be loaded!\nIt may be corrupted or missing.\nProceeding without...")
            raise MyWarningError(msg, e, fatal=False)
    
    def train_model(self, queue_signal: queue.Queue=None):
        try:   
            if self._app.data_frame.get_df().empty:
                raise ValueError("No data frame was selected!")   
            dataset = self._app.data_frame.get_df_training()
                        
            # ===================== DATA SPLIT ===========================
            training_data = dataset.iloc[:, [1, 2]]
            class_data = dataset.iloc[:, 3]
            X_train, X_test, y_train, y_test = train_test_split(training_data, 
                                                                class_data, 
                                                                test_size=0.2, 
                                                                random_state=21, 
                                                                stratify=class_data)

            # ===================== PIPELINE ===========================
            text_transformer = Pipeline(
                steps=[
                   ('textVectorizer', CountVectorizer()),
                   ('wordBankDimRed', SelectKBest(chi2, k='all'))
                ]
            )
            preprocessor = ColumnTransformer(
               transformers=[
                   ('textTransformer', text_transformer, 0)
                   
                ], remainder = 'passthrough'
            ) 
            pipeline = Pipeline(
                steps=[
                    ("preprocessor", preprocessor),
                    ('randomForest', RandomForestClassifier())
                ]
            )
            
            # ======================= HYPERPARAMETERS  ==========================
            n_estimators        = [int(x) for x in np.linspace(start = 1, stop = 120, num = 120)]
            max_depth           = [int(x) for x in np.linspace(1, 50, num = 50)]
            min_samples_split   = [int(x) for x in np.linspace(1, 20, num = 20)]
            min_samples_leaf    = [int(x) for x in np.linspace(1, 10, num = 10)]
            bootstrap           = [True, False]
            chi2_k              = [int(x) for x in np.linspace(start = 50, stop = 200, num = 150)]
                  
            random_grid =  {'randomForest__n_estimators': n_estimators,
                            'randomForest__max_depth': max_depth,
                            'randomForest__min_samples_split': min_samples_split,
                            'randomForest__min_samples_leaf': min_samples_leaf,
                            'randomForest__bootstrap': bootstrap,
                            'preprocessor__textTransformer__wordBankDimRed__k': chi2_k}
    
            tuned_model = RandomizedSearchCV(estimator=pipeline, 
                                           param_distributions=random_grid, 
                                           n_iter=500, 
                                           cv=3, 
                                           verbose=0, 
                                           random_state=42, 
                                           n_jobs =-1)
            
            tuned_model.fit(X_train, y_train)
            best_model = tuned_model.best_estimator_               
            y_pred = best_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred) 

            with open(FILE , 'wb') as file:
                joblib.dump(best_model, file)

            if queue_signal is not None: 
                queue_signal.put({'progress': 1000})
                queue_signal.put({'accuracy': accuracy}) 

        except Exception as e:
            if queue_signal is not None:
                queue_signal.put({'error': e})
            else:
                msg = "Training the AI model failed!"
                raise MyWarningError(msg, e, fatal=False)
        