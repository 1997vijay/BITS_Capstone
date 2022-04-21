
#*************************************************************************
#     Description:
#           Below is the code for visualizing various metrics for classification models.
#
#     Required Modules are: 
#           matplot,seaborn,sklearn
#
#     Functions Description:
#           1. RocAucPlot()--> Plot the ROC AUC curve.
#           2. HeatMap()--->Plot the confusion matrixs in the form of heatmap.
#           3. PredictionBarGraph---> Plot the bar graph for predicted result.
#           4. Accuracy()----> To display the accuracy
#*************************************************************************

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.metrics import accuracy_score, confusion_matrix


#function for RocAuc plot
def RocAucPlot(model,X_test,y_test):
    from sklearn.metrics import roc_auc_score,roc_curve,plot_roc_curve
    # fig,ax=plt.subplots(figsize=(15,6))
    # st.subheader("ROC Curve") 
    # plot_roc_curve(model, X_test, y_test)
    # st.pyplot()
    
    # roc curve for classes
    y_prob= model.predict_proba(X_test)
    y_pred= model.predict(X_test)
    fpr = {}
    tpr = {}
    thresh ={}
    auc = roc_auc_score(y_test, y_pred)
    
    
    n_class =len([0,1])
    
    for i in range(n_class):    
        fpr[i], tpr[i], thresh[i] = roc_curve(y_test, y_prob[:,i], pos_label=i)
        
    # plotting 
    fig=plt.figure(figsize=(16,7))
    plt.plot(fpr[0], tpr[0], linestyle='--',color='yellow', label='Class 0')
    plt.plot(fpr[1], tpr[1], linestyle='--',color='green', label='Class 1')
    plt.plot([0, 1], [0, 1],'r--',label="AUC="+str(auc))
    plt.title('ROC curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive rate')
    plt.legend(loc='best')
    st.pyplot(fig)

def HeatMap(acutal,predicted):
    cm=confusion_matrix(acutal,predicted)
    fig,ax=plt.subplots(figsize=(15,6))
    sns.heatmap(cm,annot=True,fmt='d')
    st.pyplot(fig)

# def ClassificationReport(actual,predicted):
#     report=classification_report(actual,predicted)
#     st.write(report)

def PredictionBarGraph(result):
    # plotting 


    #Add new ticks to x axis
    fig=plt.figure(figsize=(16,7))
    plots=sns.countplot(x=result['Predicted'])
    old_ticks =plots.get_xticks().tolist()
    new_ticks = ['Stay','Left']
    plt.xticks(range(len(old_ticks)), new_ticks)
    plt.legend(loc='best')

    for bar in plots.patches: 
        plots.annotate(format(bar.get_height(), ''),  
                           (bar.get_x() + bar.get_width() / 2,  
                            bar.get_height()),ha='center', va='center', 
                           size=13, xytext=(0, 8), 
                           textcoords='offset points') 
    st.pyplot(fig)

def Accuracy(actual,predicted):
    acc=accuracy_score(actual,predicted)
    st.markdown(f'<h3 style="color:green">Accuracy: {round(acc*100)}%</h3>',unsafe_allow_html=True)