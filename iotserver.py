
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

#Parts of this code originates from the Microsoft Azure IoT SDK


#Have:
#Change Device Method and recive confirmation
#List devices and preoperties
#Read current twin metadata and send new parameters

#To do:
#Add File upload notification
#List of uploaded files
#View or download files/images



import sys
import iothub_service_client
from iothub_service_client import IoTHubRegistryManager, IoTHubRegistryManagerAuthMethod
from iothub_service_client import IoTHubDeviceMethod, IoTHubError, IoTHubDeviceTwin


#Enter IOTHub credentials
CONNECTION_STRING = ""
#Device name in iot hub
DEVICE_ID = "Recon" 
DEVICE_STATUS=True
METHOD_NAME = "" 
METHOD_PAYLOAD = ""
TIMEOUT = 60
TWIN_MSG = "{\"properties\":{\"desired\":{\"Photointerval\":10}}}"

def iothub_devicetwin():

    iothub_twin_method = IoTHubDeviceTwin(CONNECTION_STRING)
    twin_info = iothub_twin_method.get_twin(DEVICE_ID)
    print ( "" )
    print ( "Device Twin before update    :" )
    print ( "{0}".format(twin_info) )

    twin_info = iothub_twin_method.update_twin(DEVICE_ID, TWIN_MSG)
    print ( "" )
    print ( "Device Twin after update     :" )
    print ( "{0}".format(twin_info) )


def list_devices():
    print ( "GetDeviceList" )
    number_of_devices = 3
    iothub_registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
    dev_list = iothub_registry_manager.get_device_list(number_of_devices)

    number_of_devices = len(dev_list)
    print ( "Number of devices                        : {0}".format(number_of_devices) )

    for device in range(0, number_of_devices):
        title = "Device " + str(device)
        print_device_info(title, dev_list[device])
        if dev_list[device].connectionState != "CONNECTED":
            DEVICE_STATUS=False
        #print(DEVICE_STATUS)
    print ( "" )
    

def print_device_info(title, iothub_device):
    print ( title + ":" )
    print ( "iothubDevice.deviceId                    = {0}".format(iothub_device.deviceId) )
    print ( "iothubDevice.primaryKey                  = {0}".format(iothub_device.primaryKey) )
    print ( "iothubDevice.secondaryKey                = {0}".format(iothub_device.secondaryKey) )
    print ( "iothubDevice.generationId                = {0}".format(iothub_device.generationId) )
    print ( "iothubDevice.eTag                        = {0}".format(iothub_device.eTag) )
    print ( "iothubDevice.connectionState             = {0}".format(iothub_device.connectionState) )
    print ( "iothubDevice.connectionStateUpdatedTime  = {0}".format(iothub_device.connectionStateUpdatedTime) )
    print ( "iothubDevice.status                      = {0}".format(iothub_device.status) )
    print ( "iothubDevice.statusReason                = {0}".format(iothub_device.statusReason) )
    print ( "iothubDevice.statusUpdatedTime           = {0}".format(iothub_device.statusUpdatedTime) )
    print ( "iothubDevice.lastActivityTime            = {0}".format(iothub_device.lastActivityTime) )
    print ( "iothubDevice.cloudToDeviceMessageCount   = {0}".format(iothub_device.cloudToDeviceMessageCount) )
    print ( "iothubDevice.isManaged                   = {0}".format(iothub_device.isManaged) )
    print ( "iothubDevice.configuration               = {0}".format(iothub_device.configuration) )
    print ( "iothubDevice.deviceProperties            = {0}".format(iothub_device.deviceProperties) )
    print ( "iothubDevice.serviceProperties           = {0}".format(iothub_device.serviceProperties) )
    print ( "iothubDevice.authMethod                  = {0}".format(iothub_device.authMethod) )
    print ( "" )
    

class ConnectionError(Exception):
    pass


def methodUpdate(METHOD_NAME, METHOD_PAYLOAD ):
    try:
        
        if DEVICE_STATUS == False:
            raise ConnectionError()
        iothub_device_method = IoTHubDeviceMethod(CONNECTION_STRING)
        
        #Skickar själva meddelandet och tar emot response
        response = iothub_device_method.invoke(DEVICE_ID, METHOD_NAME, METHOD_PAYLOAD, TIMEOUT) 
        #Vad som skickades
        print ( "" )
        print ( "Device Method called" )
        print ( "Device Method name       : {0}".format(METHOD_NAME) ) 
        print ( "Device Method payload    : {0}".format(METHOD_PAYLOAD) )
        print ( "" )
        print ( "Response status          : {0}".format(response.status) ) #200 kan t.ex vara Success
        print ( "Response payload         : {0}".format(response.payload) ) #Själva svaret från devicen. Tex Device starta utan problem
        
            #raise IoTHubDeviceMethodError
    except:
        print("")
        print ( "" )
        print ( "" ) 
        print("Oops!",sys.exc_info()[0],"occured.")
        print("ERROR No deviced connected")
        print("")

def iothub_MainMenu():

    try:
        #Main menu
        while True:      
            
            print ( "" )
            print("1 to list devices ")
            print("2 to Start the service")
            print("3 To Stop the service")
            print("4 To update method")
            inp = int((input()))
            if inp == 1:
                list_devices()
            if inp == 2:
                METHOD_NAME="Start" #Det som skickas
                METHOD_PAYLOAD = "{\"StartService\":\"42\"}"
                methodUpdate(METHOD_NAME, METHOD_PAYLOAD)
            if inp == 3:
                METHOD_NAME="Stop"
                METHOD_PAYLOAD = "{\"StopService\":\"42\"}"
                methodUpdate(METHOD_NAME, METHOD_PAYLOAD)
            if inp == 4:
                iothub_devicetwin()

        
        try:
            # Try Python 2.xx first
            raw_input("Press Enter to continue...\n")
        except:
            pass
            # Use Python 3.xx in the case of exception
            input("Press Enter to continue...\n")

    except IoTHubError as iothub_error:
        print ( "" )
        print ( "Unexpected error {0}".format(iothub_error) )
        return



print ( "IoT Hub Service Interface" )

iothub_MainMenu()
