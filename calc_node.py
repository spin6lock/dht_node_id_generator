import socket
import random
import struct
import sys

ip = sys.argv[1]
rand = int(sys.argv[2])
num_octets = 4
r = rand & 0x7
v4mask = "\x03\x0f\x3f\xff"
ipstr = socket.inet_aton(ip)
#print "ip", ipstr.encode("hex")
def and_two_str(a, b):
    tmp = []
    for i in xrange(4):
        t = chr(ord(a[i]) & ord(b[i]))
        #print ord(a[i]) , ord(b[i]), t
        tmp.append(t)
    return ''.join(tmp)
def or_two_str(a,b):
    tmp = []
    for i in xrange(4):
        t = chr(ord(a[i]) | ord(b[i]))
        #print ord(a[i]) , ord(b[i]), t
        tmp.append(t)
    return ''.join(tmp)
new_ip = and_two_str(ipstr, v4mask)
#print "new_ip", new_ip.encode("hex")
#final_ip = chr(ord(new_ip[0]) | r<<5) + new_ip[1:]
rstr = struct.pack(">I", r << 29)
final_ip = or_two_str(new_ip, rstr)
#print "final ip", final_ip.encode("hex")

import crcmod
crc32c = crcmod.predefined.mkPredefinedCrcFun("crc-32c")
crc = crc32c(final_ip)
#print struct.pack(">I", crc).encode("hex")
a = (crc>>24) & 0xff
b = (crc>>16) & 0xff
c = ((crc>>8) & 0xf8) | (random.randint(0, 255) & 0x7)
last = rand
print rand, (chr(a)+chr(b)+chr(c)).encode("hex"), ''.join([chr(random.randint(0,255)) for i in xrange(17)]).encode("hex"), chr(rand).encode("hex")
