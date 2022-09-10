'''
Created on 4 Sep 2022

@author: rasmus
'''




import  gspread
from    google.oauth2.service_account import Credentials
from    error_handling import MyWarningError


class Google_API():
    
    def __init__(self):
        self._client = None
             
                
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
            google_sh = self._client.open(sheet)
            sheet1 = google_sh.get_worksheet(0)
            print(sheet1) 
            
        except Exception as e:
            msg = "Writing to Google Drive failed"
            raise MyWarningError(msg, e, fatal=False)
        
        
