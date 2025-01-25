from fastapi import FastAPI
import os
from fastapi import Response
from datetime import date
import json
from ragbench_all_dataset_with_groq_final import *  


# Create an instance of FastAPI
app = FastAPI()

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
    top_k = 4
    responseObj,sentence_counter = getResponseForQuestion(datasetName,questionIndex,vectorstore,top_k)
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
    responseObj["question"] = question

    responseObj["generated_context_relevance"] = generated_values
    responseObj["original_context_relevance"] = original_values

    json_str = json.dumps(responseObj, indent=4, default=str)
    return Response(content=json_str, media_type='application/json')
     

# Define a route
@app.get("/getRandomQuestion")
def getRandomQuestion():
  
    datasetName,questionIndex = getRandomeQuestion(datasetList)
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
    top_k = 4
    responseObj,sentence_counter = getResponseForQuestion(datasetName,questionIndex,vectorstore,top_k)
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
    responseObj["question"] = question

    responseObj["generated_context_relevance"] = generated_values
    responseObj["original_context_relevance"] = original_values

    json_str = json.dumps(responseObj, indent=4, default=str)
    return Response(content=json_str, media_type='application/json')
     
