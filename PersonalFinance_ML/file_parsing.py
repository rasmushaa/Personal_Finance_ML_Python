'''
Created on 9 Sep 2022

@author: rasmus
'''




from error_handling import MyWarningError
import pandas as pd
import chardet
import csv


'''
Automatically detects csv file encoding and separators
and transforms those to Personal Finance File -format
'''

'''
You may increase capabilities of the software 
by adding your own parser code here.
The transform2pff must output data in the format of:

    0                1                2            3
   'Date'           'Receiver'       'Amount'     'Category'
    str(DateTime)    str              float        NaN
    
    
'''

class MyFileParser():
            
    def transform2pff(self, file_path: str):
        
        try:    
            '''
            Auto detect encoding
            '''     
            with open(file_path, 'rb') as csvFile:
                encoding_dict = chardet.detect(csvFile.read(1000))
                encoding = encoding_dict['encoding']

            '''
            Auto detect separator
            '''  
            with open(file_path, 'r', encoding=encoding) as csvFile:
                dialect = csv.Sniffer().sniff(csvFile.read(1000), delimiters=[',', ';', '', '\t', '|'])
                separator = dialect.delimiter
          
            '''
            Load the file and
            determine the type
            '''
            df = pd.read_csv(file_path, encoding=encoding, sep=separator)           
            file_type = self._detect_type(df)
            
            
            '''
            Transform the file to PFF
            '''
            if file_type == 'PFF':
                pass
            
            elif file_type == 'POP_Bank':       
                df = df.rename({'Päivämäärä': 'Date', 
                                'Saaja/Maksaja': 'Receiver', 
                                'Määrä': 'Amount'}, axis=1)      
                df = df.drop(['Selite', 'Viite/Viesti'], axis=1)
                df["Category"] = ""
                df['Amount'] = df['Amount'].str.replace(',', '.')
                df = df.astype({'Amount': 'float'})
                df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
                df['Date'] = df['Date'].dt.date   
                              
            ''' if file_type == 'YouBankCSV':
                    Your transform code goes here...
            '''      
            return df
                         
        except Exception as e:
            msg = "Data could not be loaded!"
            raise MyWarningError(msg, e, fatal=False)
        
        
    def _detect_type(self, df) -> str:
        
        column_list = list(df.columns)
        
        if (len(column_list) == 4 and
            column_list[0] == 'Date' and
            column_list[1] == 'Receiver' and
            column_list[2] == 'Amount' and
            column_list[3] == 'Category'):
            return 'PFF'
        
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
        
        
            
            