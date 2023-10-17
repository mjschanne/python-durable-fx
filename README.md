# CAUTION
- readme and code is WIP and just a demo of connecting an event hub trigger function to a durable orechstrator doing function chaining against a file in blob storage

# python-durable-fx
Demonstrating a function chaining durable function written in python

# Requirements
- Azure extension
- Azure Functions extensions
- Azurite extension
- Python 3.11.x


possibly not installed by the extensions
- Azure CLI
- Azure Functions Core tools
- Azurite

# Steps to create python Azure function
- run command palette "Python: Create Environment..."
- run command palette "Azure Functions: Create Function..."
- run commend palette "Azurite: Start"
- select Azure function list from extension and run


# Links
- [Event Hubs with Azure Functions - Azure Example Scenarios | Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/serverless/event-hubs-functions/event-hubs-functions#consuming-events-with-azure-functions)
- [Overview: Authenticate Python apps to Azure using the Azure SDK - Python on Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview#use-defaultazurecredential-in-an-application)
- [azure-sdk-for-python/sdk/identity/azure-identity at main · Azure/azure-sdk-for-python (github.com)](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity#note-about-visualstudiocodecredential)
- [Azure Blob Storage "Authorization Permission Mismatch" error for get request with AD token - Stack Overflow](https://stackoverflow.com/questions/52769758/azure-blob-storage-authorization-permission-mismatch-error-for-get-request-wit)
- [Azure Event Hubs trigger for Azure Functions | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-event-hubs-trigger?tabs=python-v2%2Cisolated-process%2Cnodejs-v4%2Cfunctionsv2%2Cextensionv5&pivots=programming-language-python)