'''
Created on 4 Sep 2022

@author: rasmus
'''




from utilis import MyWarningError
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


'''
This module pushes the labeled data to Google sheets.
In order to use this, a Google service account must be created,
and a google sheet file shared to that account.
Then, the account can be authorized using the secret key on 
your local machine.
References: https://www.youtube.com/watch?v=bu5wXjz2KvU&t=595s
'''

class GoogleAPI():
    
    def __init__(self, app):
        self._client = None
        self._app = app
                            
    def auth(self, key: str):
        try:         
            scope = ['https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive']
            creds = Credentials.from_service_account_file(key, scopes=scope)
            self._client = gspread.authorize(creds) 
                           
        except Exception as e:
            msg = "Authentication of Google service account failed"
            raise MyWarningError(msg, e, fatal=False)
              
    def write_to_cloud(self, sheet: str):     
        try:    
            df = self._app.data_frame.get_df_gs()
            google_sh = self._client.open(sheet)
            worksheet = google_sh.worksheet('_dataframe_transactions')
            worksheet.append_rows(df.values.tolist(), 
                                  value_input_option="USER_ENTERED")
                     
        except Exception as e:
            msg = "Writing to Google Drive failed"
            raise MyWarningError(msg, e, fatal=False)
        
        
    def get_from_cloud(self, sheet: str):  
        try:      
            google_sh = self._client.open(sheet)
            worksheet = google_sh.worksheet('_dataframe_transactions')
            matrix = worksheet.get_all_values()
            df = pd.DataFrame(data=matrix[1:][:], columns=matrix[0][:])
            return df                
        except Exception as e:
            msg = "Downloading data from Google Drive failed"
            raise MyWarningError(msg, e, fatal=False)
        
        
