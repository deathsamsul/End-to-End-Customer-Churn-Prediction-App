import pandas as pd
import pickle
import os,psutil


dirc = os.path.dirname(os.path.abspath(__file__))  # abspath return only script file like '.py', and dirname is rturn directory path
model_path = os.path.join(dirc, "ml_model_v3.pkl")    # it combine pkl file path


with open (model_path,'rb') as f:
    pipeline=pickle.load(f)

def churn_predictor(data:dict):
    df=data.copy()

    if df['tenure']!=0:
        df['avg_spend']=df['TotalCharges']/df['tenure']
    else:
        df['avg_spend']=0

    d=pd.DataFrame([df])
    pred=pipeline.predict(d)[0]
    probability=pipeline.predict_proba(d)[0][1]

    return {
        'churn':'Yes' if pred== 1 else "No",
        'probability':round(probability,3)
    }

# ram uses
def ram_use(): 
    process=psutil.Process(os.getpid()) 
    ram=process.memory_info().rss/1024/1024 
    return round(ram,2)