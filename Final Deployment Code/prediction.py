
#*************************************************************************
#     Description:
#           Below is the code for prediction on raw data
#           It required the functions from scalling.py and preprocess.py file for preproces the raw data.
#
#     Required Modules are: 
#           Preprocess,scalling, metrics,os,pickle,streamlit,pandas,

#     Functions Description:
#           1. MakePrediction()--> Function that recieve the data,model name and prediction type as perameters.
#                                  Then it call other functions for preprocessing the data to make the final prediction.
#
#           2. TestDataPreprocessing()--->This function is responsible for preprocessing the raw data.
#                                       and give the dataset with selected features which can be used for prediction.
#
#           3. Prediction()---> Function is responsible for making the final prediction and plotting the graph
#
#           4.SinglePrediction()----> When user want to make single prediction rather then batch prediction.
#                           This function is to display the input form and take the input from user and convert it to dataframe.
#                           
#*************************************************************************


from metrics import PredictionBarGraph
from metrics import HeatMap
from metrics import RocAucPlot,Accuracy
from preprocess import Preprocess
from os.path import exists
from scaling import MinMaxScalling, StandardScalling, PowerScalling, RobustScalling, convertToNumerical
import pickle
import pandas as pd
import streamlit as st

#to make all radio button  horizontal
#st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# preprocessing function for new test data
def TestDataPreprocessing(dataframe, encoding, scalling, features):
    df_copy = dataframe.copy()

    # Encoding
    columns = ['Gender', 'EducationLevel', 'Promotion']
    df_copy = convertToNumerical(df_copy, columns, encoding)

    df_copy = convertToNumerical(df_copy, ['City'], 'target')

    # dropping unnecessary columns
    column = ['MMM-YY', 'EmpID', 'DateofJoining','LastWorkingDate', 'Age', 'Salary']
    df_copy.drop(column, axis=1, inplace=True)

    # scalling the data
    if(scalling == 'minmax'):
        df_copy = MinMaxScalling(df_copy)
    elif(scalling == 'robust'):
        df_copy = RobustScalling(df_copy)
    elif(scalling == 'power'):
        df_copy = PowerScalling(df_copy)
    else:
        df_copy = StandardScalling(df_copy)

    X = df_copy[features]
    return X

# function to make prediction on unseen data
def Prediction(data, modelpath, features,prediction_type):
    dataframe = data
    X = TestDataPreprocessing(data, 'label', 'standard', features)

    # load the model and make prediction
    loaded_model = pickle.load(open(modelpath, 'rb'))

    #predict
    result = loaded_model.predict(X)
    data_result = pd.concat([dataframe['EmpID'], pd.DataFrame(pd.Series(result))], axis=1)
    data_result.columns = ['EmpID', 'Predicted']

    # return result
    if(prediction_type=='Single Prediction'):
                return result
    elif(prediction_type=='Batch Prediction'):
        PredictionBarGraph(data_result)
        return data_result
    else:
        RocAucPlot(loaded_model,X,data['Resign'])
        HeatMap(data['Resign'],data_result['Predicted'])
        PredictionBarGraph(data_result)
        Accuracy(data['Resign'],data_result['Predicted'])
        return data_result


def MakePrediction(data, model,prediction_type):
    # df_score_table1=pd.read_csv('final_models.csv')

    # preprocess the data
    dataframe = Preprocess(data)

    # features=df_score_table1[df_score_table1['Model']==model_name]['Features'].tolist()
    features = ['City', 'TotalBusinessValue', 'QuarterlyRating','TotalBusinessValue_change', 'Retention_years']

    # Load the model
    modelname = model
    modelpath = f'./models/{modelname}.sav'
    file_name = modelpath
    if(exists(file_name) != True):
        st.error(
            "The model {} is not available. Try a different model!".format(file_name))
        return
    
    #check the prediction type
    if(prediction_type=='Single Prediction'):
        data_result = Prediction(dataframe, modelpath, features,prediction_type)
        if(data_result==1):
            st.markdown('<h4 style="color:green">Employee will stay!! 😃</h4>',unsafe_allow_html=True)
        else:
            st.markdown('<h4 style="color:red">Employee will Resign!!</h4>',unsafe_allow_html=True)
    else:
        # # call the prediction function
        data_result = Prediction(dataframe, modelpath, features,prediction_type)
        data_result['Actual'] = dataframe['Resign']
    return data_result

# function for basic statistic of dataframe
def SinglePrediction():
    input_dict={}
    EmpID=st.text_input("Employee ID","25")
    Age=st.text_input("Age","25")
    Gender=st.radio("Gender",('Male','Female'))
    City=st.text_input("Enter the City","C23")
    EducationLevel=st.radio("Select Education",('Master', 'College', 'Bachelor'))
    Salary=st.text_input("Salary","2156")
    DateofJoining=st.date_input("Date of Joining")
    JoiningDesignation=st.radio("Joining Designation",(1, 2, 3, 4, 5))
    Designation=st.radio("Current Designation",(1, 2, 3, 4, 5))
    TotalBusinessValue=st.text_input("Business Value","0")
    QuarterlyRating=st.radio("Quarterly Rating",(1, 2, 3, 4))
    MMM_YY=st.date_input('MMM-YY',disabled=True,)

    input_dict['EmpID']=EmpID
    input_dict['Age']=Age
    input_dict['Gender']=Gender
    input_dict['City']=City
    input_dict['EducationLevel']=EducationLevel
    input_dict['Salary']=Salary
    input_dict['DateofJoining']=DateofJoining
    input_dict['JoiningDesignation']=JoiningDesignation
    input_dict['Designation']=Designation
    input_dict['MMM-YY']=MMM_YY
    input_dict['LastWorkingDate']=''
    input_dict['TotalBusinessValue']=TotalBusinessValue
    input_dict['QuarterlyRating']=QuarterlyRating

    dataframe=pd.DataFrame(input_dict,index=[0])
    dataframe['MMM-YY']=pd.to_datetime(dataframe['MMM-YY'])
    dataframe['DateofJoining']=pd.to_datetime(dataframe['DateofJoining'])
    dataframe['Age']=dataframe['Age'].astype('int')
    dataframe['Salary']=dataframe['Salary'].astype('int')

    return dataframe
