#*************************************************************************
#     Description:
#           This  code is used to display the basic statistics of the data.

#     Required Modules are: 
#           pandas,streamlit

#     Functions Description:
#           1. BasicStat()--> to display the basic details of dataset.
#           2. dfDescription()--->to display the statistics of dataset.
#*************************************************************************
import pandas as pd
import streamlit as st

def BasicStat(dataframe):
    st.markdown(
        '<h4 style="color:red;text-align:center">---Basic Description of Data Frame---</h4>', unsafe_allow_html=True)
    # total count
    st.write('Shape of the data')
    st.write(dataframe.shape)

    st.write('Total Records are..')
    st.write(len(dataframe))

    # duplicate count
    st.markdown('Total Duplicate Count..')
    st.write(dataframe.duplicated().sum())

    st.write("The first few rows...")
    st.write(dataframe.head())


    # missing value
    st.write("Are there any missing values in the dataframe?")
    null_df = pd.DataFrame(dataframe.isnull().sum())
    null_df.columns = ['Null Records']
    null_df = null_df[null_df['Null Records'] != 0]

    st.write(null_df)

    # duplicate
    st.write("Are there any duplicate observations in the dataframe?")
    st.write(dataframe.duplicated().values.any())


def dfDescription(dataframe):
    # Discreption of Data Frame
    st.write('Statistics of Data Frame:\n')
    # lamda function is to avoid printing scientific notation
    result = dataframe.describe().apply(lambda s: s.apply('{0:.5f}'.format)).T
    result['median'] = dataframe.median()
    st.write(result)
