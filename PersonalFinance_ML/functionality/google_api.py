'''
Created on 4 Sep 2022

@author: rasmus
'''




from utilis import MyWarningError
import pandas as pd
from datetime import date
import numpy as np
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
        if self._app.pf_dataFrame.get_df().empty:
            raise MyWarningError("DataFrame could not be saved to cloud! \nNo frame was selected...")    
        try: 
            '''
            Adds one empty row for each Category at
            beginning of each month, which ensures that
            averages per month are calculated correctly,
            without actually changing summing values
            Also a category ID is added'''
            temp_df = self._app.pf_dataFrame.get_df().copy()
            founded_times = []
            category_types = list(self._app.categories.expenditures.values()) + list(self._app.categories.incomes.values())  
            offset = 0 
            for index, row in temp_df.iterrows():
                year_month = row['Date'].rsplit('-', 1)[0]
                if year_month not in founded_times:
                    founded_times.append(year_month)
                    for i, category in enumerate(category_types):
                        line = pd.DataFrame({"Date": row['Date'], "Receiver": '', 'Amount': 0.0, 'Category': category}, index=[index+i])
                        temp_df = pd.concat([temp_df.iloc[:index+offset+i], line, temp_df.iloc[index+offset+i:]]).reset_index(drop=True)
                    offset += len(category_types)
                
            '''
            Adds ID category for plotting
            '''
            temp_df['Category ID'] = ""  
            for cat_id, cat in self._app.categories.expenditures.items():
                temp_df.loc[temp_df['Category'] == cat, 'Category ID'] = cat_id
            for cat_id, cat in self._app.categories.incomes.items():
                temp_df.loc[temp_df['Category'] == cat, 'Category ID'] = cat_id
            
            '''
            Time stamp of commit,
            file id
            '''      
            temp_df['Commit date'] = str(date.today())
            temp_df['Commit file'] = self._app.pf_dataFrame.get_bank_str()
            
            '''
            Flip df to chronological order
            for google sheets
            '''
            temp_df = temp_df.iloc[::-1]
            
            google_sh = self._client.open(sheet)
            worksheet = google_sh.get_worksheet(0)
            worksheet.append_rows(temp_df.values.tolist(), 
                                  value_input_option="USER_ENTERED")
            
            
            
        except Exception as e:
            msg = "Writing to Google Drive failed"
            raise MyWarningError(msg, e, fatal=False)
        
        
