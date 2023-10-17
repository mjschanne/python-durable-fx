import azure.durable_functions as df
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import json
import logging
import os
from typing import List

app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.event_hub_message_trigger(arg_name="events", event_hub_name="%TopicName%", connection="EventHubConnectionString", cardinality=func.Cardinality.MANY) 
@app.durable_client_input(client_name="client")
async def eventhub_trigger(events: List[func.EventHubEvent], client) -> None:
    filenames = []
    logging.info(f"Received {len(events)} events.")
    
    for event in events:
        jsonStr = event.get_body().decode('utf-8')
        logging.info(f"Received event data: {jsonStr}")
        data = json.loads(jsonStr)
        url = data[0]['data']['url']
        filename = read_filename_from_url(url)
        logging.info(f"Received event for file {filename}.")
        filenames.append(filename)

    instance_id = await client.start_new("my_orchestrator", None, filenames)

    logging.info(f"Started orchestration with ID = '{instance_id}'.")

@app.orchestration_trigger(context_name="context")
def my_orchestrator(context: df.DurableOrchestrationContext) -> None:
    filenames: List[str] = context.get_input()
    urls_2 = yield context.call_activity('initial_file_transform', filenames)
    # the rest of this is just showing you can chain functions together
    urls_3 = yield context.call_activity('second_file_transform', urls_2)
    urls_4 = yield context.call_activity('tertiary_file_transform', urls_3)
    for result in urls_4:
        logging.info(result)

@app.activity_trigger(input_name="filenames")
def initial_file_transform(filenames: List[str]) -> List[str]:
    default_credential = DefaultAzureCredential()
    # default_credential = DefaultAzureCredential(logging_enable=True)
    blob_account_url = os.environ["BlobAccountUrl"] #"https://<storageaccountname>.blob.core.windows.net"
    blob_service_client = BlobServiceClient(blob_account_url, credential=default_credential)
    container_name = os.environ["ContainerName"]

    for filename in filenames:
        # the code for creating the blob service client should be lifted and the client provided through DI
        # not enough time to do that now due to lack of familiarity with python DI (could be that it's not supported?)
        blob_client1 = blob_service_client.get_blob_client(container=container_name, blob=filename)
        stream = blob_client1.download_blob()
        logging.info(f"Downloaded {filename} from {container_name} to memory.")
        
        # perform some action on the stream here e.g. decrypt, decompress, or tokenize some data

        # better control over the upload process demonstrated here: https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-upload-python#upload-a-block-blob-by-staging-blocks-and-committing
        result = blob_client1.upload_blob(stream, overwrite=True)

        logging.info(result)
        logging.info(f"Replacing the prior version of {filename} in {container_name} with updated stream.")

    return filenames

@app.activity_trigger(input_name="urls")
def second_file_transform(urls: List[str]) -> List[str]:
    for url in urls:
        logging.info(f"Hello {url}!")
    # todo: transform the file
    # todo: return new location of files
    return urls

@app.activity_trigger(input_name="urls")
def tertiary_file_transform(urls: List[str]) -> List[str]:
    for url in urls:
        logging.info(f"Hello {url}!")
    # todo: transform the file
    # todo: return new location of files
    return urls

def read_filename_from_url(url: str) -> str:
    return url.split('/')[-1]