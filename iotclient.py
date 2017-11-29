# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

#Parts of this code originates from the Microsoft Azure IoT SDK

import random
import time
import sys
import json
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue, IoTHubTwinUpdateState

#def interface_run(message_txt,param_a, param_b,)
#Enter your own credentials!!

#Have:
#Message receive
#Method listener and
#File upload to blob

#To do:
#Add device twin receive and send
#Clarify method handling
#Generec file uploads with date and time stamp




CONNECTION_STRING = ""
# choose HTTP, AMQP or MQTT as transport protocol
DEVICE_ID="Recon"
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
#Variabel that the devices sends in the message
INTERFACE_PARAM_A= 2
# Global Counters
SEND_CALLBACKS = 0
METHOD_CONTEXT = 0
RECEIVE_CONTEXT = 0
METHOD_CALLBACKS = 0
RECEIVE_CALLBACKS = 0
BLOB_CALLBACKS = 0
TWIN_CONTEXT=0


#Message format that is sent with 2 decimals
MSG_TXT = "{\"deviceId\": \"Recon\",\"parameter\": %.2f}"

#File upload to blob container confirmation
def blob_upload_conf_callback(result, user_context):
    global BLOB_CALLBACKS
    print ( "Blob upload confirmation[%d] received for message with result = %s" % (user_context, result) )
    BLOB_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % BLOB_CALLBACKS )

#Confirmation after a message is sent
def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    print ( "    message_id: %s" % message.message_id )
    print ( "    correlation_id: %s" % message.correlation_id )
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    SEND_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_CALLBACKS )

#Initialiation method that creates a client
def iothub_client_init():
    # prepare iothub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    # set the time until a message times out
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    #Turn on and off log tracing for the transport
    client.set_option("logtrace", 0)
    #Anger vilken metod som anropas för att ta emot Method
    client.set_device_method_callback(device_method_callback, METHOD_CONTEXT) 
    #Anger vilken medotd för hantering av meddelanden
    client.set_message_callback(receive_message_callback, RECEIVE_CONTEXT) 
    client.set_device_twin_callback(device_twin_callback, METHOD_CONTEXT)
    #client.upload_blob_async(upload_to_blob, RECEIVE_CALLBACKS)
    return client

    #def upload_to_blob(destinationfilename, source, size, usercontext):
    #    pass
        #client.upload_blob_async(destinationfilename, source, size, blob_upload_conf_callback, usercontext)

#Function to handle method messages. Method messages are a kind of message to control the device. Method contains a name and a payload.
def device_method_callback(method_name, payload, user_context): 
    method=""
    method_response=""
    global METHOD_CALLBACKS
    
    print ( "\nMethod callback called with:\nmethodName = %s\npayload = %s\ncontext = %s" % (method_name, payload, user_context) )
    METHOD_CALLBACKS += 1
    print ( "Total calls confirmed: %d\n" % METHOD_CALLBACKS )
    if method_name == "Start":
        startService()
        method_response="Service Started"
    elif method_name == "Stop":
        stopService()
        method_response="Service Stopped"
    device_method_return_value = DeviceMethodReturnValue()
    #Response to service appplication.
    device_method_return_value.response = "{ \"Response\": \"%s\" }" % (method_response)
    device_method_return_value.status = 200
    return device_method_return_value

#Checks new twin parameters at start and listens to future twin messages
def device_twin_callback(name, payload, user_context):
    print ( "\nTwin callback called with:\nName = %s\npayload = %s\ncontext = %s" % (name, payload, user_context) )
    twin_json = json.loads(payload)
    new_param_dict=next(iter (twin_json.values()))
    new_param=next(iter (new_param_dict.keys()))
    print(new_param)
    new_interval=twin_json["desired"][new_param]
    if "Photointerval" in payload:
        print("Setting {} to {}".format( new_param , new_interval))

def startService():
    #Add HW dependadt code
    return "Service Started"

def stopService():
    #Add HW dependadt code
    return "Service Stopped"




#Function that handles received messages
def receive_message_callback(message, counter): 
    global RECEIVE_CALLBACKS
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    print ( "Received Message [%d]:" % counter )
    print ( "    Data: <<<%s>>> & Size=%d" % (message_buffer[:size].decode('utf-8'), size) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    counter += 1
    RECEIVE_CALLBACKS += 1
    print ( "    Total calls received: %d" % RECEIVE_CALLBACKS )
    return IoTHubMessageDispositionResult.ACCEPTED


#Main program
def iothub_client(): 

    try:
        #Initialice Client
        client = iothub_client_init()
        
        print ( "IoT Device Simulator, press Ctrl-C to exit" )
        #Specifies message format and values
        msg_txt_formatted = MSG_TXT % INTERFACE_PARAM_A
        message_counter = 0
        inp = 0
        while inp != 4:
            print("Press 1 to send a message to IOT Hub (Simulated message")
            print("Press 2 to send a picture to IOT Hub (Simulated message")
            print("Press 4 to EXIT")
            
            # messages can be encoded as string or bytearray

            if (message_counter & 1) == 1:
                message = IoTHubMessage(bytearray(msg_txt_formatted, 'utf8'))
            else:
                message = IoTHubMessage(msg_txt_formatted)
            # optional: assign ids
            message.message_id = "message_%d" % message_counter
            message.correlation_id = "correlation_%d" % message_counter
            # optional: assign properties
            prop_map = message.properties()
            prop_text = "PropMsg_%d" % message_counter
            prop_map.add("Property", prop_text)
            inp = int(input())
            if inp == 1:
                #Sends a message to the Hub, reveives confirmation callback, adds counter
                client.send_event_async(message, send_confirmation_callback, message_counter)
                print ( "IoTHubClient.send_event_async accepted message [%d] for transmission to IoT Hub." % message_counter )
            if inp == 2:
                #Sends a file to Azure Storage Blob
                filename = "hello.jpg"
                content1 = open(filename, "rb")
                content = content1.read()
                #Send and shows confirmation
                client.upload_blob_async(filename, content, len(content), blob_upload_conf_callback, 1001)
                
            
            #status = client.get_send_status()
            #print ( "Send status: %s" % status )
   
            message_counter += 1
            if inp == 4:
                break

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

#Starts the program
#Function to call efter import
iothub_client()  
