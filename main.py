#encoding=utf8
import urllib2
import socket
import random
import struct
import crcmod

crc32c = crcmod.predefined.mkPredefinedCrcFun("crc-32c")

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

def gen_node_id():
    ip = urllib2.urlopen("http://ipecho.net/plain").read()
    print ip
    num_octets = 4
    rand = random.randint(0, 255)
    r = rand & 0x7
    v4mask = "\x03\x0f\x3f\xff"
    ipstr = socket.inet_aton(ip)
    #print "ip", ipstr.encode("hex")
    new_ip = and_two_str(ipstr, v4mask)
    #print "new_ip", new_ip.encode("hex")
    rstr = struct.pack(">I", r << 29)
    final_ip = or_two_str(new_ip, rstr)
    #print "final ip", final_ip.encode("hex")

    crc = crc32c(final_ip)
    #print struct.pack(">I", crc).encode("hex")
    a = (crc>>24) & 0xff
    b = (crc>>16) & 0xff
    c = ((crc>>8) & 0xf8) | (random.randint(0, 255) & 0x7)
    last = rand
    node_id = ''.join([(chr(a)+chr(b)+chr(c)).encode("hex"), ''.join([chr(random.randint(0,255)) for i in xrange(17)]).encode("hex"), chr(rand).encode("hex")])
    return node_id

if __name__ == "__main__":
    print gen_node_id()
