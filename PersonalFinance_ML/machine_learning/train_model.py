'''
Created on 6 Sep 2022

@author: rhaapaniemi
'''




from app_functions                      import  DataFrame
import                                          pandas  as pd
import                                          numpy   as np
import                                          os
import                                          joblib
from pprint                             import  pprint
from sklearn.model_selection            import  train_test_split
from sklearn.model_selection            import  RandomizedSearchCV
from sklearn.feature_selection          import  SelectKBest, chi2
from sklearn.feature_extraction.text    import  CountVectorizer
from sklearn.pipeline                   import  Pipeline
from sklearn.compose                    import  ColumnTransformer
from sklearn.ensemble                   import  RandomForestClassifier
from sklearn.metrics                    import  accuracy_score




DATA_PATH           = "/Users/rasmus/Desktop/2022_Labeled.csv"
RANDOM_SEARCH_N     = 500
CROSS_VALIDATION    = 3
SAVE_MODEL          = True
MODEL_NAME          = "trained_model.pkl"




print("============== USED DATA SET ===============")
df = DataFrame()
df.load_data(DATA_PATH)
print(df.get_info_str())



print("============== DATA EFTER REMOVING NaNs ===============")
df.remove_nans()
print(df.get_info_str())



print("============ SPLITTING DATA TO TRAIN AND TEST =============")
dataset = df.get_df()
training_data = dataset.iloc[:, [1, 2]]
class_data = dataset.iloc[:, 3]
X_train, X_test, y_train, y_test = train_test_split(training_data, class_data, 
                                                    test_size=0.2, 
                                                    random_state=21, 
                                                    stratify=class_data)

print("Training X:" + str(X_train.shape) + " y:" + str(y_train.shape) + " (Rows, Columns)")
print("Testing  X:" + str(X_test.shape) + " y:" + str(y_test.shape) + " (Rows, Columns)")
print("\nHead of training X:")
print(X_train.head(10))
print("\nHead of training y:")
print(y_train.head(10))
print("\n\n\n\n")



# ===================== PIPELINE ===========================
'''
Text vectorizer
'''  
text_transformer = Pipeline(
    steps=[
       ('textVectorizer', CountVectorizer()),
       ('wordBankDimRed', SelectKBest(chi2, k='all'))
    ]
)
'''
Preprocessor of pipeline
'''
preprocessor = ColumnTransformer(
   transformers=[
       ('textTransformer', text_transformer, 0)
       
    ], remainder = 'passthrough'
) 
'''
Head of pipeline
'''
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ('randomForest', RandomForestClassifier())
    ]
)



print("============ FITTING THE MODEL =============")

print("Used pipeline:")
model_pipeline = pipeline
print (model_pipeline)


# ======================= HYPERPARAMETERS TO BE TESTED ==========================
'''
Fitting functions tests randomly some of theses hyperparameters to find 
the best model. Changes can be made according to the "Best found parameters:"
''' 
n_estimators        = [int(x) for x in np.linspace(start = 1, stop = 120, num = 120)]
max_depth           = [int(x) for x in np.linspace(1, 50, num = 50)]
min_samples_split   = [int(x) for x in np.linspace(1, 20, num = 20)]
min_samples_leaf    = [int(x) for x in np.linspace(1, 10, num = 10)]
bootstrap           = [True, False]
chi2_k              = [int(x) for x in np.linspace(start = 50, stop = 200, num = 150)]


random_grid =  {'randomForest__n_estimators': n_estimators,
                'randomForest__max_depth': max_depth,
                'randomForest__min_samples_split': min_samples_split,
                'randomForest__min_samples_leaf': min_samples_leaf,
                'randomForest__bootstrap': bootstrap,
                'preprocessor__textTransformer__wordBankDimRed__k': chi2_k}


print("\nFitting the base model...")
base_model = model_pipeline
base_model.fit(X_train, y_train)

print("Fitting the model with random hyper parameters...")
tuned_model = RandomizedSearchCV(estimator=model_pipeline, 
                               param_distributions=random_grid, 
                               n_iter=RANDOM_SEARCH_N, 
                               cv=CROSS_VALIDATION, 
                               verbose=1, 
                               random_state=42, 
                               n_jobs =-1)

tuned_model.fit(X_train, y_train)
best_model = tuned_model.best_estimator_
print("\nBest found parameters:")
pprint(tuned_model.best_params_)
print("\n\n\n\n")






print("============ VALIDATING CLASSIFIER =============")
def evaluate(model, test_features, test_labels):
    y_pred = model.predict(test_features)
    print(pd.crosstab(test_labels, y_pred, rownames=['Actual\u2193'], colnames=['Predicted\u2192']))
    accuracy = accuracy_score(test_labels, y_pred) 
    print('\nAccuracy {:0.2f}%.'.format(100*accuracy))
    return accuracy


print("Base model:")
base_accuracy = evaluate(base_model, X_test, y_test)

print("\nTuned model:")
random_accuracy = evaluate(best_model, X_test, y_test)

print('\nImprovement of {:0.2f}%.'.format( 100 * (random_accuracy - base_accuracy) / base_accuracy))



if SAVE_MODEL:
    
    ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    FILE = os.path.join(ROOT_DIR, 'files', MODEL_NAME)

    with open(FILE , 'wb') as file:
        joblib.dump(best_model, file)
        print("\nModel saved as: " + MODEL_NAME + " to files-folder")


