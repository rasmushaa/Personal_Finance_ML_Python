'''
Created on 7 Sep 2022

@author: rhaapaniemi
'''




from    app_functions                           import  DataFrame
import                                                  pandas as pd
import                                                  seaborn as sns
import                                                  matplotlib.pyplot as plt
from    sklearn.compose                         import  ColumnTransformer
from    sklearn.feature_extraction.text         import  CountVectorizer
from    sklearn.feature_selection               import  mutual_info_classif
from    skfeature.function.similarity_based     import  fisher_score
from    sklearn.feature_selection               import  SelectKBest, chi2


'''
Data features can be studied in this module,
and use to alter the model training function.
Data is loaded from the path and transformed to used format
in the app_functions.DataFrame.load_data(), which may be
extended to accept new file formats for your own purposes.
'''



DATA_PATH = "/Users/rasmus/Desktop/2022_Labeled.csv"


print("============ USED DATA SET =============")
df = DataFrame()
df.load_data(DATA_PATH )
print(df.get_info_str())


print("============== DATA EFTER REMOVING NaNs ===============")
df.remove_nans()
print(df.get_info_str())



print("============ X, y and X_cat =============")

'''
Factorising running number variables
'''
dataset = df.get_df()
dataset['Day of Month'] = dataset.iloc[:,0].astype('datetime64[ns]').dt.day
dataset['Day of Week']  = dataset.iloc[:,0].astype('datetime64[ns]').dt.dayofweek
dataset.loc[dataset['Day of Week'] >= 5, 'Weekend bool'] = 1
dataset.loc[dataset['Day of Week'] <  5, 'Weekend bool'] = 0
dataset.loc[dataset['Day of Month'] < 35, 'Quarter of Month'] = 3
dataset.loc[dataset['Day of Month'] < 24, 'Quarter of Month'] = 2
dataset.loc[dataset['Day of Month'] < 16, 'Quarter of Month'] = 1
dataset.loc[dataset['Day of Month'] <  8, 'Quarter of Month'] = 0
dataset.loc[dataset.iloc[:,2] <  0, 'Amount sign'] = 1
dataset.loc[dataset.iloc[:,2] >= 0, 'Amount sign'] = 0

X = dataset[['Day of Month', 'Day of Week', 'Amount']]
print('Shape of the X: ' + str(X.shape) + " (Rows, Columns)")
print(X.head(10))

dataset['Class']  = pd.factorize(dataset.iloc[:,3])[0]
y = dataset['Class']
print('\nShape of the y: ' + str(y.shape) + " (Rows, Columns)")
print(y.head(10))

X_cat = dataset[['Receiver', 'Quarter of Month', 'Weekend bool', 'Amount sign']]
print('\nShape of the X_cat: ' + str(X_cat.shape) + " (Rows, Columns)")
print(X_cat.head(10))
print("\n\n\n\n")




'''
Plot frequency of classes
'''
fig = plt.figure(figsize=(8,6))
dataset['Category'].value_counts().plot.bar(ylim=0, color="green", rot=45)
plt.title('Class frequencies')
plt.show()


'''
Correlation
'''
corr = dataset[['Day of Month', 
                'Day of Week', 
                'Quarter of Month', 
                'Weekend bool', 
                'Amount sign', 
                'Amount', 
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
