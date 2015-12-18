import struct
from hartcommand import *

Length = {'Total':8,'VerLen':1,'MesTypeLen':1,'MesIDLen':1,'StatusCodeLen':1,'SeqNumLen':2,'ByteCountLen':2}

Version = 1

MessageType = {'Request':0,'Response':1,'Pub_Noti':12,'Nak':15}

MessageID   = {'SessionInitiate':0,'SesstionClose':1,'KeepAlive':2,'TPPDU':3,'Discovery':128}

StatusCode = ''

SequenceNumber = ''

ByteCount = ''



def ReceiveFromSocket(data,client):
    #Calculate the data length from the socket received
    RecLength = len(data)    
    
    RecFmt = str(RecLength)+'B' 
    print  struct.unpack(RecFmt,data)
         
    Header = ProcessHeader(data[0:8])
    if Header['Status'] == True:
        
        MesHeader =  Header['RecHeader']
        
        
        if MesHeader['RecMesType'] == 0:                                 #Request
            
            if MesHeader['RecMesID'] == 0:     #Session Initiate  
                print 'Session initiate'
                SessionReq = {'MasterType':'','InactivityCloseTime':''}
                SessionReq['MasterType']            = struct.unpack('B',data[8])[0]
                SessionReq['InactivityCloseTime']   = struct.unpack('!I',data[9:13])[0]   #Milliseconeds
                
                #response to initiate
                ResData =''
                ResData += struct.pack('B',SessionReq['MasterType'])
                ResData += struct.pack('!I',SessionReq['InactivityCloseTime'])
                client.send(ResponseToRequest(Version,0,0,MesHeader['RecSecNum'],ResData))              
            
            elif MesHeader['RecMesID'] == 1:   #Session Close
                print 'Session Close'
            
            elif MesHeader['RecMesID'] == 2:   #Keep Alive
                print 'Keep Alive'
           
            elif MesHeader['RecMesID'] == 3:   #Token-Passing PDU
                print 'Token-Passing PDU'
                TPLength = MesHeader['RecByteCount'] - 8
                try:
                    RC,resBinary = ProcessTPPDURequest(data[8:RecLength],client)
                except Exception as e:
                    RC = False
                if RC == True:
                    client.send(ResponseToRequest(Version,3,0,MesHeader['RecSecNum'],resBinary))              
                
            elif MesHeader['RecMesID'] == 128: #Discovery
                print 'Discovery'
            
            else:                              #Error occur
                print 'err message type :'+ MesHeader['RecMesID']
              
      
        elif MesHeader['RecMesType'] == 1:                               #Response
            pass
        elif MesHeader['RecMesType'] == 2:                               #Publish/Notification
            pass
        elif MesHeader['RecMesType'] == 15:                              #NAK
            pass
        else:                                                            #Error occur
            print 'err message type :'+ MesHeader['RecMesType']
        
    
        
def ProcessHeader(data):
    RecHeader = {'RecVersion':'','RecMesType':'','RecMesID':'','RecStatusCode':'','RecSecNum':'','RecByteCount':''}
    Res = {'Status':'False','RecHeader':RecHeader}

    if len(data) != 8:
        return Res
    
    try:
        RecHeader['RecVersion']    = struct.unpack('B',data[0])[0]
        RecHeader['RecMesType']    = struct.unpack('B',data[1])[0]
        RecHeader['RecMesID']      = struct.unpack('B',data[2])[0]
        RecHeader['RecStatusCode'] = struct.unpack('B',data[3])[0]
        RecHeader['RecSecNum']     = struct.unpack('!H',data[4:6])[0]
        RecHeader['RecByteCount']  = struct.unpack('!H',data[6:8])[0] 
        Res['Status'] = True
    except Exception as E:
        print E
    
    return Res

def ResponseToRequest(ver,MesID,Status,SeqNum,data):
    return AssemblePacket(ver, MessageType['Response'], MesID, Status, SeqNum, data)
    
def AssemblePacket(ver,Mestype,MesID,Status,SeqNum,data):
    frame = ''
    length = 8
    newdata = []
    datalength = len(data)
    length += datalength
    
    try:    
        frame+=struct.pack('B',ver)
        frame+=struct.pack('B',Mestype)
        frame+=struct.pack('B',MesID)
        frame+=struct.pack('B',Status)
        frame+=struct.pack('!H',SeqNum)
        frame+=struct.pack('!H',length)
        frame+=data
    except Exception as e:
        print e
    
    return frame


def ProcessTPPDURequest(data,client):
    datalist = list(struct.unpack(str(len(data))+'B',data))
    recCheck = datalist.pop()
    if recCheck == CheckSum(datalist):
        Delimiter = datalist[0]
        if Delimiter == 0x02:                                   #Polling Request
            
            cmdres = CommandRequest_0()
            cmd0 = [0]
            res = cmd0 + cmdres
            resDelimiter = 0x06
            addr = [128]
            resList = [resDelimiter] + addr + res
            resList.append(CheckSum(resList))
            return True,ListToBinary(resList)
        elif Delimiter == 0x82:                                 #Long Address Request
            addr = struct.unpack('!5B',data[1:6])
            if addr == Device['Address']:
                recCmdID = datalist[6]
                recCmdLength = datalist[7]                
                try:
                    if HARTCommandRequestFunction.has_key(str(recCmdID)):
                        print 'Command' , recCmdID
                        if recCmdLength == 0:
                            resCommand = HARTCommandRequestFunction[str(recCmdID)]()                   
                        else:
                            resCommand = HARTCommandRequestFunction[str(recCmdID)](datalist[7:])
                    else:
                        print 'No this command',recCmdID
                        resCommand = [64]   # Response Code, No payloads
                except Exception as e:
                    resCommand = [64]   # problem occur
                
                res = [recCmdID] + resCommand
                    
                resDelimiter = 0x86
                addr = [166,78,0,0,240]
                resList = [resDelimiter] + addr + res
                resList.append(CheckSum(resList))
                return True,ListToBinary(resList)        
            else:
                print 'Delimiter is error'
                return 
        else:   #checksum is error
            print checksum is error
            return
    else:
        print 'wrong request is receive' + Delimiter
        return 
    
def ListToBinary(InputList):
    str = ''
    for i in range(len(InputList)):
        str += struct.pack('B',InputList[i])        
    return str

def CheckSum(InputList):
    Check = InputList[0]
    for i in range(1,len(InputList)):
        Check ^= InputList[i]
        
    return Check