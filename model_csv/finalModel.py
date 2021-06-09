# After Predictions , It was found the Random Forest Classifier predicted values with the best accuracy

## Importing all the required libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.ensemble import RandomForestClassifier
import pickle
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv("Covid Dataset.csv")
df.head()


df.describe()

#wearing masks and sanitization column had one value only which will be of no use hence dropping them
df.drop(["Wearing Masks","Sanitization from Market"], axis= 1, inplace = True)


## Converting Categorical data to numerical data
le=LabelEncoder()
df['Breathing Problem']=le.fit_transform(df['Breathing Problem'])
df['Fever']=le.fit_transform(df['Fever'])
df['Dry Cough']=le.fit_transform(df['Dry Cough'])
df['Sore throat']=le.fit_transform(df['Sore throat'])
df['Running Nose']=le.fit_transform(df['Running Nose'])
df['Asthma']=le.fit_transform(df['Asthma'])
df['Chronic Lung Disease']=le.fit_transform(df['Chronic Lung Disease'])
df['Headache']=le.fit_transform(df['Headache'])
df['Heart Disease']=le.fit_transform(df['Heart Disease'])
df['Diabetes']=le.fit_transform(df['Diabetes'])
df['Hyper Tension']=le.fit_transform(df['Hyper Tension'])
df['Fatigue ']=le.fit_transform(df['Fatigue '])

df['Gastrointestinal ']=le.fit_transform(df['Gastrointestinal '])
df['Abroad travel']=le.fit_transform(df['Abroad travel'])
df['Contact with COVID Patient']=le.fit_transform(df['Contact with COVID Patient'])
df['Attended Large Gathering']=le.fit_transform(df['Attended Large Gathering'])
df['Visited Public Exposed Places']=le.fit_transform(df['Visited Public Exposed Places'])
df['Family working in Public Exposed Places']=le.fit_transform(df['Family working in Public Exposed Places'])
df['COVID-19']=le.fit_transform(df['COVID-19'])
df['Sore throat']=le.fit_transform(df['Sore throat'])

df.head()

## ML Model

x=df.drop('COVID-19',axis=1)
y=df['COVID-19']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

## Random Forest Classifier 

# Fitting & Training Model 
RFmodel = RandomForestClassifier(random_state=0)
RFmodel.fit(x_train,y_train)


pickle.dump(RFmodel,open('RFmodel.pkl','wb'))