from gpt_index import SimpleDirectoryReader,GPTListIndex,GPTSimpleVectorIndex,LLMPredictor,PromptHelper
from langchain import OpenAI
import sys
import os
import config


os.environ["OPENAI_API_KEY"] = config.OPEN_API_KEY


def create_vector_index():
  max_input = 4096
  tokens = 200
  chunk_size = 600 #for LLM, we need to define chunk size
  max_chunk_overlap = 20
  
  # name of the directory where *txt files are stored
  path ="book"
  
  #define prompt 
  promptHelper = PromptHelper(max_input,tokens,max_chunk_overlap,chunk_size_limit=chunk_size)
  
  #define LLM — there could be many models we can use, but in this example, let’s go with OpenAI model
  llmPredictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-ada-001",max_tokens=tokens))
  
  #load data — it will take all the .txt files, if there are more than 1
  docs = SimpleDirectoryReader(path).load_data()

  #create vector index
  vectorIndex = GPTSimpleVectorIndex(documents=docs,llm_predictor=llmPredictor,prompt_helper=promptHelper)
  vectorIndex.save_to_disk('vectorIndex.json')
  return vectorIndex



def create_chat_display():
  vIndex = GPTSimpleVectorIndex.load_from_disk('vectorIndex.json')
  while True:
    user_input = input('Please ask: ')
    response = vIndex.query(user_input,response_mode="compact")
    print(f"Response: {response} \n")


create_vector_index()
create_chat_display()