'''
Created on 19 Aug 2022

@author: rasmus
'''




from app import Application
from utilis import MyWarningError
import json
import sys
import os
import traceback
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from threading import Thread

FILE = "settings.json"
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
FILE_PATH = os.path.join(ROOT_DIR, "gui", FILE)



class GUI(TkinterDnD.Tk, tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.app = Application()
        with open(FILE_PATH, 'r') as f:
            self.settings = json.load(f)
        self.title(self.settings['title'])
        self.geometry(self.settings['window'])                 
        self.front_page = FrontPage(parent=self, application=self.app)
        
        
    '''
    All exceptions will be shown here 
    and system may be exited
    '''
    def report_callback_exception(self, exctype, excvalue, tb):          
        if isinstance(excvalue, MyWarningError):
            messagebox.showwarning('Warning', str(excvalue))
            if excvalue.fatal:
                sys.exit()
        else:    
            msg = ('An uncaught exception has occurred!\n\n' 
                   + str(excvalue) 
                   + '\n\n\n' 
                   + '\n'.join(traceback.format_tb(tb, limit=-1)))
            messagebox.showerror('Error', msg)
            sys.exit()

    '''
    Save GUI state
    and exit all.
    '''
    def on_closing(self):
        with open(FILE_PATH, 'w') as f:
            self.settings['sheet_name'] = self.front_page.entry_box_sheet.get()
            self.settings['private_key'] = self.front_page.entry_box_key.get()
            self.settings['window'] = self.winfo_geometry()
            json.dump(self.settings, f)
        self.destroy()
        
        
    
'''
All windows will be on this
'''
class FrontPage():
    def __init__(self, parent, application):
        self.gui = parent
        self.app = application
                
        '''
        GOOGLE CLOUD AUTH
        '''
        labelframe = tk.LabelFrame(self.gui, 
                                   text="Google cloud authentication")
        labelframe.grid(row=0, column=0, sticky='ew', padx=(20, 10), pady=10)      
        self.gui.grid_columnconfigure(0, weight=1)
        # Entry labels   
        l1 = tk.Label(labelframe, text = "Sheet")
        l2 = tk.Label(labelframe, text = "Key")         
        l1.grid(row=0, column=0, sticky='w', ipadx=2)
        l2.grid(row=1, column=0, sticky='w', ipadx=2)   
        labelframe.grid_columnconfigure(0, weight=0)        
        # Entry boxes
        self.entry_box_sheet = tk.Entry(labelframe,)
        self.entry_box_sheet.insert(0, self.gui.settings['sheet_name'])
        self.entry_box_key = tk.Entry(labelframe)
        self.entry_box_key.insert(0, self.gui.settings['private_key'])       
        self.entry_box_sheet.grid(row=0, column=1, sticky='ew', padx=10, pady=7)
        self.entry_box_key.grid(row=1, column=1, sticky='ew', padx=10, pady=9)      
        labelframe.grid_columnconfigure(1, weight=1)
        # SAVE BUTTONS
        labelframe = tk.LabelFrame(self.gui, text="Save")
        labelframe.grid(row=0, column=1, padx=(10, 20), pady=10)      
        self.gui.grid_columnconfigure(1, weight=0)    
        # Check button
        self.check_bool_1 = tk.IntVar()
        self.check_button_1 = tk.Checkbutton(labelframe, 
                                             text = "Local save", 
                                             variable = self.check_bool_1)
        self.check_button_1.grid(row=0, column=0)
        # Save button
        self.save_button = tk.Button(labelframe, 
                                     text='Save',
                                     font=("arial bold", 18), 
                                     command=self.save_button_action,
                                     height = 2,
                                     width  = 6)
        self.save_button.grid(row=1, column=0, padx=10, pady=5)      
        
        '''
        AI SETTINGS
        '''
        labelframe = tk.LabelFrame(self.gui, text="AI")
        labelframe.grid(row=1, column=0, columnspan=2, sticky='ew', padx=20, pady=0)     
        # Check button
        self.check_bool_2 = tk.IntVar()
        self.check_button_2 = tk.Checkbutton(labelframe, 
                                             text = "Use AI",
                                             pady = 0, 
                                             variable = self.check_bool_2)
        self.check_button_2.grid(row=0, column=0, pady=(0, 4))
        self.check_button_2.select()
        # Slider
        self.slider_label = tk.Label(labelframe, width=4)
        self.slider_value = tk.IntVar()       
        def slider_label_update(a, b, c):
            self.slider_label["text"] = "{:3d}%".format(self.slider_value.get())         
        self.slider_value.trace('w', slider_label_update)
        l1 = tk.Label(labelframe, text = "Prediction limit")
        self.slider = tk.Scale(labelframe, 
                               from_=0, 
                               to=100, 
                               orient='horizontal', 
                               variable=self.slider_value,
                               showvalue=0)
        self.slider.set(80)
        l1.grid(row=0, column=2, sticky='w', padx=(5, 0), pady=(0, 4))
        self.slider.grid(row=0, column=2, sticky='ew')
        labelframe.grid_columnconfigure(2, weight=1)
        self.slider_label.grid(row=0, column=3, sticky='e', padx=(0, 5), pady=(0, 4))
        # TRAIN Button
        self.train_button = tk.Button(labelframe, 
                                     text="Train model",
                                     font=("arial", 15), 
                                     command=self.train_button_action,
                                     height = 1,
                                     width  = 7)
        self.train_button.grid(row=0, column=4, padx=5, ipady=2, ipadx=2, pady=(0, 5))
        # FILL Button
        self.auto_fill_button = tk.Button(labelframe, 
                                     text="Auto fill",
                                     font=("arial", 15), 
                                     command=self.fill_button_action,
                                     height = 1,
                                     width  = 4)
        self.auto_fill_button.grid(row=0, column=1, padx=5, ipady=2, ipadx=2, pady=(0, 5))
        
        '''
        CSV DATA
        '''
        self.data_table = DataTable(parent=self.gui, application=self.app)
        self.data_table.bind('<Right>', self.set_category_action)
        self.data_table.bind('<Down>', self.scrolling_pad_action)
        self.data_table.bind('<Double-1>', self.set_category_action)
        self.data_table.bind('<<TreeviewSelect>>', self.predict_category_action)     
        self.data_table.drop_target_register(DND_FILES)
        self.data_table.dnd_bind('<<Drop>>', self.drop_files_action)   
        self.data_table.grid(row=2, column=0, columnspan=2, sticky='nesw', padx=20, pady=20)
        self.gui.grid_rowconfigure(2, weight=1)    
   
        
    '''
    Action handles
    '''
    def drop_files_action(self, event):
        file_path = event.data
        self.app.data_frame.load_data(file_path)
        self.data_table.init_table(self.app.data_frame.get_df())

    
    def set_category_action(self, event):
        self.data_table.set_category(event)
        
    def scrolling_pad_action(self, event):
        self.data_table.scrolling_pad(event)
    
    def predict_category_action(self, event):       
        if self.check_bool_2.get() and self.app.ai.seted_up():
            row_values = self.data_table.get_row_values()
            if len(row_values) and row_values[-1] == "":  # Check if category is already chosen
                row_id_str = self.data_table.get_row_id_str()
                X = self.app.data_frame.get_x_features_row(int(row_id_str))
                probas = self.app.ai.predict_proba(X)
                if probas[0] > self.slider_value.get()/100:
                    categories = self.app.ai.predict_category(X)
                    self.data_table.update_row(row_id_str, categories[0])
                    
    def fill_button_action(self):
        if not self.app.data_frame.get_df().empty:
            X = self.app.data_frame.get_x_features()
            categories = self.app.ai.predict_category(X)
            probas = self.app.ai.predict_proba(X)      
            for i, category in enumerate(categories):
                if probas[i] > self.slider_value.get()/100:
                    self.data_table.update_row(str(i), category)
           
    def save_button_action(self):
        local_save_bool = self.check_bool_1.get()      
        if local_save_bool:
            self.app.data_frame.save_data()
        else:
            key = self.entry_box_key.get()
            gogle_sheet = self.entry_box_sheet.get()
            self.app.google_api.auth(key)
            self.app.google_api.write_to_cloud(gogle_sheet)

    def train_button_action(self):
        t1 = Thread(target=self.worker)
        t1.start()

    def worker(self):
        try:
            key = self.entry_box_key.get()
            gogle_sheet = self.entry_box_sheet.get()
            self.app.google_api.auth(key)
            training_data = self.app.google_api.get_from_cloud(gogle_sheet)
            training_data = training_data.drop(['Category ID', 'Commit date', 'Commit file ID'], axis=1)
            training_data = training_data[training_data['Receiver'] != '']
            training_data = training_data.fillna("")
            train = True
        except:
            train = messagebox.askyesno('Confirmation', 
                                        "Failed to get training data from Google Sheets!\nProceed anyway?",
                                        icon='warning')
            training_data = self.app.data_frame.get_df()

        if train is True:
            self.train_button['state'] = 'disabled'
            score = self.app.ai.train_model(training_data)
            info_str = ("A new AI model created succesfully" +
                        "\nAn overall accuracy of {:0.2f}% was achieved!".format(score*100))
            messagebox.showinfo('Info', info_str)
            self.train_button['state'] = 'normal'
                
        
'''
Shows CSV data in Treeview table
'''
class DataTable(ttk.Treeview):
    def __init__(self, parent: type[GUI], application: type[Application]):
        super().__init__()
        self.gui = parent
        self.app = application
        scroll_Y = tk.Scrollbar(self, orient='vertical', command=self.yview)
        self.configure(yscrollcommand=scroll_Y.set)
        scroll_Y.pack(side='right', fill='y')

    def init_table(self, dataframe: type[pd.DataFrame]):     
        self.delete(*self.get_children())        
        columns = list(dataframe.columns)
        self.__setitem__('column', columns)
        self.__setitem__('show', 'headings')

        for col in columns:
            self.heading(col, text=col)            
            if col == "Date":
                self.column(col, minwidth=0, width=self.gui.settings['width_date'], stretch='NO')
            elif col == "Receiver":
                self.column(col, minwidth=0, width=self.gui.settings['width_rec'], stretch='NO')
            elif col == "Amount":
                self.column(col, minwidth=0, width=self.gui.settings['width_amount'], stretch='NO')
            elif col == "Category":
                self.column(col, minwidth=0, width=self.gui.settings['width_cat'], stretch='YES')

        df_rows = dataframe.to_numpy().tolist()
        for i, row in enumerate(df_rows):
            self.insert("", 'end', iid=i, values=row) 
                
    def get_row_id_str(self):
        row_id_str = self.focus()
        return row_id_str
      
    def get_row_values(self):
        row_id_str = self.get_row_id_str()
        values = self.item(row_id_str)['values']
        return values         
            
    def set_category(self, event):
        row_id_str = self.get_row_id_str() 
        row = int(row_id_str)
        x, y, width, height = self.bbox(row, 3)  # 3 is the category
        
        self.list_popup = ListPopup(parent=self, row_id_str=row_id_str, application=self.app)
        self.list_popup.pack()    
        self.list_popup.place(y=y, x=x, width=width-20)     
        self.list_popup.update()

        if y + self.list_popup.winfo_height() > self.winfo_height():  # if the popup box does not fit, place it above row
            y -= int(self.list_popup.winfo_height() * ((self.list_popup.size()-1) / self.list_popup.size()))
            self.list_popup.place(y=y, x=x, width=width-20)
                                        
    def update_row(self, row_id_str: str, category: str):
        new_values = self.item(row_id_str)['values']
        row = int(row_id_str)
        new_values[-1] = category  # Last element of treeview is the new category
        self.item(row_id_str, values=new_values)
        self.app.data_frame.update_category(row, category)   
               
    def scrolling_pad(self, event):
        row_id_str = self.get_row_id_str() 
        row_pad = int(row_id_str) + len(self.app.categories.expenditures)
        if row_pad < len(self.get_children()):
            self.see(str(row_pad))
            
            
'''
POP Up list BOX
'''
class ListPopup(tk.Listbox):
    def __init__(self, parent: type[DataTable], row_id_str: str, application: type[Application], **kw):
        super().__init__(parent, **kw)
        self.data_table = parent
        self.row_id_str = row_id_str
        self.app = application

        transaction_value = self.app.data_frame.get_df()["Amount"].iloc[int(self.row_id_str)]
        if transaction_value > 0:
            category_types = list(self.app.categories.incomes.values())
        else:
            category_types = list(self.app.categories.expenditures.values())            
        tk_category_types = tk.StringVar(value=category_types)
   
        self.config(listvariable=tk_category_types, 
                    background='skyblue4', 
                    foreground='white', 
                    font=('Aerial 13'), 
                    height=len(category_types)) 
           
        self.selection_set( first = 0 )
        self.bind('<Return>', self.onReturn)
        self.bind('<Double-1>', self.onReturn)
        self.bind('<FocusOut>', self.onFocusOut) 
        self.bind('<Left>', self.onFocusOut)
        self.focus_set()
        
    def onFocusOut(self, event):
        self.data_table.focus_set()
        self.destroy()
        
    def onReturn(self, event):
        self.data_table.focus_set()
        category = self.get(self.curselection())
        self.data_table.update_row(self.row_id_str, category)
        self.destroy()

      
            