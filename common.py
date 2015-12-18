"""
obj:string
maxlen:fixed length,HCF127-cmd18
Only the tag 6Bytes or 8Packed ASCII
"""
def StrToPackedASCII(obj,maxlen):
    a=[]
    result=[]
    objlen=len(obj)
    if objlen > maxlen:
        return False
    for str in obj:
        #trans to ascii and truncate bit 6 and 7,then put into a list
        a.append((ord(str) & 0x3F))    

    a=a+(maxlen-objlen)*[0x20]    
    #print a
    #cal the list length
    q =len(a)/4

    if q:
        for arry in range(q):
            b=[]
            for num in 0,1,2,3:
                b.append((a[num+(arry*4)]))           
            #print b        
            for num in 0,1,2:
                #print bin(b[num]<<(2*(num+1)))
                #print bin(b[num+1]>>(6-2*(num+1)))
                result.append(((b[num]<<(2*(num+1))) | (b[num+1]>>(6-2*(num+1)))) & 0x000000FF)
    #if r:
        ##no need to repair the list
        #if r == 1:
            #result.append((a[q*4]<<2) & 0x00FD)
        #else:
            ##r==2 r==3 need to repai the list "one" 0
            #a.append(0x20)
            #for num in range(r): 
                ##print bin(a[num+q*4]<<(2*(num+1)))
                ##print bin(a[num+1+q*4]>>(6-2*(num+1)))
                #result.append(((a[num+q*4]<<(2*(num+1))) | (a[num+1+q*4]>>(6-2*(num+1)))) & 0x000000FF)        
    return result

def StrToList(string,width):
    return [int(string[x:x+width],16) for x in range(0,len(string),width)]

def ListtoString(list):
    strList = [str(x) for x in list]
    return ','.join(strList)

def StrToAsciiList(str):
    length = len(str)
    result = []
    for i in range(length):
        result.append(ord(str[i]))
    
    return result
    