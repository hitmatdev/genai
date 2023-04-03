from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PDFMinerLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA


from gpt_index import SimpleDirectoryReader,GPTListIndex,GPTSimpleVectorIndex,LLMPredictor,PromptHelper,Document

import config
import os
os.environ["OPENAI_API_KEY"] = config.OPEN_API_KEY



def create_index():

  loader = PDFMinerLoader("book/history_of_kumaon.pdf")
  data = loader.load()

  print (f'You have {len(data)} document(s) in your data')
  print (f'There are {len(data[0].page_content)} characters in your document')

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
  texts = text_splitter.split_documents(data)
  dir_name = "pdf_split_files"

  # create the directory if it doesn't exist
  if not os.path.exists(dir_name):
      os.mkdir(dir_name)
  else:
      # remove any existing files in the directory
      for filename in os.listdir(dir_name):
          file_path = os.path.join(dir_name, filename)
          os.remove(file_path)


  for i, doc in enumerate(texts):
      filename = f"document_{i}.txt"
      file_path = os.path.join(dir_name, filename)
      with open(file_path, "w") as f:
          f.write(doc.page_content)




  documents = SimpleDirectoryReader(dir_name).load_data()

  max_input = 4096
  tokens = 200
  chunk_size = 600 #for LLM, we need to define chunk size
  max_chunk_overlap = 20
    
  
  promptHelper = PromptHelper(max_input,tokens,max_chunk_overlap,chunk_size_limit=chunk_size)
    
    #define LLM — there could be many models we can use, but in this example, let’s go with OpenAI model
  llmPredictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-ada-001",max_tokens=tokens))


  #GPTSimpleVectorIndex = GPTSimpleVectorIndex()
  vectorIndex = GPTSimpleVectorIndex(documents,llm_predictor=llmPredictor,prompt_helper=promptHelper)
  vectorIndex.save_to_disk('bookVectorIndex.json')

def chat_prompt():
  vIndex = GPTSimpleVectorIndex.load_from_disk('`BGHHT6XSa  .json')
  while True:
    user_input = input('Please ask: ')
    response = vIndex.query(user_input,response_mode="compact")
    print(f"Response: {response} \n")


create_index()


