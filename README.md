# OctoPrint IoTHub Telemetry Capture

This is a simple script to push telemetry data from OctoPrint into Azure IoTHub

## Installation

These are instructions for running this script directly on OctoPi, on other systems your mileage may vary.

### Step 1: Get the code
```
git clone https://github.com/cbattlegear/OctoPrint-IoTHub.git
```

### Step 2: Install the Python 3 IoT Hub module
```
python3 -m pip install azure.iot.device
```

### Step 3: Get the Creds
Get your OctoPrint API Key [via these instructions](https://docs.octoprint.org/en/master/api/general.html)

Get your IoTHub Connection string [via these instructions]()

### Step 4: Set Environment Variables

In your ~/.bashrc put

```
export IOTHUB_DEVICE_CONNECTION_STRING="YourIoTHubConnectionStringHere"
export OCTOPRINT_API_KEY="YourOctoPrintAPIKeyHere"
```

After saving run 
```source ~/.bashrc```

### Step 5: Run the script!
You can choose to do this in a screen/tmux session

```chmod +x octoprint_iothub.py```

```./octoprint_iothub.py```