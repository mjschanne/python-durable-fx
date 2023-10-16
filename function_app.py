import azure.functions as func
import azure.durable_functions as df
import logging

app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="blobadded", connection="EventHubConnectionString") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s', azeventhub.get_body().decode('utf-8'))

@app.route(route="orchestrators/{functionName}")
@app.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    function_name = req.route_params.get('functionName')
    instance_id = await client.start_new(function_name)
    
    logging.info(f"Started orchestration with ID = '{instance_id}'.")
    return client.create_check_status_response(req, instance_id)

@app.orchestration_trigger(context_name="context")
def my_orchestrator(context: df.DurableOrchestrationContext):
    result1 = yield context.call_activity('say_hello', "Tokyo")
    result2 = yield context.call_activity('say_hello', "Seattle")
    result3 = yield context.call_activity('say_hello', "London")
    return [result1, result2, result3]

@app.activity_trigger(input_name="city")
def say_hello(city: str) -> str:
    return f"Hello {city}!"