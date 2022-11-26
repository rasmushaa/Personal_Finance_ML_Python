'''
Created on 5 Sep 2022

@author: rhaapaniemi
'''




from functionality import DataFrame
import joblib
import os
import timeit

DATA_PATH   = "/Users/rasmus/Desktop/2022_Labeled.csv"
MODEL_NAME  = "trained_model.pkl"
LIMIT       = 0.8

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
FILE = os.path.join(ROOT_DIR, 'files', MODEL_NAME)


'''
Trained model can be tested manually in this module.
Data is loaded from the path and transformed to used format
in the functionality.DataFrame.load_data(), which may be
extended to accept new file formats for your own purposes.
LIMIT shows you how curtain the model is about its predictions
'''


with open(FILE , 'rb') as file:
    model_pipeline = joblib.load(file)
    print("\n\n\nLoaded model: " + MODEL_NAME + "\n\n")
    
    
print("============ USED DATA SET =============")
df = DataFrame()
df.load_data(DATA_PATH )
print(df.get_info_str())


print("============== DATA EFTER REMOVING NaNs ===============")
df.remove_nans()
print(df.get_info_str())


print("============ TESTING X =============")
real_data = df.get_df()
X = real_data.iloc[:, [1, 2]]
print('Shape of the X: ' + str(X.shape) + " (Rows, Columns)")
print(X.head(10))
print("\n\n")


print("============ VALIDATING CLASSIFIER =============")

start   = timeit.default_timer()
y_pred  = model_pipeline.predict(X)
probas  = model_pipeline.predict_proba(X)
stop    = timeit.default_timer()

print("     Date:                           Receiver:    Amount:     Prediction:")

for i in range(len(y_pred)):    
    category = y_pred[i]
    if probas[i].max() < LIMIT:
        category = " "   
    print("%10s %35s %10.2f %15s" % (real_data.iloc[i][0], 
                                     real_data.iloc[i][1], 
                                     real_data.iloc[i][2], 
                                     category))
    
print("\n\nPredicted: {:d} types and threshold was: {:0.1f}".format(len(y_pred), LIMIT))
print("Total running time of predictions: {:f} seconds.".format(stop - start))


