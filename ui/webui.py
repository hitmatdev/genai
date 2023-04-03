from flask import Flask, render_template, request
from gpt_index import SimpleDirectoryReader,GPTListIndex,GPTSimpleVectorIndex,LLMPredictor,PromptHelper

import time
import os

import sys
sys.path.insert(0, '.')
import config


os.environ["OPENAI_API_KEY"] = config.OPEN_API_KEY

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg')+ " (give html formatted reply)"
    kbase_embedding =  request.args.get('embedding')
    vectorIndexJson = "vectorIndex.json"

    if kbase_embedding == "hok" :
        vectorIndexJson="bookVectorIndex.json" 
    
    print('vectorIndexJson : '+ '/Users/hmathpal/Desktop/aiml/genai/'+vectorIndexJson)
    vIndex = GPTSimpleVectorIndex.load_from_disk('/Users/hmathpal/Desktop/aiml/genai/'+vectorIndexJson)
    response = vIndex.query(user_input, response_mode="compact")
    time.sleep(1)
    return str(response)

if __name__ == "__main__":
    app.run()
