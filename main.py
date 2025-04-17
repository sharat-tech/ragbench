from fastapi import FastAPI
import os
from fastapi import Response
from datetime import date
import json
from ragbench_all_dataset import *  
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

def writetocsv(original_values, generated_values, metrics, dataset_name):
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

def process_question(datasetName: str, questionIndex: int) -> tuple:
    """Helper function to process a question and generate response"""
    question = ragbench_all[datasetName]['train'][questionIndex]['question']
    org_answer = ragbench_all[datasetName]['train'][questionIndex]['response']
    
    top_k = 5
    response_obj, sentence_counter = getResponseForQuestion(datasetName, questionIndex, top_k)
    
    generated_values = getGeneratedvalues(sentence_counter, response_obj)
    original_values = getOriginalvalues(datasetName, questionIndex)
    metrics = compute_metrics(original_values, generated_values)
    
    # Update response object
    response_obj.update({
        "datasetName": datasetName,
        "question": question,
        "orginalanswer": org_answer,
        "generated_context_relevance": generated_values,
        "original_context_relevance": original_values
    })
    
    writetocsv(original_values, generated_values, metrics, datasetName)
    return response_obj

@app.get("/search")
def search(datasetName: str = "hagrid", questionIndex: int = 2):
    response_obj = process_question(datasetName, questionIndex)
    return Response(content=json.dumps(response_obj, indent=4, default=str), 
                   media_type='application/json')

@app.get("/getRandomQuestion")
def getRandomQuestion():
    datasetName, questionIndex = getRandomeQuestion(datasetList)
    response_obj = process_question(datasetName, questionIndex)
    response_obj["questionIndex"] = questionIndex
    return Response(content=json.dumps(response_obj, indent=4, default=str), 
                   media_type='application/json')

