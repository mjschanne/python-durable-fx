import azure.functions as func
import azure.durable_functions as df
import logging

app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="blobadded", connection="EventHubConnectionString") 
@app.durable_client_input(client_name="client")
async def eventhub_trigger(azeventhub: func.EventHubEvent, client):
    logging.info('Python EventHub trigger processed an event: %s', azeventhub.get_body().decode('utf-8'))

    instance_id = await client.start_new("my_orchestrator", None, None)

    logging.info(f"Started orchestration with ID = '{instance_id}'.")


@app.orchestration_trigger(context_name="context")
def my_orchestrator(context: df.DurableOrchestrationContext):
    result1 = yield context.call_activity('say_hello', "Tokyo")
    result2 = yield context.call_activity('say_hello', "Seattle")
    result3 = yield context.call_activity('say_hello', "London")
    for result in [result1, result2, result3]:
        logging.info(result)

@app.activity_trigger(input_name="city")
def say_hello(city: str) -> str:
    return f"Hello {city}!"