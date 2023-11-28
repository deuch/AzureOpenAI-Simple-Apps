# Very Simple Chat App with AOAI

This repo contains some code for a very simple chat webapp that integrates with Azure OpenAI. Note: some portions of the app use preview APIs.  
You do not need nodejs or otehr tools. This is purely HTML/CSS/Javascript. IT can be helpfull on desktop/laptop with strict restrictions.

## Prerequisites
- An existing Azure OpenAI resource and model deployment of a chat model (e.g. `gpt-35-turbo`, `gpt-4`)
- An Azure Subscription for a deployment in Azure (Azure App Service)
- Local Deployment : Python and pip installed

## Deploy the app

### Deploy from your local machine

#### Local Setup: Basic Chat Experience
1. Rename the `.env_sample` to `.env` file and Update the environment variables
    
    These variables are required:
    - `DEPLOYMENT_TARGET` set to "Local" as value
    - `AZURE_OPENAI_RESOURCE_ENDPOINT`
    - `AZURE_OPENAI_ENGINE`
    - `AZURE_OPENAI_KEY`

    Please refer and configure your settings as described in the [Environment variables](#environment-variables) section.

2. Install the python dependencies with the command `pip install -r requirements.txt`. This will install the needed librairies (Flask, openai ...)

3. You can see the local running app at http://127.0.0.1:5000.

### Deploy on Azure

#### Deploy with Azure CLI

1. Create a managed identity to handle the authentication from the App Service WebApp to Azure OpenAI
    - Create a User Managed Identiy if needed [how to](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp)
    - Please follow [this guide](https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=portal%2Chttp#add-a-user-assigned-identity) to bind the Managed Identity to your WebApp 
    - Give "Cognitive Services OpenAI User" role to the Managed Identity to the Azure OpenAI ressource 

2. Rename the `appsettings-sample.json` to `appsettings.json` file and Update the environment variables
    
    These variables are required:
    - `DEPLOYMENT_TARGET` set to "Azure" as value
    - `AZURE_CLIENT_ID` with clientID of the managed identity used to authenticate to Azure OpenAI
    - `AZURE_OPENAI_RESOURCE_ENDPOINT`
    - `AZURE_OPENAI_ENGINE`
    - `AZURE_OPENAI_KEY`

3. Create the Azure WebApp

You can use the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) to deploy the app from your local machine. Make sure you have version 2.48.1 or later.

If this is your first time deploying the app, you can use [az webapp up](https://learn.microsoft.com/en-us/cli/azure/webapp?view=azure-cli-latest#az-webapp-up). Run the following command from the root folder of the repo, updating the placeholder values to your desired app name, resource group, location, and subscription. You can also change the SKU if desired.

`az webapp up --runtime PYTHON:3.9 --sku B1 --name <new-app-name> --resource-group <resource-group-name> --location <azure-region> --subscription <subscription-name>`

After that, you need to apply the custom configuration to the AppService WebApp (the app will restart)

`az webapp config appsettings set -g <resource-group-name> -n <new-app-name> --settings "@.\appsettings.json"`

Deployment will take several minutes. When it completes, you should be able to navigate to your app at {app-name}.azurewebsites.net.

#### Add an identity provider

After deployment, you will need to add an identity provider to provide authentication support in your app. See [this tutorial](https://learn.microsoft.com/en-us/azure/app-service/scenario-secure-app-authentication-app-service) for more information.

#### Enable VNET injection

You can inject your App Service in a VNET to be able to reach private endpoint of your Azure OpenAi resource to enhance security and privacy.
See [this tutorial](https://learn.microsoft.com/en-us/azure/app-service/configure-vnet-integration-enable) for more information.

#### Add an private endpoint

Your WebApp is deployed publicly by default. You can add a private endpoint to your WebApp. See [this tutorial](https://learn.microsoft.com/en-us/azure/app-service/overview-private-endpoint) for more information.

## Environment variables

| App Setting | Value | Note |
| --- | --- | ------------- |
|DEPLOYMENT_TARGET||Deployment Target. Local or Azure|
|AZURE_OPENAI_RESOURCE_ENDPOINT||The URL starting with https:// of your Azure OpenAI Service| 
|AZURE_OPENAI_ENGINE||The Deployment Name of your Azure OpenAI model|
|AZURE_OPENAI_KEY||An **access key** for your Azure OpenAI resource|
|AZURE_CLIENT_ID||clientID of the managed identity used by your WebApp to authenticate to Azure OpenAI|
