
#*************************************************************************
#     Description:
#           Below is the user interface code for prediction. User can upload the raw data and can make the prediction.

#     Required Modules are: 
#           prediction, discription,pandas,streamlit
#
#     Functions Description:
#           1. OnFileUploat()--> It is basically calling other function after loading the raw data like to dispaly basic details of dataset
#           2. main()--->Main function that contain the code for user interface and to load the file.
#                       It use other function from prediction.py file like MakePrediction() and SinglePrediction()       
#*************************************************************************
from operator import index
import os
import pandas as pd
import streamlit as st
from prediction import SinglePrediction,MakePrediction
from description import BasicStat,dfDescription
import base64


#list of models
path = "./models"
dir_list = os.listdir(path)
model_name = []
for name in dir_list:
    nm = name.split(".sav")[0]
    model_name.append(nm)


#show basic details of dataframe after loading the file
def OnFileUpload(uploaded_file):
    with st.spinner('Please wait...'):
        data = pd.read_csv(uploaded_file)
        st.success('Here is some information about the uploaded data')
    BasicStat(data)
    dfDescription(data)
    return data


def main():
    #st.image('emp2.jpg')

    file_ = open("emp2.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(f'<img width=800 style="margin-left:-50px" src="data:image/gif;base64,{data_url}">',unsafe_allow_html=True,)
    st.markdown('<h1 style=text-align:center;color:teal;)>Employee Retention Prediction</center>',unsafe_allow_html=True)
    st.markdown('<h2 style=text-align:center>Capstone Project</center>',unsafe_allow_html=True)
    st.markdown('<h4 style=text-align:center>PGCP in Artificial Intelligence and Machine Learning- Group 5</center>',unsafe_allow_html=True)


    # Sidebar -Menu
    st.sidebar.header("Employee Retention Prediction")
    prediction_type=st.sidebar.radio('👉 Prediction Type',('Batch Prediction','Single Prediction','Train Prediction'))

    # model selectbox
    modelname = st.sidebar.selectbox("Models:", model_name)

    # Select the prediction type
    if(prediction_type=='Single Prediction'):
        data=SinglePrediction()
        submit_button=st.button("Predict  🤖")
        if(submit_button):
            st.markdown(f"<h4 style='color:green'>Selected Model: {modelname}</h4>",unsafe_allow_html=True)
            MakePrediction(data, modelname,prediction_type)

    elif(prediction_type=='Train Prediction'):
                # Sidebar - Upload Data File
        uploaded_file = st.sidebar.file_uploader("📁 Upload Your .csv File", type='csv')
        if (uploaded_file is not None):
            data = OnFileUpload(uploaded_file)


            #Select the model and make prediction
            if(modelname):
                st.markdown(f"<h4 style='color:green'>Selected Model: {modelname}</h4>",unsafe_allow_html=True)
                predict = st.button("Predict  🤖")
                if(predict):
                    st.write('Prediction and Graph will go here..')
                    MakePrediction(data, modelname,prediction_type)   
        else:
            st.info('Please upload the file!')

    else:
        # Sidebar - Upload Data File
        uploaded_file = st.sidebar.file_uploader("📁 Upload Your .csv File", type='csv')
        if (uploaded_file is not None):
            data = OnFileUpload(uploaded_file)

            #Select the model and make prediction
            if(modelname):
                st.markdown(f"<h4 style='color:green'>Selected Model: {modelname}</h4>",unsafe_allow_html=True)
                predict = st.button("Predict  🤖")
                if(predict):
                    MakePrediction(data, modelname,prediction_type)   
        else:
            st.info('Please upload the file!')

if __name__ == '__main__':
    main()

# end of file
