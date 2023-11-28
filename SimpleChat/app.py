import os
import openai

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)
from werkzeug.utils import secure_filename
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

DEPLOYMENT_TARGET=os.environ.get('DEPLOYMENT_TARGET') #Local or Azure
AZURE_OPENAI_RESOURCE_ENDPOINT=os.environ.get('AZURE_OPENAI_RESOURCE_ENDPOINT')
AZURE_OPENAI_ENGINE=os.environ.get('AZURE_OPENAI_ENGINE')
AZURE_OPENAI_API_VERSION=os.environ.get('AZURE_OPENAI_API_VERSION')

print(DEPLOYMENT_TARGET.lower())

openai.api_base = AZURE_OPENAI_RESOURCE_ENDPOINT
openai.api_version = AZURE_OPENAI_API_VERSION

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
     default_credential = DefaultAzureCredential()
     openai.api_type = "azure_ad"
     token = default_credential.get_token("https://cognitiveservices.azure.com")
     openai.api_key = token.token
   else: # Local Deployment
     AZURE_OPENAI_API_KEY=os.getenv('AZURE_OPENAI_API_KEY')
     openai.api_type = "azure"
     openai.api_key = AZURE_OPENAI_API_KEY

   response = openai.ChatCompletion.create(
     engine=AZURE_OPENAI_ENGINE,
     messages = messages['messages'],
     temperature=messages['temperature'],
     max_tokens=messages['max_tokens'],
     top_p=messages['top_p'],
     frequency_penalty=messages['frequency_penalty'],
     presence_penalty=messages['presence_penalty'],
     stop=messages['stop'])

   print(response['choices'][0]['message']['content'])

   return response

if __name__ == '__main__':
   app.run()

