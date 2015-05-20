import sys
import fileinput
import os
import ipaddress


def processRoute(line) :
    """Process route"""
    words = line.split()
    temp = words[2] + "/" + words[3]
    if words[2] != "0.0.0.0":
        network = ipaddress.IPv4Network(temp)
        print(network)
    print(temp)

print(os.getcwd())

print(sys.argv)
if len( sys.argv) != 3 :
    print("Usage: \n"
          "     convert <source file> <destfile>\n")
    sys.exit( )

print("ok")

a = ipaddress.IPv4Network("0.0.0.0/0.0.0.0")

b = ipaddress.IPv4Address("10.168.1.0")
print(b.max_prefixlen)
print(a)
#for line in fileinput.input(sys.argv[1]):
#    line = line.strip()
#    if line.startswith("name ") :
#        #print(line)
#        pass
#    elif line.startswith("route "):
#        processRoute(line)
#        print(line)


