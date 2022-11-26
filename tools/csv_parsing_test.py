








import unittest
import os
import sys
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
FOLDER_PATH = os.path.join(ROOT_DIR, "src/")
sys.path.append(FOLDER_PATH)
from app import Application

'''
Change your own absolut path to your bankinf file!
'''
FILE_PATH = "/Users/rasmus/Ohjelmointi/visual_studio/AI_finance/tools/bank_testing_file.csv"
app = Application()
app.data_frame.load_data(FILE_PATH )
df = app.data_frame.get_df()

class TestFileParsing(unittest.TestCase):
    def test_column_len(self):
        columns = list(df.columns)
        self.assertEqual(len(columns), 4)

    def test_column_names(self):
        columns = list(df.columns)
        self.assertEqual(columns[0], 'Date')
        self.assertEqual(columns[1], 'Receiver')
        self.assertEqual(columns[2], 'Amount')
        self.assertEqual(columns[3], 'Category')

    def test_column_types(self):
        self.assertIsInstance(df.iloc[0][0], str)
        self.assertIsInstance(df.iloc[0][1], str)
        self.assertIsInstance(df.iloc[0][2], float)

    def test_datetime_str(self):
        date =  df.iloc[0][0]
        self.assertEqual(len(date), 10)
        self.assertEqual(date[4], '-')
        self.assertEqual(date[7], '-')

unittest.main()