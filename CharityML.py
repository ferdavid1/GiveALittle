# Import libraries necessary for this project
import numpy as np
import pandas as pd
from time import time
from IPython.display import display # Allows the use of display() for DataFrames

# Import supplementary visualization code visuals.py
import visuals as vs

# Pretty display for notebooks
#%matplotlib inline

# Load the Census dataset
data = pd.read_csv("census.csv")

# Success - Display the first record
#display(data.head(n=1))
n_records = len(data)

# TODO: Number of records where individual's income is more than $50,000
n_greater_50k = len(data[data['income']== ">50K"])

# TODO: Number of records where individual's income is at most $50,000
n_at_most_50k = len(data[data['income'] == "<=50K"])

# TODO: Percentage of individuals whose income is more than $50,000
greater_percent = n_greater_50k/n_records

# print ("Total number of records: {}".format(n_records))
# print ("Individuals making more than $50,000: {}".format(n_greater_50k))
# print ("Individuals making at most $50,000: {}".format(n_at_most_50k))
# print ("Percentage of individuals making more than $50,000: {:.2f}%".format(greater_percent))

# Split the data into features and target label
income_raw = data['income']
features_raw = data.drop('income', axis = 1)

# Log-transform the skewed features
skewed = ['capital-gain', 'capital-loss']
features_raw[skewed] = data[skewed].apply(lambda x: np.log(x + 1))

# Import sklearn.preprocessing.StandardScaler
from sklearn.preprocessing import MinMaxScaler

# Initialize a scaler, then apply it to the features
scaler = MinMaxScaler()
numerical = ['age', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
features_raw[numerical] = scaler.fit_transform(data[numerical])

# Show an example of a record with scaling applied
#display(features_raw.head(n = 1))

# from sklearn.preprocessing import OneHotEncoder

# ohe = OneHotEncoder()

# onehotlabels = ohe.fit_transform(features_raw)
# that was one way to encode
# this is another (easier)

# TODO: One-hot encode the 'features_raw' data using pandas.get_dummies()
features = pd.get_dummies(features_raw)

# TODO: Encode the 'income_raw' data to numerical values
income = income_raw.replace(["<=50K", ">50K"], [0,1])

# Print the number of features after one-hot encoding
encoded = list(features.columns)
print ("{} total features after one-hot encoding.".format(len(encoded)))

# Uncomment the following line to see the encoded feature names
#print (encoded)

# Import train_test_split
from sklearn.cross_validation import train_test_split

# Split the 'features' and 'income' data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, income, test_size = 0.2, random_state = 0)

# Show the results of the split
print ("Training set has {} samples.".format(X_train.shape[0]))
print ("Testing set has {} samples. \n".format(X_test.shape[0]))
#print(len(X_train[:300]))

from sklearn.metrics import recall_score as recall
from sklearn.metrics import precision_score as precision
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
#from sklearn.svm import SVC
# from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.ensemble import AdaBoostClassifier
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.linear_model import SGDClassifier
# from sklearn.linear_model import LogisticRegression
#import xgboost as xgb
#from xgboost.sklearn import XGBClassifier

clf = GradientBoostingClassifier()
#clf = XGBClassifier(learning_rate = 0.1, n_estimators=1000, max_depth=4, min_child_weight=6, gamma=0, subsample=0.8, nthread=4, seed=27)
clf.fit(X_train, y_train)
precision = precision(y_test,clf.predict(X_test)) #calculate precision

recall = recall(y_test,clf.predict(X_test)) # calculate recall

# TODO: Calculate accuracy

accuracy = accuracy_score(y_test, clf.predict(X_test))

from sklearn.metrics import fbeta_score, accuracy_score
# TODO: Calculate F-score using the formula above for beta = 0.5: (1+b^2)*((precision*recall)/((b^2*precision)+recall)
fscore = (1.25)*((precision*recall)/((.25*precision)+recall))

# alternative -> print(fbeta_score(y_test, clf.predict(X_test), beta=0.5))
# Print the results 
#print ("Naive Predictor: [Accuracy score: {}, F-score: {}]".format(accuracy, fscore))

# TODO: Import two metrics from sklearn - fbeta_score and accuracy_score


# def train_predict(learner, sample_size, X_train, y_train, X_test, y_test): 
#     '''
#     inputs:
#        - learner: the learning algorithm to be trained and predicted on
#        - sample_size: the size of samples (number) to be drawn from training set
#        - X_train: features training set
#        - y_train: income training set
#        - X_test: features testing set
#        - y_test: income testing set
#     '''
    
#     results = {}
    
#     # TODO: Fit the learner to the training data using slicing with 'sample_size'
#     start = time() # Get start time
#     learner.fit(X_train[:int(sample_size)], y_train[:int(sample_size)])
#     end = time() # Get end time
    
#     # TODO: Calculate the training time
#     results['train_time'] = end - start
        
#     # TODO: Get the predictions on the test set,
#     #       then get predictions on the first 300 training samples
#     start = time() # Get start time
#     predictions_test = learner.predict(X_test)
#     predictions_train = learner.predict(X_train[:300])
#     end = time() # Get end time
    
#     # TODO: Calculate the total prediction time
#     results['pred_time'] = end-start
            
#     from sklearn.metrics import accuracy_score
#     # TODO: Compute accuracy on the first 300 training samples
#     results['acc_train'] = accuracy_score(y_train[:300], predictions_train)
        
#     # TODO: Compute accuracy on test set
#     results['acc_test'] = accuracy_score(y_test, predictions_test)
    
#     # TODO: Compute F-score on the the first 300 training samples
#     results['f_train'] = fbeta_score(y_train[:300], predictions_train, beta=.5)
        
#     # TODO: Compute F-score on the test set
#     results['f_test'] = fbeta_score(y_test, predictions_test, beta=.5)
       
#     # Success
#     print ("{} trained on {} samples.".format(learner.__class__.__name__, sample_size))
#     print ("Accuracy, F-Score on first 300 samples: {}, {}".format(results['acc_train'], results['f_train']))
#     print ("Accuracy, F-Score on test set: {}, {}".format(results['acc_test'], results['f_test']))
#     print ("Training time: {} seconds".format(results['train_time']))
#     print ("Time taken to predict: {} seconds \n".format(results['pred_time']))
#     # Return the results
#     return results

# # TODO: Import the three supervised learning models from sklearn
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.tree import DecisionTreeClassifier

# # TODO: Initialize the three models
# clf_A = RandomForestClassifier()
# clf_B = GradientBoostingClassifier()
# clf_C = DecisionTreeClassifier()

# # TODO: Calculate the number of samples for 1%, 10%, and 100% of the training data

# samples_1 = len(X_train)*.01
# samples_10 = len(X_train)*.1
# samples_100 = len(X_train)

# # Collect results on the learners
# results = {}
# for clf in [clf_A, clf_B, clf_C]:
#     clf_name = clf.__class__.__name__
#     results[clf_name] = {}
#     for i, samples in enumerate([samples_1, samples_10, samples_100]):
#         results[clf_name][i] = \
#         train_predict(clf, samples, X_train, y_train, X_test, y_test)

# Run metrics visualization for the three supervised learning models chosen
#vs.evaluate(results, accuracy, fscore)

# TODO: Import 'GridSearchCV', 'make_scorer', and any other necessary libraries
from sklearn.grid_search  import GridSearchCV
from sklearn.metrics import make_scorer

# TODO: Initialize the classifier
clf = GradientBoostingClassifier()

# TODO: Create the parameters list you wish to tune
#parameters = {'n_estimators':[100,500], 'max_depth':[1,10], 'subsample':[0.8,0.9,1], 'max_features':["auto","log2","sqrt"]}
parameters = {'n_estimators':[100,200,300,400],'max_depth':[1,2,3,4,5,6,7,8,9,10]}
# TODO: Make an fbeta_score scoring object
scorer = make_scorer(fbeta_score, beta=0.5)

# TODO: Perform grid search on the classifier using 'scorer' as the scoring method
grid_obj = GridSearchCV(estimator=clf, param_grid=parameters, scoring=scorer, cv=5)

# TODO: Fit the grid search object to the training data and find the optimal parameters
grid_fit = grid_obj.fit(X_train, y_train)

# Get the estimator
best_clf = grid_fit.best_estimator_

# Make predictions using the unoptimized and model
predictions = (clf.fit(X_train, y_train)).predict(X_test)
best_predictions = best_clf.predict(X_test)

# Report the before-and-afterscores
print ("Unoptimized model\n------")
print ("Accuracy score on testing data: {:.4f}".format(accuracy_score(y_test, predictions)))
print ("F-score on testing data: {:.4f}".format(fbeta_score(y_test, predictions, beta = 0.5)))
print ("\nOptimized Model\n------")
print ("Final accuracy score on the testing data: {:.4f}".format(accuracy_score(y_test, best_predictions)))
print ("Final F-score on the testing data: {:.4f}".format(fbeta_score(y_test, best_predictions, beta = 0.5)))