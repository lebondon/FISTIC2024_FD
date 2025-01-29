import joblib
from pathlib import Path
import pandas as pd
import os
import numpy as np
import logging

class churn_predictor:

    def __init__(self, model_path="model/pipe.pkl",output_path="output",input_path="data"):
        self.model_path=model_path
        self.output_path=output_path
        self.input_path=input_path


    def load_model(self):
        return joblib.load(self.model_path)
    
    def file_names(self):
        return list(Path(self.input_path).glob("*.csv"))
    
    def load_data(self):

        all_files = self.file_names()

        df_list=[]

        for file in all_files:
            df=pd.read_csv(file)
            df_list.append(df)

            return df_list


    def predict(self):
        data=self.load_data()
        model=self.load_model()

        print(f"Starting predictions...")
        print(f"Using model from: {self.model_path}")
        print(f"Input directory: {self.input_path}")
        print(f"Output directory: {self.output_path}")

        i=0

        for df in data:
            print(f"DataFrame shape: {df.shape}")
            predictions=model.predict(df)
            predictions = np.ravel(predictions)
            print(f"Predictions shape: {predictions.shape}")
            print(f"Predictions type: {type(predictions)}")
            df["Churn_label"]=predictions
            df=df.drop("Unnamed: 0",axis=1)
            print(self.output_path)
            print(self.file_names())
            df.to_csv(f"{self.output_path}/test_predicted.csv")
            i=i+1


def main():

    predictor = churn_predictor()
    predictor.predict()


if __name__=="__main__":
    main()

