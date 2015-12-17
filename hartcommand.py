


Device = {'ChangeCounter':[00,00],'ExtendStatus':0}                           
                           
Command0_Response = [254,   
                     0x26,0x4E,                     #Expanded Device Type  :  0x264E Rosemount Wireless Gateway   Table 1
                     0x00,                          #Minimun number of Preambles
                     0x07,                          #HART Protocol Major revision
                     0x01,                          #Device Revision Level
                     0x04,                          #Software Revision
                     0x08,                          #Hardware Revision
                     0x06,                          #Physical Signaling Code    0x06:Special (includes, for example, Ethernet, TCP/IP, WiFi, etc.)
                     0x08,                          #Flags 0x08  IEEE 802.15.4 2.4GHz DSSS with O-QPSK Modulation
                     0x00,0x00,0xF0,                #DeviceID
                     0x00,                          #Minimun number of Preambles to be sent
                     0x04,                          #Maximun number of Device Variables
                     Device['ChangeCounter'],       #Configuration Change Counter
                     Device['ExtendStatus'],        #Extended Field Device Status
                     0x60,0x1E,                     #ManufacturerID Microcyber INC.
                     0x60,0x1E,                     #Private Label Distributor Code
                     132,                           #Device Profile  WirelessHART Gateway
                     ]