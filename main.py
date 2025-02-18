from fastapi import FastAPI
import os
from fastapi import Response
from datetime import date
import json
from ragbench_all_dataset_with_groq_final import *  
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Create an instance of FastAPI
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def writetocsv(original_values, generated_values,metrics,dataset_name):

    # Prepare the row with dataset name, generated values, and original values
    row = {
        'Dataset Name': dataset_name,
        'Generated Context Relevance': generated_values['Context Relevance'],
        'Generated Context Utilization': generated_values['Context Utilization'],
        'Generated Completeness': generated_values['Completeness'],
        'Generated Adherence': generated_values['Adherence'],
        'Original Context Relevance': original_values['Context Relevance'],
        'Original Context Utilization': original_values['Context Utilization'],
        'Original Completeness': original_values['Completeness'],
        'Original Adherence': original_values['Adherence'],
        'Context Relevance_RMSE': metrics['Context Relevance_RMSE'],
        'Context Relevance_AUCROC': metrics['Context Relevance_AUCROC'],
        'Context Utilization_RMSE': metrics['Context Utilization_RMSE'],
        'Context Utilization_AUCROC': metrics['Context Utilization_AUCROC'],
        'Completeness_RMSE': metrics['Completeness_RMSE'],
        'Completeness_AUCROC': metrics['Completeness_AUCROC'],
        'Adherence_RMSE': metrics['Adherence_RMSE'],
        'Adherence_AUCROC': metrics['Adherence_AUCROC'],
    }

    # Define the CSV file name
    csv_file = 'output.csv'

    # Append to CSV
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        df = pd.DataFrame()

    # Create a DataFrame from the new row
    new_row_df = pd.DataFrame([row])

    # Append the new row to the existing DataFrame
    df = pd.concat([df, new_row_df], ignore_index=True)

    # Save to CSV
    df.to_csv(csv_file, index=False)

    print(f"Data appended to {csv_file}")

# Define a route
@app.get("/search")
def search(datasetName:str="hagrid",questionIndex:int=2):
  
    #datasetName,questionIndex = getRandomeQuestion(datasetList)
    # datasetName = "hagrid"
    # questionIndex = 1
    #questionIndex = 270
    #questionIndex = 1303
    question = ragbench_all[datasetName]['train'][questionIndex]['question']
    orgAnswer = ragbench_all[datasetName]['train'][questionIndex]['response']
    orgDocuents = ragbench_all[datasetName]['train'][questionIndex]['documents']
    print("Question: ",question)
    print("Original Answer: ",orgAnswer)
    #print("Original Documents: ",orgDocuents)
    

    #print("Question: ",question)
    top_k = 5
    responseObj,sentence_counter = getResponseForQuestion(datasetName,questionIndex,top_k)
    #print answer from the responseObj
    answer = responseObj["answer"]
    
    print("Generated Answer: ",answer)
    generated_values = getGeneratedvalues(sentence_counter,responseObj)
    original_values = getOriginalvalues(datasetName,questionIndex)

    
    # print values from generated_values object
    print("Generated Context Relevance: ",generated_values["Context Relevance"])
    print("Original Context Relevance: ",original_values["Context Relevance"])
    
    # current_directory = os.getcwd()
    # print("Current Working Directory:", current_directory)
    #return {"message": "Hello from FastAPI!"+current_directory}
    responseObj["datasetName"] = datasetName
    responseObj["question"] = question
    responseObj["orginalanswer"] = orgAnswer

    
    metrics = compute_metrics(original_values,generated_values)
    writetocsv(original_values,generated_values,metrics, datasetName)
    responseObj["generated_context_relevance"] = generated_values
    responseObj["original_context_relevance"] = original_values

    json_str = json.dumps(responseObj, indent=4, default=str)
    return Response(content=json_str, media_type='application/json')
     

# Define a route
@app.get("/getRandomQuestion")
def getRandomQuestion():
  
    datasetName,questionIndex = getRandomeQuestion(datasetList)
    question = ragbench_all[datasetName]['train'][questionIndex]['question']
    orgAnswer = ragbench_all[datasetName]['train'][questionIndex]['response']
    orgDocuents = ragbench_all[datasetName]['train'][questionIndex]['documents']
    print("Question: ",question)
    print("Original Answer: ",orgAnswer)
    
    top_k = 5
    responseObj,sentence_counter = getResponseForQuestion(datasetName,questionIndex,top_k)
    #print answer from the responseObj
    answer = responseObj["answer"]
    print("Generated Answer: ",answer)
    generated_values = getGeneratedvalues(sentence_counter,responseObj)
    original_values = getOriginalvalues(datasetName,questionIndex)
    # print values from generated_values object
    print("Generated Context Relevance: ",generated_values["Context Relevance"])
    print("Original Context Relevance: ",original_values["Context Relevance"])
    
    responseObj["datasetName"] = datasetName

    metrics = compute_metrics(original_values,generated_values)
    writetocsv(original_values,generated_values,metrics, datasetName)

    responseObj["question"] = question

    responseObj["generated_context_relevance"] = generated_values
    responseObj["original_context_relevance"] = original_values
    responseObj["orginalanswer"] = orgAnswer
    responseObj["questionIndex"] = questionIndex

    json_str = json.dumps(responseObj, indent=4, default=str)
    return Response(content=json_str, media_type='application/json')
     
