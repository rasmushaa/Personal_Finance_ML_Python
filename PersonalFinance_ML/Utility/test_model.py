'''
Created on 5 Sep 2022

@author: rhaapaniemi
'''




import pandas as pd
import joblib
import timeit

'''
USES PROCESSED UNLABELED DATA

    0                1                2            3
   'Date'           'Receiver'       'Amount'     'Category'
    str(DateTime)    str              float        NaN

'''

DATA_PATH           = "/Users/rasmus/Desktop/2022_Labeled.csv"
DATE_COLUMN         = 0
TEXT_COLUMN         = 1
AMOUNT_COLUMN       = 2
CLASS_COLUMN        = 3
MODEL_NAME          = "randomForest_pipeline.pkl_"



with open(MODEL_NAME , 'rb') as file:
    model_pipeline = joblib.load(file)
    print("\n\n\nLoaded model: " + MODEL_NAME + "\n\n")
    
    

print("============ USED DATA SET =============")
real_data = pd.read_csv(DATA_PATH)
print('Shape of the data set: ' + str(real_data.shape) + " (Rows, Columns)")
print(real_data.head(10))
print("\n\n")



print("============== ROWS WITH NaN ===============")
df_nan_check = real_data[real_data.isna().any(axis=1)]
print(df_nan_check)
real_data = real_data.dropna()
print('\nShape of the data after removing NaNs: ' + str(real_data.shape) + " (Rows, Columns)")
print("\n\n")


print("============ TESTING X =============")
X = real_data.iloc[:, [TEXT_COLUMN, AMOUNT_COLUMN]]
#X = X.rename(columns={'Saaja/Maksaja': 'Receiver', 'Määrä': 'Amount'})
print('Shape of the X: ' + str(X.shape) + " (Rows, Columns)")
print(X.head(10))
print("\n\n")


print("============ VALIDATING CLASSIFIER =============")

LIMIT = 0.8

start   = timeit.default_timer()
y_pred  = model_pipeline.predict(X)
probas  = model_pipeline.predict_proba(X)
stop    = timeit.default_timer()

print("     Date:                           Receiver:    Amount:     Prediction:")

for i in range(len(y_pred)):
    
    category = y_pred[i]
    if probas[i].max() < LIMIT:
        category = " "
    
    print("%10s %35s %10.2f %15s" % (real_data.iloc[i][DATE_COLUMN], 
                                     real_data.iloc[i][TEXT_COLUMN], 
                                     real_data.iloc[i][AMOUNT_COLUMN], 
                                     category))
    
print("\n\nPredicted: {:d} types and threshold was: {:0.1f}".format(len(y_pred), LIMIT))
print("Total running time of predictions: {:f}seconds.".format(stop - start))


