'''
Created on 19 Aug 2022

@author: rasmus
'''




from    application     import  Application
from    utilis          import  MyWarningError
import                          sys
import                          traceback
import  pandas          as      pd
import  tkinter         as      tk
from    tkinter         import  ttk
from    tkinter         import  messagebox
from    tkinterdnd2     import  DND_FILES, TkinterDnD



class GUI(TkinterDnD.Tk, tk.Tk):
    def __init__(self):
        super().__init__()
        self.app = Application()
        self.title(self.app.settings.application.title)
        self.geometry(self.app.settings.application.window)       
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
            messagebox.showwarning('Warning', msg)
            sys.exit()
        
        
    
'''
All windows will be on this
'''
class FrontPage():
    def __init__(self, parent, application):
        self.gui = parent
        self.app = application
        
        '''
        Entry labels
        '''
        l1 = tk.Label(self.gui, text = "Google sheet")
        l2 = tk.Label(self.gui, text = "Google account key")     
        l1.grid(row=0, column=0, sticky='w', padx=10)
        l2.grid(row=1, column=0, sticky='w', padx=10)
        self.gui.grid_columnconfigure(0, weight=0)
        
        '''
        Entry boxes
        '''
        self.entry_box_sheet = tk.Entry(self.gui)
        self.entry_box_sheet.insert(0, self.app.settings.google_api.default_sheet)
        self.entry_box_key = tk.Entry(self.gui)
        self.entry_box_key.insert(0, self.app.settings.google_api.default_key)
        self.entry_box_sheet.grid(row=0, column=1, sticky='ew', padx=10, pady=10)
        self.entry_box_key.grid(row=1, column=1, sticky='ew', padx=10)
        self.gui.grid_columnconfigure(1, weight=1)   
        
        '''
        Check buttons
        '''
        self.check_bool_1 = tk.IntVar()
        self.check_button_1 = tk.Checkbutton(self.gui, 
                                             text = "Local backup", 
                                             variable = self.check_bool_1)
        self.check_button_1.grid(row=0, column=2)
  
        '''
        Save button
        '''
        self.save_button = tk.Button(self.gui, 
                                     text='Save',
                                     font=("arial bold", 18), 
                                     command=self.save_button_action,
                                     height = 2,
                                     width  = 6)
        self.save_button.grid(row=1, column=2, padx=10)
        self.gui.grid_columnconfigure(2, weight=0)

        '''
        CSV data
        '''
        self.data_table = DataTable(parent=self.gui, application=self.app)
        self.data_table.bind("<Right>", self.data_table.set_category)
        self.data_table.bind("<Down>", self.data_table.scrolling_pad)
        self.data_table.bind("<Double-1>", self.data_table.set_category)
        self.data_table.bind("<<TreeviewSelect>>", self.predict_category_action)     
        self.data_table.drop_target_register(DND_FILES)
        self.data_table.dnd_bind("<<Drop>>", self.drop_files_action)   
        self.data_table.grid(row=3, column=0, columnspan=3, sticky='nesw', padx=20, pady=20)
        self.gui.grid_rowconfigure(3, weight=1)    
   
        
    '''
    Action handles
    '''
    def drop_files_action(self, event):
        file_path = event.data
        self.app.pf_dataFrame.load_data(file_path)
        self.data_table.init_table(self.app.pf_dataFrame.get_df())
           
    def save_button_action(self):
        key = self.entry_box_key.get()
        gogle_sheet = self.entry_box_sheet.get()
        local_save_bool = self.check_bool_1.get()
        
        if local_save_bool:
            self.app.pf_dataFrame.save_data()
        self.app.google_api.auth(key)
        self.app.google_api.write_to_cloud(gogle_sheet, self.app.pf_dataFrame.get_df())
        
    def predict_category_action(self, event):
        pass

        
        
        
'''
Shows CSV data in Treeview table
'''
class DataTable(ttk.Treeview):
    def __init__(self, parent: type[GUI], application: type[Application]):
        super().__init__()
        self.gui = parent
        self.app = application
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=scroll_Y.set)
        scroll_Y.pack(side="right", fill="y")


    def init_table(self, dataframe: type[pd.DataFrame]):     
        self.delete(*self.get_children())        
        columns = list(dataframe.columns)
        self.__setitem__("column", columns)
        self.__setitem__("show", "headings")

        for col in columns:
            self.heading(col, text=col)            
            if col == "Date":
                self.column(col, minwidth=0, width=100, stretch='NO')
            elif col == "Receiver":
                self.column(col, minwidth=0, width=250, stretch='NO')
            elif col == "Amount":
                self.column(col, minwidth=0, width=100, stretch='NO')
            elif col == "Category":
                self.column(col, minwidth=0, width=200, stretch='YES')

        df_rows = dataframe.to_numpy().tolist()
        for i, row in enumerate(df_rows):
            self.insert("", "end", iid=i, values=row)          
          
            
    def set_category(self, event):
        row_id_str = self.focus() 
        row = int(row_id_str)
        x, y, width, height = self.bbox(row, 3) #3 is the category
        
        self.list_popup = ListPopup(parent=self, row_id_str=row_id_str, application=self.app)
        self.list_popup.pack()    
        self.list_popup.place(y=y, x=x, width=width-20)     
        self.list_popup.update()

        # if the popup box does not fit, place it above row
        if y + self.list_popup.winfo_height() > self.winfo_height():
            y -= int(self.list_popup.winfo_height() * ((self.list_popup.size()-1) / self.list_popup.size()))
            self.list_popup.place(y=y, x=x, width=width-20)
          
                                  
    def update_row(self, row_id_str: str, category: str):
        # get row of treeview
        new_values = self.item(row_id_str)['values']
        row = int(row_id_str)
        # last element of treeview is the new category
        new_values[-1] = category
        self.item(row_id_str, values=new_values)
        self.app.pf_dataFrame.update_category(row, category)   
        
        
    def scrolling_pad(self, event):
        row_id_str = self.focus() 
        row_pad = int(row_id_str) + len(self.app.settings.transaction_types.expenditure_list)
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

        # Select income or expense
        transaction_value = self.app.pf_dataFrame.get_df()['Amount'].iloc[int(self.row_id_str)]
        if transaction_value > 0:
            category_types = list(self.app.settings.transaction_types.income_list.values())
        else:
            category_types = list(self.app.settings.transaction_types.expenditure_list.values())            
        tk_category_types = tk.StringVar(value=category_types)
   
        self.config(listvariable=tk_category_types, 
                    background="skyblue4", 
                    foreground="white", 
                    font=('Aerial 13'), 
                    height=len(category_types)) 
           
        self.selection_set( first = 0 )
        self.bind("<Return>", self.onReturn)
        self.bind("<Double-1>", self.onReturn)
        self.bind("<FocusOut>", self.onFocusOut) 
        self.bind("<Left>", self.onFocusOut)
        self.focus_set()
        
    def onFocusOut(self, event):
        self.data_table.focus_set()
        self.destroy()
        
    def onReturn(self, event):
        self.data_table.focus_set()
        category = self.get(self.curselection())
        self.data_table.update_row(self.row_id_str, category)
        self.destroy()



            





            
            
            