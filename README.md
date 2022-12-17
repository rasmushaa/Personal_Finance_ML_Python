# Personal_Finance_ML_Python
This is a small python program with a GUI, intended to automate Banking file
parsing, using ML. You are able to extend the usage to include your own csv-files
with little work. The data is analysed using free Google drive Sheets and Data studio in the cloud. 
All files can freely be copied using the links below.
Although, using AI finance localy is also possible and data can be plotted, for example, in Excell.
You may also see this functionality demonstration: https://www.youtube.com/watch?v=gjR14kTgweA&t=54s


<img src="https://github.com/rasmushaa/Personal_Finance_ML_Python/blob/master/git_images/app.png" width="500">

<img src="https://github.com/rasmushaa/Personal_Finance_ML_Python/blob/master/git_images/dashboard.png" width="500">

<img src="https://github.com/rasmushaa/Personal_Finance_ML_Python/blob/master/git_images/drive.png" width="500">


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

## How to build an Exe
It is possible to build a standalone executeable file, using the PyInstaller librarym which is included in the Conda environment. 
However, for some reason, running Pyinstaller normally does not produce succesfull results on Mac mini M1 computer and needs a bit hacking.

1. Activate your virtual environment
2. Set you current folder to build/
3. Run command in terminal: 
```pyinstaller --windowed --collect-all tkinterdnd2 --add-data="/Users/you/build/brute_include/*:." --icon=logo.icns main.py```

This should generate working Application in build/dist. If it does not work, you can try to debugg using terminal version in /build/dist/main.
The command --collect-all tkinterdnd2 forces Pyinstaller to include file dragging library, used by Tkinter, whihch would other wise not be found. 
The brute_include/ folder has all same files as buid/, except the main.py. It is used to manually ensure that all files are included into the Application. For this reason, the folder structure of the project is changed to be flatt. Also, absolut paths to filse inside of the program must use sys._MEIPASS to find the path, however, this does not work when running files normally in Visual Studio, and thus, two separed version are needed. 
If you want to build your own version of AI finance, you must first verify the proper working of your code in IDE from the previous section, and after that, add the new file parsing functions to correct py files in buid/ and also to the build/brute_include/.




