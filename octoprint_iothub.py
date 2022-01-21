# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
import asyncio
import time
import uuid
import requests, json
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

octoprint_url = ""
octoprint_api_key = ""


async def send_recurring_telemetry(device_client, octoprint_url, octoprint_api_key):
    # Connect the client.
    await device_client.connect()

    # Send recurring telemetry
    i = 0
    while True:
        header = {'X-Api-Key': octoprint_api_key}
        r = requests.get(octoprint_url + '/api/printer', headers=header)
        printer = json.loads(r.text)
        r = requests.get(octoprint_url + '/api/job', headers=header)
        job = json.loads(r.text)
        octoprint = {**printer, **job}

        i += 1
        msg = Message(json.dumps(octoprint))
        msg.message_id = uuid.uuid4()
        msg.correlation_id = "correlation-" + str(i)
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"
        print("sending message #" + str(i))
        await device_client.send_message(msg)
        await device_client.patch_twin_reported_properties(printer["temperature"])
        time.sleep(2)

def main():
    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
    octoprint_url = os.getenv("OCTOPRINT_URL").strip('/')
    octoprint_api_key = os.getenv("OCTOPRINT_API_KEY")

    def message_received_handler(message):
        data = json.loads(message.data)
        if "lcdMessage" in data:
            commands = {
                "commands": ["M117 " + data["lcdMessage"]]
            }
            header = {'X-Api-Key': octoprint_api_key}
            r = requests.get(octoprint_url + '/api/printer/command', data=commands, headers=header)
        print("the data in the message received was ")
        print(message.data)
        print("custom properties are")
        print(message.custom_properties)
        print("content Type: {0}".format(message.content_type))
        print("")

    def twin_patch_handler(patch):        
        print("the data in the desired properties patch was: {}".format(patch))

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    device_client.on_twin_desired_properties_patch_received = twin_patch_handler
    device_client.on_message_received = message_received_handler

    print("IoTHub Device Client Recurring Telemetry Sample")
    print("Press Ctrl+C to exit")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(send_recurring_telemetry(device_client, octoprint_url, octoprint_api_key))
    except KeyboardInterrupt:
        print("User initiated exit")
    except Exception:
        print("Unexpected exception!")
        raise
    finally:
        loop.run_until_complete(device_client.shutdown())
        loop.close()


if __name__ == "__main__":
    main()