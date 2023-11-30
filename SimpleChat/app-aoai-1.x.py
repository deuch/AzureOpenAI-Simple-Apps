import os
import httpx

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)
from werkzeug.utils import secure_filename
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

DEPLOYMENT_TARGET=os.environ.get('DEPLOYMENT_TARGET') #Local or Azure
AZURE_OPENAI_RESOURCE_ENDPOINT=os.environ.get('AZURE_OPENAI_RESOURCE_ENDPOINT')
AZURE_OPENAI_ENGINE=os.environ.get('AZURE_OPENAI_ENGINE')
AZURE_OPENAI_API_VERSION=os.environ.get('AZURE_OPENAI_API_VERSION')
#SSL_CA_CERTIFICATE=os.environ.get('SSL_CA_CERTIFICATE')
#PROXY_LIST=os.environ.get('PROXY_LIST')
#By default, SSL Verify is set to True
#SSL_VERIFY=True

app = Flask(__name__)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/chat', methods=['POST'])
def chat():

   messages = request.json
   print(messages)
   
   if DEPLOYMENT_TARGET.lower()=="azure":
     # Deployment in Azure 
     token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
     client = AzureOpenAI(
       api_version = AZURE_OPENAI_API_VERSION,
       azure_ad_token_provider = token_provider,
       azure_endpoint = AZURE_OPENAI_RESOURCE_ENDPOINT,
       http_client=httpx.Client(verify=True)
     )
   else: # Local Deployment
     AZURE_OPENAI_API_KEY=os.getenv('AZURE_OPENAI_API_KEY')
     client = AzureOpenAI(
       api_version = AZURE_OPENAI_API_VERSION,
       api_key = AZURE_OPENAI_API_KEY,
       azure_endpoint = AZURE_OPENAI_RESOURCE_ENDPOINT,
       http_client=httpx.Client(verify=False)
     )

   completion = client.chat.completions.create(
     model=AZURE_OPENAI_ENGINE,
     messages = messages['messages'],
     temperature=messages['temperature'],
     max_tokens=messages['max_tokens'],
     top_p=messages['top_p'],
     frequency_penalty=messages['frequency_penalty'],
     presence_penalty=messages['presence_penalty'],
     stop=messages['stop'])

   print(completion.choices[0].message.content)
   #print(response['choices'][0]['message']['content'])
   
   return completion.model_dump_json()

if __name__ == '__main__':
   app.run()
