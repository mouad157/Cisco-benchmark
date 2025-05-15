"""
Project: AI Model Evaluation for Question Answering
Author: Mouad Hakam
Date: 04/03/2025
Description: This script evaluates AI models (OpenAI, Mistral, DeepSeek, and Anthropic) on question-answering tasks.
             It standardizes question types, generates model responses, compares them to ground truth answers, 
             calculates scores, and stores the results in a MongoDB database.

Usage:
    - Run `evaluate()` to process a dataset and evaluate model performance.
    - Use `save_mongodb()` to store results in a MongoDB collection.

Dependencies:
    - Python 3.x
    - Required packages in `requirements.txt`
"""

import openai
from mistralai import Mistral
import anthropic
import csv
import pandas as pd
from pymongo import MongoClient
import torch
import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from QTypeDefs import getPromptMCQ
from pymongo import MongoClient

# Define supported model lists
OPENAI_MODELS=['gpt-4.5-preview', 'omni-moderation-2024-09-26', 'gpt-4.5-preview-2025-02-27', 'gpt-4o-mini-audio-preview-2024-12-17', 'dall-e-3', 'dall-e-2', 'gpt-4o-audio-preview-2024-10-01', 'gpt-4o-audio-preview', 'gpt-4o-mini-realtime-preview-2024-12-17', 'gpt-4o-2024-11-20', 'gpt-4o-mini-realtime-preview', 'o1-mini-2024-09-12', 'o1-preview-2024-09-12', 'o1-mini', 'o1-preview', 'gpt-4o-mini-audio-preview', 'whisper-1', 'gpt-4o-2024-05-13', 'o1', 'gpt-4o-realtime-preview-2024-10-01', 'babbage-002', 'o1-2024-12-17', 'chatgpt-4o-latest', 'gpt-4-turbo-preview', 'tts-1-hd-1106', 'gpt-4o-audio-preview-2024-12-17', 'gpt-4', 'gpt-4-turbo', 'tts-1-hd', 'gpt-4o-mini-2024-07-18', 'gpt-4o-mini', 'text-embedding-3-large', 'tts-1', 'tts-1-1106', 'gpt-4-turbo-2024-04-09', 'gpt-4o-2024-08-06', 'davinci-002', 'gpt-4o', 'gpt-3.5-turbo-1106', 'gpt-3.5-turbo-instruct', 'gpt-3.5-turbo-instruct-0914', 'gpt-3.5-turbo-0125', 'gpt-4-0125-preview', 'gpt-4o-realtime-preview-2024-12-17', 'gpt-3.5-turbo', 'gpt-4o-realtime-preview', 'gpt-3.5-turbo-16k', 'text-embedding-3-small', 'gpt-4-1106-preview', 'text-embedding-ada-002', 'gpt-4-0613', 'o3-mini', 'o3-mini-2025-01-31', 'omni-moderation-latest'] 
ANTHROPIC_MODELS=['claude-3-7-sonnet-20250219', 'claude-3-5-sonnet-20241022', 'claude-3-5-haiku-20241022', 'claude-3-5-sonnet-20240620', 'claude-3-haiku-20240307', 'claude-3-opus-20240229']
DEEPSEEK_MODELS=['deepseek-chat', 'deepseek-reasoner']
MISTRAL_MODELS=['ministral-3b-2410', 'ministral-3b-latest', 'ministral-8b-2410', 'ministral-8b-latest', 'open-mistral-7b', 'mistral-tiny', 'mistral-tiny-2312', 'open-mistral-nemo', 'open-mistral-nemo-2407', 'mistral-tiny-2407', 'mistral-tiny-latest', 'open-mixtral-8x7b', 'mistral-small', 'mistral-small-2312', 'open-mixtral-8x22b', 'open-mixtral-8x22b-2404', 'mistral-small-2402', 'mistral-small-2409', 'mistral-medium-2312', 'mistral-medium', 'mistral-medium-latest', 'mistral-large-2402', 'mistral-large-2407', 'mistral-large-2411', 'mistral-large-latest', 'pixtral-large-2411', 'pixtral-large-latest', 'mistral-large-pixtral-2411', 'codestral-2405', 'codestral-2501', 'codestral-latest', 'codestral-2412', 'codestral-2411-rc5', 'codestral-mamba-2407', 'open-codestral-mamba', 'codestral-mamba-latest', 'pixtral-12b-2409', 'pixtral-12b', 'pixtral-12b-latest', 'mistral-small-2501', 'mistral-small-latest', 'mistral-saba-2502', 'mistral-saba-latest']

# Path to the fine-tuned T5 model
MODEL_PATH= "mood157/question_type"

##################################################### Useful functions ###############################################################

def standardize_string(s):
    """
    Standardize a string by removing unwanted characters and splitting.
    
    Examples:
        "C'" -> "C"
        "A, B" -> ["A", "B"]
        "A B" -> ["A", "B"]
        "AB" -> ["AB"]
    """
    # Remove quotes and extra spaces
    s = s.replace('"', '').replace("'", "").strip()
    # Split by commas or spaces first
    parts = [part.strip() for part in s.replace(",", " ").split()]
    # Further split any multi-character parts into individual characters
    split_parts = []
    for part in parts:
        split_parts.extend(list(part))  # Break each part into characters
    return split_parts

def compute_score(str1, str2):
    """
    Compute score between two strings:
    - 1 for exact match
    - 0 for no match
    - Partial score for partial matches (e.g., 0.5 if one matches partially).
    """
    if str1 == str2:
        return 1  # Exact match
    elif str1 in str2 or str2 in str1:
        return 0.5  # Partial match
    else:
        return 0  # No match
def clean_and_compare(list1, list2):
    """
    Compare two lists of strings and compute scores based on matches.

    Parameters:
        list1 (list): List of strings with complex formats (e.g., "A, B", "AB").
        list2 (list): List of clean strings to compare against (e.g., "A", "AB").
    
    Returns:
        list: A list of scores for each string in list1 when compared to list2.
    """
    scores = []
    for i in range(len(list1)):
        # Standardize the complex string into parts
        standardized_parts = standardize_string(list1[i])
        max_score = 0

        # Compare each part to the strings in list2
        score = compute_score("".join(standardized_parts), list2[i])
        
        # Append the highest score for the current complex_str
        scores.append(score)
    avg = sum(scores)/len(scores)
    return avg

def predict_question_type(question,model,tokenizer,device):
    """
    Generate a predicted question type using a fine-tuned T5 model.

    Parameters:
        question (str): The input question.
        model (AutoModelForSeq2SeqLM): The T5 model.
        tokenizer (AutoTokenizer): The tokenizer.
        device (str): The device (CPU/GPU).

    Returns:
        str: The predicted question type.
    """
    inputs = tokenizer(getPromptMCQ() + question, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=50)  # Adjust max_length if needed
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.strip()
def get_type(df):
    """
    Apply question type prediction to a dataframe.

    Parameters:
        df (pd.DataFrame): A dataframe containing questions.

    Returns:
        pd.DataFrame: Updated dataframe with predicted types.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH).to(device)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    
    df['predicted_type'] = df['question'].apply(predict_question_type,model=model,tokenizer=tokenizer,device= device)
    # Send the data to the server
    return df
def get_openai_models(api_key):
    try:
        openai.api_key =api_key
        response = openai.models.list()
        return [model.id for model in response]
    except:
        return f"Error: {response.status_code}, {response.text}"
def get_mistral_models(api_key):
    url = "https://api.mistral.ai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        models_json = response.json()
        text_completion_models = [model["id"] for model in models_json["data"] if model["capabilities"]['completion_chat']]
        return text_completion_models
    else:
        return f"Error: {response.status_code}, {response.text}"
    
def get_deepseek_models(api_key):
    url = "https://api.deepseek.com/models"

    payload={}
    headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {api_key}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        models_json = response.json()
        text_completion_models = [model["id"] for model in models_json["data"]]
        return text_completion_models
    else:
        return f"Error: {response.status_code}, {response.text}"
def get_anthropic_models(api_key):
    client = anthropic.Anthropic(api_key=api_key)
    response = client.models.list(limit=20).data
    models = [model.id for model in response]
    return models
####################################################################################################################################

def evaluate(input_file,model_type, model_name, api_key,system_prompt,output_file="questions_answers.csv"):
    """
    Evaluate a model on a dataset.

    Parameters:
        input_file (str): Path to input CSV file.
        model_type (str): choose one of those openai, mistral, deepseek, anthropic.
        model_name (str): Model name.
        api_key (str): API key.
        system_prompt (str): System-level prompt.
        output_file (str, optional): Output file name.

    Returns:
        pd.DataFrame: Updated dataset with results.
        float: The overall model accuracy.
    """

    if input_file:
        dataset = pd.read_csv(input_file)
        dataset_type = get_type(dataset)

    def generate_answer(question,model_type, model_name,key,prompt=None):
        """
        Generate an answer using the specified AI model.

        Parameters:
            question (str): The input question.
            model_type (str): choose one of those openai, mistral, deepseek, anthropic.
            model_name (str): The model being used.
            key (str): API key for authentication.
            prompt (str, optional): System prompt.

        Returns:
            str: The generated answer.
        """
        if model_type == "openai":
          OPENAI_MODELS = get_openai_models(api_key)
        elif model_type == "mistral":
          MISTRAL_MODELS = get_mistral_models(api_key)
        elif model_type == "deepseek":
          DEEPSEEK_MODELS = get_deepseek_models(api_key)
        elif model_type == "anthropic":
          ANTHROPIC_MODELS = get_anthropic_models(api_key)
        else:
          return "The model_type you provided is not openai, mistral, anthropic nor deepseek. Please provide a correct model type"
        if prompt and model_name in MISTRAL_MODELS:
            message= [
                {"role": "assistant", "content": prompt},
                {"role": "user", "content": question}
            ]
        elif prompt and model_name not in MISTRAL_MODELS:
            message = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
                ]
        else:
            message = [
                {"role": "user", "content": question}
                ]
        if model_name in OPENAI_MODELS:
            response = openai.OpenAI(api_key=key).chat.completions.create(
            model=model_name,
            messages=message,
            seed = 12
        )
            return response.choices[0].message.content
        elif model_name in MISTRAL_MODELS:
            client = Mistral(api_key=key)
            chat_response = client.chat.complete(model = model_name,messages = message)
            return chat_response.choices[0].message.content
        elif model_name in DEEPSEEK_MODELS:
            client = openai.OpenAI(api_key=key, base_url="https://api.deepseek.com")
            chat_response = client.chat.completions.create(model = model_name,messages = message,stream= False)
            return chat_response.choices[0].message.content
        elif model_name in ANTHROPIC_MODELS:
            client = anthropic.Anthropic(api_key=key)
            message1 = client.messages.create(model=model_name,max_tokens=1024,messages=message)
            return message1
        else:
            return "Model not found."
    # Evaluate Model
    y_true = [item["answer"] for _,item in dataset_type.iterrows()]
    y_pred = [generate_answer(item["question"],model_type, model_name,api_key,prompt=system_prompt) for _,item in dataset_type.iterrows()]
    for index, elem in dataset_type.iterrows():
        dataset_type.at[index,"model_name"] = str(model_name)
        dataset_type.at[index,"model_answer"] = y_pred[index]
        dataset_type.at[index,"dataset"] = input_file
        dataset_type.at[index,"score"] = compute_score("".join(standardize_string(y_pred[index])),elem["answer"])

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write the header
        writer.writerow(['question', 'answer',"file_name"])
        # Write the rows
        for question, answer in zip(y_true, y_pred):
            
            writer.writerow([question, answer, input_file])

    data_dict = dataset_type.to_dict('records')

    avg = clean_and_compare(y_true, y_pred)*100
    return dataset_type, avg

def save_mongodb(df,client,db,collection):
    """
    Save results to a MongoDB collection.

    Parameters:
        df (pd.DataFrame): Dataframe to save.
        client (str): MongoDB connection string.
        db (str): Database name.
        collection (str): Collection name.
    """
    _client = MongoClient(client)
    _database  = _client[db]
    _collection = _database[collection]
    data_dict = df.to_dict('records')
    _collection.insert_many(data_dict)


