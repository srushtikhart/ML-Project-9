# -*- coding: utf-8 -*-
"""fake_job_postings.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1x9fztfVD3bY-SAehuvjjviWKbftUZcQv
"""

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df_job=pd.read_csv(r'/content/drive/MyDrive/fake_job_postings.csv')
df_job.head()

#Check columns
df_job.columns

df_job.isnull().sum()

df_job.dtypes

df_job['department'] = df_job['department'].fillna(df_job['department'].mode()[0])

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn import feature_selection
from sklearn.impute import SimpleImputer

data_cat_imp=SimpleImputer(strategy="constant",fill_value="Missing")
cat_imp_feature=["title","location","department","salary_range","company_profile","description","requirements","benefits",
                 "employment_type","required_experience","required_education","industry","function"]

# Filling the Numerical values through existing value
data_num_imp=SimpleImputer(strategy="constant",fill_value=None)
num_imp_feature =["job_id","telecommuting","has_company_logo","has_questions","fraudulent"]

# Transforming into column
data_imp_trans=ColumnTransformer([("data_cat_imp",data_cat_imp,cat_imp_feature),
                                 ("data_num_imp",data_num_imp,num_imp_feature)])

# Transforming and assigning the data
transformed_data=data_imp_trans.fit_transform(df_job)
transformed_data

#Transforming the data into data frame
df_job_transformed_data=pd.DataFrame(transformed_data,
                         columns=["title","location","department","salary_range","company_profile","description",
                                  "requirements","benefits", "employment_type","required_experience","required_education",
                                  "industry","function","job_id","telecommuting","has_company_logo","has_questions",
                                  "fraudulent"])

df_job_transformed_data.head(2)

df_job_transformed_data.isna().sum()

X_trans = df_job_transformed_data.drop("fraudulent",axis=1)
y_trans = df_job_transformed_data.fraudulent
y_trans=y_trans.astype('int')

#shape(row,column) of features and label
X_trans.shape, y_trans.shape,X_trans.columns

X_trans

# Instantation of One Hot Encoder for categorical data tarnsformatio into Numeric
one_hot=OneHotEncoder()
clf_trans=ColumnTransformer([("one_hot",one_hot,cat_imp_feature)],remainder="passthrough")
X_trans_fin=clf_trans.fit_transform(X_trans)
np.array(X_trans_fin)

#splitting the data into train and test with 23% reserved for testing and 77% for training
X_train,X_test,y_train,y_test=train_test_split(X_trans_fin,y_trans,test_size=0.23, random_state=42)
X_train.shape,X_test.shape,y_train.shape,y_test.shape

model_rfm=RandomForestClassifier()

#fitting the data into model
model_rfm.fit(X_train,y_train)

print(f"Fake Job Random Forest Model Accuracy : {model_rfm.score(X_test,y_test)*100:.2f}%")

y_pred_rfm=model_rfm.predict(X_test)
y_pred_rfm

from sklearn.metrics import classification_report

#classification report
print(classification_report(y_test,y_pred_rfm))