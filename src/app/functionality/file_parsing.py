'''
Created on 9 Sep 2022

@author: rasmus
'''




from utilis import MyWarningError
import pandas as pd
from datetime import date
import chardet
import csv

'''
You may increase capabilities of the software 
by adding your own parser code here.
The _transform2aidf must output data in the format of:

    0                1                2            3
   'Date'           'Receiver'       'Amount'     'Category'
    str(DateTime)    str              float        str("")
    
If file contains Nan values, those must be converted to str("") values,
since sklearn machine learning model is unable to handle missing values
and will result an error. Although, files will be saved including 
missing values as Nans, to help processing the data in the Data Studio.       
'''


class DataFrame():
    
    def __init__(self, app):
        self._app = app
        self._local_path = ""
        self._data_frame = pd.DataFrame()
        self._bank_file_type = ""
        self._encoding = ""
        self.separator = ""
        
    def get_path(self):
        return self._local_path
    
    def get_bank_str(self):
        return self._bank_file_type
               
    def get_info_str(self) -> str:
        msg = ("Local path: " + self._local_path +
                "\nData loaded from " + self._bank_file_type + "-file" +
                "\nUsed separator: (" + self._separator + ") endoding: " + self._encoding +
                "\n\nShape of the DataFrame: " + str(self._data_frame.shape) + 
                "\n" + str(self._data_frame.head(10)) +
                "\n\nRows with NaNs:\n" + str(len(self._data_frame[self._data_frame.isna().any(axis=1)])) +
                "\n\nRows with Empty strings:\n" + str(len(self._data_frame[self._data_frame.applymap(lambda x: x == '').any(axis=1)])) +
                "\n\n")
        return msg
      
    def get_x_features(self):
        return self._data_frame.iloc[:, [1, 2]]
    
    def get_x_features_row(self, row: int):
        return self._data_frame.iloc[[row], [1, 2]]
    
    def get_df(self):
        return self._data_frame

    def get_df_training(self):
        original = self._data_frame.copy()
        self.remove_empties()
        self.remove_nans()
        processed = self._data_frame
        self._data_frame = original
        return processed
    
    def get_df_gs(self):
        '''
        Adds one empty row for each Category at
        beginning of each month, which ensures that
        averages per month are calculated correctly,
        without actually changing summing values
        '''
        temp_df = self._data_frame.copy()
        if temp_df.empty:
            raise ValueError("No DataFrame was selected...")   
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
        temp_df['Commit file'] = self._app.data_frame.get_bank_str()
        
        '''
        Flip df to chronological order
        for google sheets
        '''
        temp_df = temp_df.iloc[::-1]  
        return temp_df
        
      
    def remove_nans(self):
        self._data_frame = self._data_frame.dropna()
        
    def remove_empties(self):
        self._data_frame = self._data_frame[self._data_frame['Receiver'] != '']
        self._data_frame = self._data_frame[self._data_frame['Category'] != '']
              
    def update_category(self, row: int, category: str):
        self._data_frame.at[row, 'Category'] = category 
    
    def save_data(self):
        if self._data_frame.empty:
            raise MyWarningError("DataFrame could not be saved. \nNo frame selected...")
        if self._local_path is None:
            raise MyWarningError("DataFrame pulled from Google sheets\ncan not be saved localy!\nPath is unkown...")
        else:
            save_path = self._local_path.rsplit('.')[0]
            save_path += "_Labeled.csv"
            self._data_frame.to_csv(save_path, index=False, sep=',', encoding=self._encoding)    

    def set_data(self, df: pd.DataFrame):
        bank_file_type = self._detect_bank(df)
        df = self._transform2aidf(df, bank_file_type)
        self._local_path = None
        self._data_frame = df
        self._bank_file_type = bank_file_type
        self._encoding = None
        self._separator = ','
                
    def load_data(self, path: str):      
        try:  
            if not path.endswith('.csv'):
                raise TypeError("File type is not supported!\nOnly CSV files are allowed...")                     
            '''
            Load the file,
            determine the bank,
            transform to AIDF
            '''
            self._local_path = path
            df = self._auto_open_file(path)          
            bank_file_type = self._detect_bank(df)
            self._bank_file_type = bank_file_type
            df = self._transform2aidf(df, bank_file_type)
            self._data_frame = df                                  
        except Exception as e:
            msg = "Data could not be loaded!"
            raise MyWarningError(msg, e, fatal=False)

    def _auto_open_file(self, path: str) ->pd.DataFrame:
        '''
        Detect encoding
        '''     
        with open(path, 'rb') as csvFile:
            encoding_dict = chardet.detect(csvFile.read())
            encoding = encoding_dict['encoding']
        '''
        Detect separator
        '''  
        with open(path, 'r', encoding=encoding) as csvFile:
            dialect = csv.Sniffer().sniff(csvFile.read(), delimiters=[',', ';', '', '\t', '|'])
            separator = dialect.delimiter
        
        df = pd.read_csv(path, encoding=encoding, sep=separator)
        self._encoding = encoding
        self._separator = separator
        return df
        
    def _detect_bank(self, df: type[pd.DataFrame]) -> str:
        
        column_list = list(df.columns)

        if (len(column_list) == 4 and
            column_list[0] == 'Date' and
            column_list[1] == 'Receiver' and
            column_list[2] == 'Amount' and
            column_list[3] == 'Category'):
            return 'AIDF'
        
        elif (len(column_list) == 7 and
            column_list[0] == 'Date' and
            column_list[1] == 'Receiver' and
            column_list[2] == 'Amount' and
            column_list[3] == 'Category' and 
            column_list[4] == 'Category ID' and
            column_list[5] == 'Commit date' and
            column_list[6] == 'Commit file ID'):
            return 'AIDF_GS'
        
        elif (len(column_list) == 5 and
            column_list[0] == 'Päivämäärä' and
            column_list[1] == 'Saaja/Maksaja' and
            column_list[2] == 'Selite' and
            column_list[3] == 'Viite/Viesti' and
            column_list[4] == 'Määrä'):
            return 'POP_BANK'
        
        #elif (Your file detection code):
            #return 'YourBankCSV'       
        else:
            raise TypeError("The Bank is not supported...")
        
                  
    def _transform2aidf(self, df: type[pd.DataFrame], bank_file_type : str) -> type[pd.DataFrame]:                      
        if bank_file_type == 'AIDF':
            df = df.fillna("")
            
        elif bank_file_type == 'AIDF_GS':
            df = df.drop(['Category ID', 'Commit date', 'Commit file ID'], axis=1)
            df = df.astype({'Date':'string','Receiver':'string','Amount':'float','Category':'string'})
            df = df.fillna("")
        
        elif bank_file_type == 'POP_BANK':       
            df = df.rename({'Päivämäärä': 'Date', 
                            'Saaja/Maksaja': 'Receiver', 
                            'Määrä': 'Amount'}, axis=1)      
            df = df.drop(['Selite', 'Viite/Viesti'], axis=1)
            df["Category"] = ""
            df['Amount'] = df['Amount'].str.replace(',', '.')
            df = df.astype({'Amount': 'float'})
            df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
            df['Date'] = df['Date'].dt.date.astype(str)
            df = df.fillna("")           
        
        #if file_type == 'YourBankCSV':
            #Your transform code goes here...         
        return df
                         
        
        
            
            