from common import *

ManufacturerID     = (0x60,0x1E)
ExpandedDeviceType = (0x26,0x4E)
DeviceID           = (0x00,0x00,0xF0)

Device = {'ChangeCounter':0,
          'Status':0,
          'ExtendStatus':0,
          'Address':(0x80|ExpandedDeviceType[0],ExpandedDeviceType[1],DeviceID[0],DeviceID[1],DeviceID[2]),
          'DeviceOperatingMode':0,
          'DeviceSpecificStatus':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
          'StandardizedStatus0':0,
          'StandardizedStatus1':0,
          'StandardizedStatus2':0,
          'StandardizedStatus3':0,
          } 
                           
Command0_Response = [254,   
                     ExpandedDeviceType[0],         #Expanded Device Type  :  0x264E Rosemount Wireless Gateway   Table 1
                     ExpandedDeviceType[1],
                     0x00,                          #Minimun number of Preambles
                     0x07,                          #HART Protocol Major revision
                     0x01,                          #Device Revision Level
                     0x04,                          #Software Revision
                     0x08,                          #Hardware Revision
                     0x0E,                          #Physical Signaling Code    0x06:Special (includes, for example, Ethernet, TCP/IP, WiFi, etc.)  0x08
                                                    #Flags 0x08  IEEE 802.15.4 2.4GHz DSSS with O-QPSK Modulation                                   0x06
                     DeviceID[0],                   #DeviceID
                     DeviceID[1],
                     DeviceID[2],
                     0x00,                          #Minimun number of Preambles to be sent
                     0x04,                          #Maximun number of Device Variables
                     0,                             #Configuration Change Counter
                     0,
                     Device['ExtendStatus'],        #Extended Field Device Status
                     ManufacturerID[0],             #ManufacturerID Microcyber INC.
                     ManufacturerID[1],
                     ManufacturerID[0],             #Private Label Distributor Code
                     ManufacturerID[1],
                     132,                           #Device Profile  WirelessHART Gateway
                     ]

Command12_Response = 'Microcyber'

Command13_Response = {'Tag':'W','Descriptor':'WIRELESS123','Date':[18,12,2015-1900]}

Command20_Response = 'Microcyber\'s Gateway'

DetectDeviceNum = 1
DRBufferNum = 2
Command74_Response = [
                      0x01,                       #Maximun Number of I/O Cards
                      0x01,                       #Maximum Number of Channels per I/O Card
                      0xF9,                       #Maximum Number of Sub-Devices Per Channel
                      0x00,                       #Number of devices detected 
                      0x01,                                                   #default is 0x01
                      DRBufferNum,                #Maximum number of delayed responses supported by I/O System
                      0x01,                       #Master Mode for communication on channels . 0 = Secondary Master; 1 = Primary Master (default)
                      0x03,                       #Retry Count to use when sending commands to a sub-device. Valid range is 2 to 5. 3 retries is default.
                     ]



def CommandRequest_0(): 
    RC = [0]
    ChangeCounter = FillAlign(Device['ChangeCounter'],2)
    Command0_Response[14] = ChangeCounter[0]
    Command0_Response[15] = ChangeCounter[1]
    return  [len(Command0_Response)+2] + RC + [Device['Status']] + Command0_Response

def CommandRequest_12(): 
    RC = [0]
    datalist = []
    datalist = StrToPackedASCII(Command12_Response,32)
    return  [len(datalist)+2] + RC + [Device['Status']] + datalist

def CommandRequest_13():
    RC = [0]
    datalist = StrToPackedASCII(Command13_Response['Tag'], 8) + StrToPackedASCII(Command13_Response['Descriptor'], 16) + Command13_Response['Date']
    return  [len(datalist)+2] + RC + [Device['Status']] + datalist

def CommandRequest_20():
    RC = [0]
    datalist = StrToAsciiList(Command20_Response)
    datalist = datalist + (32-len(datalist))*[0x20]
    return  [len(datalist)+2] + RC + [Device['Status']] + datalist

def CommandRequest_48():
    RC = [0]
    datalist = Device['DeviceSpecificStatus'][0:6] + [Device['ExtendStatus']] + [Device['DeviceOperatingMode']] + [Device['StandardizedStatus0']] + \
                   [Device['StandardizedStatus0']] + [Device['StandardizedStatus1']] + [0] + [Device['StandardizedStatus2']] +[ Device['StandardizedStatus3']] + [0] + Device['DeviceSpecificStatus'][6:]
    return [len(datalist)+2] + RC + [Device['Status']] + datalist

def CommandRequest_74():
    RC = [0]
    localDetectDeviceNum = FillAlign(DetectDeviceNum,2)
    Command74_Response[3] = localDetectDeviceNum[0]  
    Command74_Response[4] = localDetectDeviceNum[1] 
    return [len(Command74_Response)+2] + RC + [Device['Status']] + Command74_Response

    

HARTCommandRequestFunction = {'0':CommandRequest_0,
                              '12':CommandRequest_12,
                              '13':CommandRequest_13,
                              '20':CommandRequest_20,
                              '48':CommandRequest_48,
                              '74':CommandRequest_74,                              
                              }   
