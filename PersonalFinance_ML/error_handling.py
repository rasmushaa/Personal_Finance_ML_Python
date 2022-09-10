'''
Created on 9 Sep 2022

@author: rasmus
'''


'''
A custom error, which prints occurred error
as user friendly format with a note.
Fatality modifies the printing and if true,
program will sys.exit() after throwing it.
'''

'''
Error is raise in try, except structure and additional
information is provided. All thrown errors are 
caught by tk.Tk.report_callback_exception() in
the main loop.
'''


class MyWarningError(Exception):

    def __init__(self, note: str, error: type[Exception], fatal: bool):       
        self.note       = note
        self.root_error = error
        self.fatal      = fatal


    def __str__(self):             
        error_class = self.root_error.__class__.__name__
        error_msg   = str(self.root_error)    
        if self.fatal:
            type = "A fatal error occurred!\n\n" 
        else:
            type = "Warning!\n\n"
        msg = type + self.note + '\n\n' + error_class + '\n' + error_msg        
        return msg
    
    
    