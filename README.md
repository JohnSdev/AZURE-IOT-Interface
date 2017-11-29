# AZURE-IOT
WIP
Azure IoT D2C/C2D interface in Python

The purpose of the interface is the simplify Iot implemetation in your own software

User needs to enter own connection string and customize the input/outout parameters

For example
Inputs variables: interface_input_a
If you have an output from a sensor, send that parameter as interface_input_a and it will be sent a to the Iot Hub


iotclient.py is the client that can either simulate a device och take inputs from actual sensors and send them to your Iot Hub.



iotserver.py is a back end app(Or webapp) to send messages/twins/methods to a device.

Dont forget to use your own connections keys

Both applications can be used simultaneously 

I possible to use Device Explorer app to monitor msg data to the hub and/or send messages/methods to the device

