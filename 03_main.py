#Convert text to Embedings
import os
from dotenv import load_dotenv
import json
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
from openai import OpenAI

load_dotenv()

def create_embedding(text_list):
    req = requests.post("http://localhost:11434/api/embed", json={
        "model":"bge-m3",
        "input":text_list
    })

    embeddings=req.json()['embeddings']

    return embeddings

def process_all_json_files():
    jsons = os.listdir('newJsons')
    chunk_list_dict=[]
    chunk_id=0

    for json_file in jsons:
        with open(f"newJsons/{json_file}") as f:
            content = json.load(f)
        print(f"Processing file: {json_file} with {len(content['chunks'])} chunks")
        embeddings = create_embedding([chunk['text'] for chunk in content['chunks']])
        for i, chunk in enumerate(content['chunks']):
            chunk['embedding']=embeddings[i]
            chunk_id+=1
            chunk['chunk_id']=chunk_id
            chunk_list_dict.append(chunk)
    df=pd.DataFrame.from_records(chunk_list_dict)
    joblib.dump(df,'embeddings.joblib')
    # print(np.vstack(df['embedding'])[:5])
    # print(df['embedding'][:5])

def process_query():
    query = input("Ask a Question: ")

    df= joblib.load('embeddings.joblib')
    query_embedding=create_embedding([query])[0]
    # print(query_embedding)
    similarities=cosine_similarity(np.vstack(df['embedding'].values), 
                                [query_embedding]).flatten()

    # print(similarities)

    top_results=10
    sorted_top_idx = similarities.argsort()[::-1][0:top_results]

    # print(sorted_top_idx)
    top_results_df=df.loc[sorted_top_idx]
    # print(top_results_df[['video_title','video_number','text']])

    # for i, row in top_results_df.iterrows():
    #     print(f"Index:{i}, Video Title: {row['video_title']}, Video Number: {row['video_number']}, Text: {row['text']}, Start Timestamp:{row['start']}, End Timestamp:{row['end']}")
    get_response_from_llm(query,top_results_df)

def get_response_from_llm(query,new_df):
    prompt = f'''
            Your role is to answer the user queries related to the sigma web development course. If a user asks something unrelated to the course just tell I'm Sigma Assistant for the Web developement course and please Ask from the course related queries only.
            Here are the top 10 video chunks containing Video Title, Video Number, Text, Start Timestamp in seconds, End Timestamp in seconds  that have high cosine similarity to user query: {new_df[['video_title','video_number','text','start','end']].to_json(orient='records')}
            --------------------------------------------------------
            User will ask query and you have to answer How much content is taught in which video at what timestamp and guide the user to go to that particular video.
    '''
    #------------Local LLM Server Request----------------
    # req = requests.post("http://localhost:11434/api/generate", json={
    #     "model":"llama3.2",
    #     "prompt":prompt,
    #     "stream":False,
    # })

    # ----------------- Api call to OpenAi responses API -----------------------

    # req = requests.post("https://api.openai.com/v1/responses", 
    #                     headers={
    #                         "Content-Type": "application/json",
    #                         "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    #                     },
    #                     json= {"model":"gpt-4.1-mini",
    #                     "instructions": prompt,
    #                     "temperature": 0.6,
    #                     "input": f"{query}",
    #                     "store":False,
    # })

    # response=req.json()['output'][0]['content'][0]['text']

    #--------------------Using  Open AI SDK------------------------

    client =OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response  =client.responses.create(
        model="gpt-4.1-mini",
        instructions=prompt,
        input=query,
        temperature=0.6,
        store=False
    )
    with open('prompt.txt','w') as f:
        f.write(prompt)

    with open('response.txt','w') as f:
        f.write(response.output_text)

task=int(input("Enter task: \n 0 for Creating Data Embeddings. \n 1 for entering input\n "))
if task==1:
    process_query()
elif task == 0:
    process_all_json_files()
else:
    print("Invalid Input")
# embedding=create_embedding('Nasib Farooq Ahanger')
# print(len(embedding))