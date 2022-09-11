'''
Created on 4 Sep 2022

@author: rasmus
'''




from    utilis                          import  MyWarningError
import                                          gspread
import  pandas                          as      pd
from    google.oauth2.service_account   import  Credentials


class GoogleAPI():
    
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
        
        
    def write_to_cloud(self, sheet: str, df : type[pd.DataFrame]):  
        if df.empty:
            raise MyWarningError("DataFrame could not be saved to cloud! \nNo frame was selected...")    
        try: 
            google_sh = self._client.open(sheet)
            sheet1 = google_sh.get_worksheet(0)
            print(sheet1) 
            print(df.head())
            
        except Exception as e:
            msg = "Writing to Google Drive failed"
            raise MyWarningError(msg, e, fatal=False)
        
        
