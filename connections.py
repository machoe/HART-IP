import socket


ipList = socket.gethostbyname_ex(socket.gethostname())

'''
判断IP地址是否是有效的IPv4地址
'''
def is_valid_ipv4_address(address):
    try:
        addr= socket.inet_pton(socket.AF_INET, address)
    except AttributeError: # no inet_pton here, sorry
        try:
            addr= socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error: # not a valid address
        return False
    return True

'''
判断IP地址是否是有效的IPv6地址
'''
def is_valid_ipv6_address(address):
    try:
        addr= socket.inet_pton(socket.AF_INET6, address)
    except socket.error: # not a valid address
        return False
    return True

print str(ipList[2][0])

