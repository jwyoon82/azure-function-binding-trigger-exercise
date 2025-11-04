import azure.functions as func
import logging

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="test-hub",
                               connection="dt023eventhub_RootManageSharedAccessKey_EVENTHUB") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))

@app.function_name(name="eventhub_output")
@app.route(route="eventhub_output", methods=["POST"])
@app.event_hub_output(arg_name="event", event_hub_name="test-hub",
                      connection="dt023eventhub_RootManageSharedAccessKey_EVENTHUB")
def eventhub_output(req: func.HttpRequest, event: func.Out[str]) -> func.HttpResponse:
    req_body = req.get_body().decode('utf-8')

    logging.info("HTTP trigger function received a request: %s", req_body)

    event.set(req_body)

    return func.HttpResponse("Event hub output function executed successfully.", status_code=200)


# This example uses SDK types to directly access the underlying EventData object provided by the Event Hubs trigger.
# To use, uncomment the section below and add azurefunctions-extensions-bindings-eventhub to your requirements.txt file
# Ref: aka.ms/functions-sdk-eventhub-python
#
# import azurefunctions.extensions.bindings.eventhub as eh
# @app.event_hub_message_trigger(
#     arg_name="event", event_hub_name="test-hub", connection="dt023eventhub_RootManageSharedAccessKey_EVENTHUB"
# )
# def eventhub_trigger(event: eh.EventData):
#     logging.info(
#         "Python EventHub trigger processed an event %s",
#         event.body_as_str()
#     )
