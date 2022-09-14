'''
Created on 9 Sep 2022

@author: rasmus
'''




from utilis import MyWarningError
import pandas as pd
import chardet
import csv

'''
You may increase capabilities of the software 
by adding your own parser code here.
The _transform2pfdf must output data in the format of:

    0                1                2            3
   'Date'           'Receiver'       'Amount'     'Category'
    str(DateTime)    str              float        str("")
    
If file contains Nan values, those must be converted to str("") values,
since sklearn machine learning model is unable to handle missing values
and will result an error. Although, files will be saved including 
missing values as Nans, to help processing the data in some analyzing software.       
'''


class DataFrame():
    
    def __init__(self):
        self._local_path = ""
        self._data_frame = pd.DataFrame()
        self._bank_file_type = ""
        self._encoding = ""
        self.separator = ""
        
    def get_path(self):
        return self._local_path
               
    def get_df(self):
        return self._data_frame
      
    def get_info_str(self) -> str:
        msg = ("Local path: " + self._local_path +
                "\nData loaded from " + self._bank_file_type + "-file" +
                "\nUsed separator: (" + self._separator + ") endoding: " + self._encoding +
                "\n\nShape of the DataFrame: " + str(self._data_frame.shape) + 
                "\n" + str(self._data_frame.head(10)) +
                "\n\nRows with NaNs:\n" + str(self._data_frame[self._data_frame.isna().any(axis=1)]) +
                "\n\n")
        return msg
      
    def get_x_features(self):
        return self._data_frame.iloc[:, [1, 2]]
    
    def get_x_features_row(self, row: int):
        return self._data_frame.iloc[[row], [1, 2]]
      
    def remove_nans(self):
        self._data_frame = self._data_frame.dropna()
              
    def update_category(self, row: int, category: str):
        self._data_frame.at[row, 'Category'] = category 
    
    def save_data(self):
        if self._data_frame.empty:
            raise MyWarningError("DataFrame could not be saved. \nNo frame selected...")
        else:
            save_path = self._local_path.rsplit('.')[0]
            save_path += "_Labeled.csv"
            self._data_frame.to_csv(save_path, index=False, sep=',', encoding=self._encoding) 
                
    def load_data(self, path: str):      
        try:    
            '''
            Auto detect encoding
            '''     
            with open(path, 'rb') as csvFile:
                encoding_dict = chardet.detect(csvFile.read())
                encoding = encoding_dict['encoding']
            '''
            Auto detect separator
            '''  
            with open(path, 'r', encoding=encoding) as csvFile:
                dialect = csv.Sniffer().sniff(csvFile.read(), delimiters=[',', ';', '', '\t', '|'])
                separator = dialect.delimiter
          
            '''
            Load the file,
            determine the bank,
            transform to PFDF
            '''
            df = pd.read_csv(path, encoding=encoding, sep=separator)           
            bank_file_type = self._detect_bank(df)
            df = self._transform2pfdf(df, bank_file_type)
            
            '''
            If succeeded, 
            add data to class
            '''
            self._local_path = path
            self._data_frame = df
            self._bank_file_type = bank_file_type
            self._encoding = encoding
            self._separator = separator
                                     
        except Exception as e:
            msg = "Data could not be loaded!"
            raise MyWarningError(msg, e, fatal=False)
        
        
    def _detect_bank(self, df: type[pd.DataFrame]) -> str:
        
        column_list = list(df.columns)
        
        if (len(column_list) == 4 and
            column_list[0] == 'Date' and
            column_list[1] == 'Receiver' and
            column_list[2] == 'Amount' and
            column_list[3] == 'Category'):
            return 'PFDF'
        
        if (len(column_list) == 5 and
            column_list[0] == 'Päivämäärä' and
            column_list[1] == 'Saaja/Maksaja' and
            column_list[2] == 'Selite' and
            column_list[3] == 'Viite/Viesti' and
            column_list[4] == 'Määrä'):
            return 'POP_Bank'
        
        ''' if (Your file detection code):
                return 'YouBankCSV'
        '''
        
                  
    def _transform2pfdf(self, df: type[pd.DataFrame], bank_file_type : str) -> type[pd.DataFrame]:      
        try:                      
            '''
            Transform the file to PFDF
            '''
            if bank_file_type == 'PFDF':
                df = df.fillna("")
            
            elif bank_file_type == 'POP_Bank':       
                df = df.rename({'Päivämäärä': 'Date', 
                                'Saaja/Maksaja': 'Receiver', 
                                'Määrä': 'Amount'}, axis=1)      
                df = df.drop(['Selite', 'Viite/Viesti'], axis=1)
                df["Category"] = ""
                df['Amount'] = df['Amount'].str.replace(',', '.')
                df = df.astype({'Amount': 'float'})
                df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
                df['Date'] = df['Date'].dt.date   
                df = df.fillna("")
                              
            ''' if file_type == 'YouBankCSV':
                    Your transform code goes here...
            '''      
            return df
                         
        except Exception as e:
            msg = "Data could not be loaded!"
            raise MyWarningError(msg, e, fatal=False)
        
        
            
            