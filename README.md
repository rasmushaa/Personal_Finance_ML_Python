# Personal_Finance_ML_Python
This is a small python program with a GUI, intended to automate Banking file
parsing, using ML. You are able to extend the usage to include your own csv-files
with little work. The overall project uses free Google drive Sheets and Data studio
to analyse the banking data in the cloud. All files can freely be copied using the links below.
Although, using AI finance localy is also possible and data can be plotted, for example, in Excell.

## How to install and run
1. Copy the Conda environment yaml.file
(Note, on ARM-Mac the terminal and conda must be X86 compatable,
the code is not tested on Windows, but it should work by default)
2. Run the main.py in src/
3. You can test AI finance using the testing_file.json in tools/
4. Make a copy from the Google sheets file in https://docs.google.com/spreadsheets/d/1N6VWUqoeCKhhXQ_HbCjpnZmo8Xuc5hbO1P1VtNcO3Gk/edit?usp=sharing
5. Make a Google service account and share your copy in (4), using these instructions https://www.youtube.com/watch?v=bu5wXjz2KvU&t=595s
6. Make a copy from Google Data Studio in https://datastudio.google.com/reporting/01b3b306-3c6e-469c-8144-187039841b75
7. The Data studio report asks you to replace exisiting data source with a new one. Provide corresponding worksheets from (4)
8. Using the private key from (5), you can push the test file into to (4), and use (6) to analyse the new data.


## How to extend AI finance to include your own bank
In src/app/functionality/file_parsing.py is a class DataFrame, which is responsible for parsing all inputed files everywhere in the repo. 
It has two mtehods: _detect_bank, and _transform2aidf. You must provide your bank type detection code and then transform the file into the AI-DataFame (aidf),
which is documentented in src/app/functionality/file_parsing.py. It is recommended to use unit testing file csv_parsing_test.py in tools/ 
to verify the proper working of your code.



