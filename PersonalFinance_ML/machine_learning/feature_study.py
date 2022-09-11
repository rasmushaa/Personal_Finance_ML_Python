'''
Created on 7 Sep 2022

@author: rhaapaniemi
'''




import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import mutual_info_classif
from skfeature.function.similarity_based import fisher_score
from sklearn.feature_selection import SelectKBest, chi2


'''
USES PROCESSED AND LABELED DATA

    0                1                2            3
   'Date'           'Receiver'       'Amount'     'Category'
    str(DateTime)    str              float        str

'''



DATA_PATH           = "/Users/rasmus/Desktop/2022_Labeled.csv"
DATE_COLUMN         = 'Date'
TEXT_COLUMN         = 'Receiver'
AMOUNT_COLUMN       = 'Amount'
CLASS_COLUMN        = 'Category'




print("============== USED DATA SET ===============")
dataset = pd.read_csv(DATA_PATH)
print('Shape of the data set: ' + str(dataset.shape) + " (Rows, Columns)")
print(dataset.head(10))
print("\n\n")



print("============== ROWS WITH NaN ===============")
df_nan_check = dataset[dataset.isna().any(axis=1)]
print(df_nan_check)
dataset = dataset.dropna()
print('\nShape of the data after removing NaNs: ' + str(dataset.shape) + " (Rows, Columns)")
print("\n\n")


print("============ X, y and X_cat =============")

'''
Factorising running number variables
'''
dataset['Day of Month'] = dataset[DATE_COLUMN].astype('datetime64[ns]').dt.day
dataset['Day of Week'] = dataset[DATE_COLUMN].astype('datetime64[ns]').dt.dayofweek
dataset.loc[dataset['Day of Week'] >= 5, 'Weekend'] = 1
dataset.loc[dataset['Day of Week'] <  5, 'Weekend'] = 0
dataset.loc[dataset['Day of Month'] < 35, 'Month quarter'] = 3
dataset.loc[dataset['Day of Month'] < 24, 'Month quarter'] = 2
dataset.loc[dataset['Day of Month'] < 16, 'Month quarter'] = 1
dataset.loc[dataset['Day of Month'] <  8, 'Month quarter'] = 0
dataset.loc[dataset[AMOUNT_COLUMN] <  0, 'Amount sign'] = 1
dataset.loc[dataset[AMOUNT_COLUMN] >= 0, 'Amount sign'] = 0

X = dataset[['Day of Month', 'Day of Week', AMOUNT_COLUMN]]
print('Shape of the X: ' + str(X.shape) + " (Rows, Columns)")
print(X.head(20))

dataset['Class']  = pd.factorize(dataset[CLASS_COLUMN])[0]
y = dataset['Class']
print('\nShape of the y: ' + str(y.shape) + " (Rows, Columns)")
print(y.head(10))

X_cat = dataset[[TEXT_COLUMN, 'Month quarter', 'Weekend', 'Amount sign']]
print('\nShape of the X_cat: ' + str(X_cat.shape) + " (Rows, Columns)")
print(X_cat.head(10))
print("\n\n\n\n")




'''
Plot frequency of classes
'''
fig = plt.figure(figsize=(8,6))
dataset[CLASS_COLUMN].value_counts().plot.bar(ylim=0, color="green", rot=45)
plt.title('Class frequencies')
plt.show()


'''
Correlation
'''
corr = dataset[['Day of Month', 
                'Day of Week', 
                'Month quarter', 
                'Weekend', 
                'Amount sign', 
                AMOUNT_COLUMN, 
                'Class']].corr()
sns.heatmap(corr, cmap="Greens", annot=True)
plt.title('Correlation without words')
plt.show()



print("============ VECTORIZING TEXT =============")

transformer = ColumnTransformer(transformers=[('vec', CountVectorizer(), 0)], remainder = 'passthrough')
X_cat = transformer.fit_transform(X_cat)
vocabRaw = transformer.get_feature_names_out()
vocab    = [s.replace("vec__", "") for s in vocabRaw]
vocab    = [s.replace("remainder__",  "") for s in vocab]
X_cat = pd.DataFrame(X_cat.toarray(), columns = vocab)

print('Shape of the word bank: ' + str(X_cat.shape) + " (Rows, Columns)")
print(X_cat.head(10))



'''
Information gain
'''
importance = mutual_info_classif(X, y)
feat_importance = pd.Series(importance, X.columns)
feat_importance.plot(kind='barh', color='green')
plt.title('Information gain Numbers')
plt.show()


'''
Information gain text
'''
importance = mutual_info_classif(X_cat, y)
feat_importance = pd.Series(importance, X_cat.columns)
feat_importance.plot(kind='barh', color='green')
plt.title('Information gain Words')
plt.show()


'''
Fisher
'''
ranks = fisher_score.fisher_score(X.values, y.values)
feat_importance = pd.Series(ranks, X.columns)
feat_importance.plot(kind='barh', color='green')
plt.title('Fisher Score Numbers')
plt.show()


'''
Fisher text
'''
ranks = fisher_score.fisher_score(X_cat.values, y.values)
feat_importance = pd.Series(ranks, X_cat.columns)
feat_importance.plot(kind='barh', color='green')
plt.title('Fisher Score categorical values')
plt.show()

'''
chi2 categorical
'''
importance = chi2(X_cat, y)[0]
feat_importance = pd.Series(importance, X_cat.columns)
feat_importance.plot(kind='barh', color='green')
plt.title('Chi2 score of categorical values')
plt.show()


'''
chi2 top50
'''
selector = SelectKBest(chi2, k=50)
X_cat_best = selector.fit_transform(X_cat, y)
col_i = selector.get_support(indices=True)
importance = chi2(X_cat_best, y)[0]
feat_importance = pd.Series(importance, X_cat.columns[col_i])
feat_importance.plot(kind='barh', color='green')
plt.title('Chi2 score 50 bes words and categorical values')
plt.show()
