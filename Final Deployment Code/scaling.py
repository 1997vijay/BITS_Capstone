#*************************************************************************
#     Description:
#           Below is the code for scalling the  preprocessed data for prediction purpose.
#           
#
#     Required Modules are: 
#           matplot,seaborn,sklearn
#     Functions Description:
#           1. convertToNumerical()--> Function to convert categorical data to numerical data.
#*************************************************************************

import pandas as pd
import streamlit as st
from preprocess import ChangeDataTypes
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler, RobustScaler, PowerTransformer
from category_encoders import TargetEncoder

# function for One-hot encoding and Label Encoding
def convertToNumerical(dataframe, columns, encoding):
    if(encoding == 'one-hot'):
        #print('One-Hot Encoding..')
        for c in columns:
            new_df = 'df_'+c
            new_df = pd.get_dummies(dataframe[c])
            dataframe = pd.concat([dataframe, new_df], axis=1)
            dataframe.drop(c, axis=1, inplace=True)
    elif(encoding == 'target'):
        #st.write('Target Encoding...')
        # cat_column=['Gender','EducationLevel','JoiningDesignation','Designation','QuarterlyRating','Resign']
        cat_column = ['Resign']
        dataframe = ChangeDataTypes(dataframe, cat_column, 'int64')
        tr = TargetEncoder(cols=['City'])
        dataframe = tr.fit_transform(X=dataframe, y=dataframe['Resign'])
        dataframe = ChangeDataTypes(dataframe, cat_column, 'category')
    else:
        #print('Label Encoding...')
        for c in columns:
            lr = LabelEncoder()
            dataframe[c] = lr.fit_transform(dataframe[c])
    return dataframe


def MinMaxScalling(data):
    scaler = MinMaxScaler()
    for c in data.columns.tolist():
        if(c != 'Resign'):
            data[c] = scaler.fit_transform(data[[c]])
        else:
            pass
    #st.write('MinMax Scalling done')
    return data


def StandardScalling(data):
    scaler = StandardScaler()
    for c in data.columns.tolist():
        if(c != 'Resign'):
            data[c] = scaler.fit_transform(data[[c]])
        else:
            pass
    #st.write('Standard Scalling done')
    return data


def RobustScalling(data):
    scaler = RobustScaler()
    for c in data.columns.tolist():
        if(c != 'Resign'):
            data[c] = scaler.fit_transform(data[[c]])
        else:
            pass
    #st.write('Robust Scalling done')
    return data


def PowerScalling(data):
    scaler = PowerTransformer()
    for c in data.columns.tolist():
        if(c != 'Resign'):
            data[c] = scaler.fit_transform(data[[c]])
        else:
            pass
    st.write('Power Scalling done')
    return data
