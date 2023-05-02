# -*- coding: utf-8 -*-
"""Copy of Ex_4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kaMBwdR5HqOsghMlIXtWG8BIzLTN5RBx

IMPORT LIBRARIES

*   In this example there are only libraries needed for the example code.
"""

from sklearn.datasets import load_digits 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline

"""READ THE DATA:

*   In this challenge you will use the dataset "Optical recognition of handwritten digits", usually indicated as Digits.

>     In the following example, how to load and read the info of this dataset, and visualize some of the samples.

"""

digits = load_digits()

print("Image Data Shape: ", digits.data.shape)
print("Label Data Shape: ", digits.target.shape)

plt.figure(figsize = (20, 4))
for index, (image, label) in enumerate(zip(digits.data[0:10], digits.target[0:10])):
  plt.subplot(1, 10, index + 1)
  plt.imshow(np.reshape(image, (8, 8)), cmap = plt.cm.gray)
  plt.title("Training: %i\n" % label, fontsize = 15)
  plt.axis("off")

"""FEATURE EXTRACTION

*   Transform the raw images into feature data:

>     To apply a classifier on the images, we can use the pixel values as features. We need to flatten the image and turn the data in a matrix with samples on the rows and features on the columns.
"""

n_samples = len(digits.images)
digits_data = digits.images.reshape((n_samples, -1))
digits_class = digits.target

"""FEATURE ENGINEERING AND TRAINING/TEST OF THE LEARNING MODEL

*   Evaluate if you need features normalization, feature selection or dimensionality reduction;
*   Find the best parameter for a classifier using a grid search approach applied on a stratified k-fold cross validation;
*   Evaluate the accuracy and the confusion matrix.


> Use these classifiers:

    *   SVM (different models and different kernels), see https://scikit-learn.org/stable/modules/svm.html
    *   Ensemble methods (e.g., RandomForest, AdaBoost, GradientBoosting, etc.), see https://scikit-learn.org/stable/modules/ensemble.html


  >> Which one is the best?

    *   Can you find a combination rule (e.g. majority voting, simple average, etc.) to build an ensemble of classifiers (e.g. decision trees, Naïve Bayes, etc.) with similar performances?
"""

#As an example in the following code lines there is a pipeline with standard scaler and linear SVM
  #where the C parameter is optimized with a grid search on a stratified cross validation

#As an example, let's fix some variables
n_values = 11
lower_value_C = -5
higher_value_C = 5

#Let's apply a stratified 10-fold cross validation
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# #Let's build a pipeline with only a scaler and a linear SVM
pipe = Pipeline([('scaler', StandardScaler()),('classifier',SVC(kernel='linear'))])


#Let's build a structure for the grid search with a set of parameters for the techniques in the pipeline
#Be careful to the double underscore between the name you chose in the pipeline and the name of the parameter
#Be careful also to the function logspace for the range of the C values
parameters={'classifier__C': np.logspace(lower_value_C, higher_value_C, num=n_values,base=10)}


#Let's apply the grid search function
grid_search = GridSearchCV(pipe, parameters, cv=cv)
#Let's train and test the learning system
grid_search.fit(digits_data, digits_class)

#Here we just print the best accuracy and the corresponding values for the parameters
print("The best parameters are %s with an accuracy of %0.4f"%(grid_search.best_params_, grid_search.best_score_))

"""**SVM STUDIES**"""

from sklearn import svm
from tqdm import tqdm
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, confusion_matrix


cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42) 


pipe = Pipeline([('scaler', StandardScaler()), ('pca', PCA()), ('svm', svm.SVC())]) 


parameters = {'pca__n_components': [10, 20, 30], 'svm__kernel': ['linear', 'poly', 'rbf', 'sigmoid'], 'svm__C': [0.05, 0.5, 1, 20, 200], 'svm__degree': [2, 3, 4, 5], 'svm__coef0': [-1, 0, 1],  'svm__gamma': ['scale', 'auto'] 
             }


grid_search = GridSearchCV(pipe, parameters, cv=cv, n_jobs=-1,verbose=1) 

grid_search.fit(digits_data, digits_class)


best_svm = grid_search.best_estimator_ 
y_pred = best_svm.predict(digits_data)

accuracy = accuracy_score(digits_class, y_pred)
confusion = confusion_matrix(digits_class, y_pred)

print("The best parameters are %s with an accuracy of %0.4f"%(best_svm, accuracy))
print(confusion)

from sklearn import svm
from sklearn.metrics import accuracy_score, confusion_matrix


cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

pipe = Pipeline([('scaler', StandardScaler()), ('pca', PCA()), ('svm', svm.NuSVC())])

parameters = {'svm__kernel': ['linear', 'poly', 'rbf', 'sigmoid'],'svm__nu': np.linspace(0.2, 0.5, 5),'svm__degree': [2, 3, 4, 5],'svm__coef0': [-1, 0, 1],'svm__gamma': ['scale', 'auto']}

grid_search = GridSearchCV(pipe, parameters, cv=cv, n_jobs=-1, verbose=2)

grid_search.fit(digits_data, digits_class)

# results evaluation
best_svm = grid_search.best_estimator_
y_pred = best_svm.predict(digits_data)

accuracy = accuracy_score(digits_class, y_pred)
confusion = confusion_matrix(digits_class, y_pred)

print("The best parameters are %s with an accuracy of %0.4f"%(best_svm, accuracy))
print(confusion)

"""**ENSEMBLE METHOD STUDIES**"""

# importing required libraries
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.naive_bayes import GaussianNB

# define ensemble models and parameters
models = [('rf', RandomForestClassifier()),
          ('ada', AdaBoostClassifier()),
          ('gb', GradientBoostingClassifier()),
          ('nb', GaussianNB())]

# set parameters
params = [{'pca__n_components': [20, 30, 40]},
          {'pca__n_components': [20, 30, 40], 'ada__n_estimators': [50, 100, 200], 'ada__learning_rate' : [0.0001, 0.001, 0.01, 0.1, 1.0]},
          {'pca__n_components': [20, 30, 40], 'gb__learning_rate': [0.1, 0.5, 1], 'gb__n_estimators': [50, 100, 200]},
          {'pca__n_components': [20, 30, 40]}]

# define the pipeline for each ensemble model
pipelines = []
for name, model in models:
    pipelines.append((name, Pipeline([('pca', PCA()), (name, model)])))

# define the grid search object
grid_searches = []
for pipeline, params in zip(pipelines, params):
    grid_searches.append(GridSearchCV(pipeline[1], params, cv=5, scoring='accuracy', n_jobs=-1))

# fit the grid search objects and evaluate performance
for name, grid_search in zip(models, grid_searches):
    print(name,'')
    grid_search.fit(digits_data, digits_class)
    y_pred = grid_search.predict(digits_data)
    print(grid_search.best_estimator_)
    print('Accuracy:', accuracy_score(digits_class, y_pred))
    print('Confusion Matrix:\n', confusion_matrix(digits_class, y_pred))

"""**VOTING OF ENSEMBLE MODEL**"""

# importing required libraries
from sklearn.ensemble import VotingClassifier

rf = RandomForestClassifier()
ada = AdaBoostClassifier(learning_rate=0.01)
gb = GradientBoostingClassifier(learning_rate=0.5)
nb = GaussianNB()

# define the ensemble classifier
ensemble = VotingClassifier(estimators=[('rf', rf), ('ada', ada),('gb',gb), ('nb', nb)], voting='soft')

# fit the ensemble classifier on the training data
ensemble.fit(digits_data, digits_class)

# evaluate the performance of the ensemble classifier on the testing data
y_pred = ensemble.predict(digits_data)
print('Accuracy:', accuracy_score(digits_class, y_pred))
print('Confusion Matrix:\n', confusion_matrix(digits_class, y_pred))
