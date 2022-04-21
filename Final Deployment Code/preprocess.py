#*************************************************************************
#     Description:
#           Below is the code is responsible for preprocessing the raws data to prediction ready input data.
#           
#
#     Required Modules are: 
#           matplot,numpy,pandas,streamlit
#     Functions Description:
#           1. ChangeInValue()--> It will add new column as per the increase and decrease in the value for a column.
#           2. BinningCol()--> Function to add the binning value for any columns
#           3. NewColumn()--> Function to add all the required derived column
#           4. ChangeDataTypes()--> To change the data type of any columns to any data type.
#           5. remove_duplicate()--> to remove the duplicate from the dataset.
#           6. Preprocess()---> Main pipeline that is calling all the function in sequence 
#*************************************************************************

# import all the required library
import matplotlib.style as style
import pandas as pd
import numpy as np
import warnings
import streamlit as st
warnings.filterwarnings('ignore')

style.use('fivethirtyeight')

# Function to Determining the variation
# shift is used to shift the value by index

def ChangeInValue(dataframe, column):
    new_column = column+'_change'
    dataframe[new_column] = dataframe.groupby(['EmpID'])[column].transform(lambda y: y - y.shift(1)).apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    return dataframe


def BinningCol(df, col):
    label = [1, 2, 3]
    df['bins_'+col] = pd.cut(df[col], 3)
    return pd.cut(df[col], 3, labels=label)


def NewColumn(dataframe):
    # adding target column
    dataframe['Resign'] = np.where(dataframe['LastWorkingDate'].isnull() == True, 0, 1)

    # Hike Column
    dataframe['SalaryChangeAmount'] = dataframe.groupby(['EmpID'])['Salary'].transform(lambda y: y-y.shift(1)).apply(lambda x: x if x > 0 else (-x if x < 0 else 0))
    dataframe['Hike%'] = (dataframe['SalaryChangeAmount'])*100//dataframe['Salary']
    dataframe.drop('SalaryChangeAmount', axis=1, inplace=True)

   # Promotion Column (Yes/No)
    dataframe['Promotion'] = dataframe['Designation'] - dataframe['JoiningDesignation']

    # Replacing Promotion values to Yes and No
    dataframe['Promotion'] = dataframe['Promotion'].replace(to_replace=[1, 2, 3, 4], value="Yes").replace(to_replace=[0], value="No").astype('category')
    #st.write('Resign,Hike and Promotion column added,..')

    # Sallary Binning
    dataframe['BinnedSalary'] = BinningCol(dataframe, 'Salary')  # applying the function

    # Age binning
    dataframe['BinnedAge'] = BinningCol(dataframe, 'Age')  # applying the function
    return dataframe

# function to change the datatype of column


def ChangeDataTypes(dataframe, column, column_type):
    import datetime as datetime
    for c in column:
        if(column_type == 'category'):
            dataframe[column] = dataframe[column].astype('category')
        elif(column_type == 'date'):
            # dataframe[column]=pd.to_datetime(dataframe[column],format='%d-%m-%Y').dt.tz_localize(None)
            dataframe[column] = pd.to_datetime(dataframe[column])
        elif(column_type == 'float'):
            dataframe[column] = dataframe[column].astype('float')
        else:
            dataframe[column] = dataframe[column].astype('int64')
    return dataframe


def remove_duplicate(dataframe, column_name):
    # Aggregating the TotalBusinessValue before removing the duplicates
    total_tvb = dataframe[['EmpID', 'TotalBusinessValue']].groupby('EmpID').sum()
    total_tvb.reset_index(drop=True, inplace=True)

    if(len(dataframe)==1):
            dataframe = dataframe.drop_duplicates([column_name], keep='last')
            dataframe.reset_index(drop=True, inplace=True)
    else:
        # remove duplicate
        #st.write(f'Before Removing the duplicates:{len(dataframe)}')
        #st.write('Removing the Duplicate')
        dataframe = dataframe.drop_duplicates([column_name], keep='last')
        dataframe.reset_index(drop=True, inplace=True)
        #st.write(f'After Removing the duplicates:{len(dataframe)}')

    # replacing the TotalBusinessValue value by Aggrgating values
    dataframe['TotalBusinessValue'] = total_tvb['TotalBusinessValue']
    return dataframe


def RetentionYear(dataframe):
    cnt = 0
    dataframe['DateofJoining'] = pd.to_datetime(dataframe['DateofJoining'])
    dataframe['LastWorkingDate'] = pd.to_datetime(dataframe['LastWorkingDate'])
    dataframe['MMM-YY'] = pd.to_datetime(dataframe['MMM-YY'])
    for j, val in enumerate(dataframe.columns.values):
        k = j
    dataframe.insert(k+1, "Retention_years", np.nan)
    for i in range(0, len(dataframe['LastWorkingDate'])):
        f1 = pd.isnull(dataframe['LastWorkingDate'].loc[i])
        if(f1 == False):
            dataframe["Retention_years"].loc[i] = (
                dataframe['LastWorkingDate'].loc[i] - dataframe['DateofJoining'].loc[i])/np.timedelta64(1, 'Y')
            if(pd.isnull(dataframe["Retention_years"].loc[i])):
                dataframe["Retention_years"].loc[i] = (
                    dataframe["MMM-YY"].loc[i]-dataframe["DateofJoining"].loc[i])/np.timedelta64(1, 'Y')
        else:
            dataframe["Retention_years"].loc[i] = (
                dataframe["MMM-YY"].loc[i]-dataframe["DateofJoining"].loc[i])/np.timedelta64(1, 'Y')
            if(dataframe["MMM-YY"].loc[i] == dataframe["DateofJoining"].loc[i]):
                dataframe["Retention_years"].loc[i] = 0

        if(dataframe["Retention_years"].loc[i] < 0):
            cnt = cnt + 1
            dataframe["Retention_years"].loc[i] = 0

    # st.write(
    #     "No. of Cases where Date of Joining is later than Last Working Date:", cnt)
    dataframe["Retention_years"] = dataframe['Retention_years'].round(decimals=2)
    return dataframe


def PromoPerYr(dataframe):
    for j, val in enumerate(dataframe.columns.values):
        k = j
    dataframe.insert(k+1, "PromoPerYr", np.nan)
    for i in range(0, len(dataframe['Retention_years'])):
        if(dataframe['Retention_years'].loc[i] != 0):
            dataframe['PromoPerYr'].loc[i] = (
                dataframe['Designation'].loc[i] - dataframe['JoiningDesignation'].loc[i])/dataframe['Retention_years'].loc[i]

    return dataframe


# function that include all the function to process the file
def Preprocess(data):
    df = data
    # Change in value
    columns = ['Salary', 'Designation','TotalBusinessValue', 'QuarterlyRating']
    for c in columns:
        df = ChangeInValue(df, c)

    # Adding columns
    df = NewColumn(df)

    # changing the data types into category
    cat_column = ['Gender', 'EducationLevel', 'QuarterlyRating', 'Resign']
    df = ChangeDataTypes(df, cat_column, 'category')

    # changing the data types into date
    column = ['MMM-YY', 'DateofJoining', 'LastWorkingDate']
    for col in column:
        df = ChangeDataTypes(df, col, 'date')

    # Remove the duplicate
    df = remove_duplicate(df, 'EmpID')

    # Add the retention year column
    df = RetentionYear(df)

    # Add the PromoPerYr year column
    df = PromoPerYr(df)

    cat_column = ['JoiningDesignation', 'Designation', ]
    df = ChangeDataTypes(df, cat_column, 'category')

    df['YearsOfExperience'] = round(df['Retention_years'])

    df.drop(['bins_Age', 'bins_Salary'], axis=1, inplace=True)

    return df
