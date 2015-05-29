'''
Created on May 20, 2015

@author: yhuang
'''
import ipaddress
import SubnetTree
import sys
import fileinput
#import os
#import linecache

from _functools import reduce
from ipaddress import AddressValueError

    
if len( sys.argv) != 3 :
    print("Usage: \n"
          "     convert <source file> <destfile>\n")
    sys.exit( )

print("ok")

namelst = []
routelst = []
accesslst = []

cGType = ""
cGName = ""

netGLst = []
serviceGLst = []
protocolLst = []

for line in fileinput.input(sys.argv[1]):
    line = line.strip()
    if line.startswith("name ") :
        namelst.append(line)
    elif line.startswith("route "):
        routelst.append(line)
    elif line.startswith("access-list "):
        accesslst.append(line)
    elif line.startswith("object-group "):
        words = line.split()
        cGType = words[1]
        cGName = words[2] 
        if cGType == "network":
            netGLst.append( (cGName, []))
        elif cGType == "service":
            serviceGLst.append( (cGName, []))
        elif cGType == "protocol":
            protocolLst.append( (cGName, []))
    elif line.startswith("description"):
        pass
    elif line.startswith("network-object") and cGType == "network":
        if netGLst[-1][0] == cGName:
            netGLst[-1][1].append( line)
    elif line.startswith("port-objec") and cGType == "service":
        if serviceGLst[-1][0] == cGName:
            serviceGLst[-1][1].append(line)
    elif line.startswith("protocol-object") and cGType == "protocol":
        if protocolLst[-1][0] == cGName:
            protocolLst[-1][1].append(line)
    elif line.startswith("group-object"):
        if cGType == "network" and netGLst[-1][0] == cGName:
            netGLst[-1][1].append( line)
        elif cGType == "service" and serviceGLst[-1][0] == cGName:
            serviceGLst[-1][1].append(line)
        elif cGType == "protocol" and protocolLst[-1][0] == cGName:
            protocolLst[-1][1].append(line)


## Load all names
names = { k: v for d in list( map( lambda x: {x.split()[2]: x.split()[1]}, namelst ) ) for k, v in d.items() }
 
## Load all routes
def addRouteByNames(routelst, names):
    def addRoute(rs, line):
        words = line.split()
        if words[2] in names:
            rs[ipaddress.IPv4Network(names[words[2]] + "/" + words[3]).compressed] = words[1]
        else:
            rs[ipaddress.IPv4Network(words[2] + "/" + words[3]).compressed] = words[1]
     
        return rs
 
    return reduce( addRoute, routelst, SubnetTree.SubnetTree())
 
 
routes = addRouteByNames(routelst, names)
 
# try:
#     print(routes["137.172.26.140"])
# except KeyError as err:
#     print("Error: %s not found" % err)
     
print("load object groups")     
## Load all network object groups
netGs = {}
for t in netGLst:
    gn = t[0]
    ip = ""
    for line in t[1]:
        words = line.split()
        if words[0] == "network-object":
            if words[1] == "host":
                if words[2] in names:
                    ip = names[words[2]]
                else:
                    ip = words[2]
                if ip in routes:
                        netGs[t[0] ] = routes[ ip]            
                break
            else:
                try:
                    if words[1] in names:
                        ip = ipaddress.IPv4Network( names[words[1] ] + "/" + words[2]).compressed
                    else:
                        ip = ipaddress.IPv4Network( words[1] + "/" + words[2]).compressed
                    if ip in routes:
                            netGs[t[0] ] = routes[ ip]            
                    break
                except KeyError as err:
                    print("Error: %s not found" % err)
        elif words[0] == "group-object":
            if words[1] in netGs:
                netGs[t[0] ] = netGs[words[1] ]
            break

# for k,v in netGs.items():
#     print(k)
#     print(v)
    
print( "Legato_Backup_Hosts" in netGs)
print("DMZ2_Legato_Backup_Hosts" in netGs)
print(netGs["DMZ2_Legato_Backup_Hosts"])


outf = open(sys.argv[2] + ".debug", "w")
destf = open(sys.argv[2] , "w")

for line in accesslst:
    words = line.split()
    sr = ""
    dr = ""
    port = ""
    #print(line)
    if words[5] == "any" or words[4] not in ["udp","tcp"]:
        outf.write("Exception(Any, not udp/tcp). original=%s\n" % line)
        continue
    if words[5] == "host":
        sr = routes[ names[ words[6] ] ]
    elif words[5] == "object-group":
        sr = netGs[ words[6] ]
    else:
        if words[5] in names:
            sr = routes[ ipaddress.IPv4Network( names[ words[5]] +"/" + words[6]).compressed ]
        else:
            sr = routes[ ipaddress.IPv4Network( words[5] +"/" + words[6]).compressed ]
    if words[7] in ["any", "eq"] or sr =="":
        outf.write("Exception(Any) or source ip =%s. original=%s\n" % (sr, line) )
        continue
    if words[7] == "host":
        if words[8] in names:
            dr = routes[ names[ words[8] ] ]
        else:
            try:
                dr = routes[ ipaddress.IPv4Address( words[8]).compressed ]
            except AddressValueError as err:
                outf.write("Exception(Can't find host %s). original=$s\n" % (err, line) )
                continue
    elif words[7] == "object-group":
        dr = netGs[ words[8] ]
    else:
        if words[7] in names:
            dr = routes[ ipaddress.IPv4Network( names[ words[7]] +"/" + words[8]).compressed ]
        else:
            dr = routes[ ipaddress.IPv4Network( words[7] +"/" + words[8]).compressed ]
    
    if len(words) <= 9:
        outf.write("Exception(No port). original=%s\n" % (line) )
        continue
        
    if words[9] in ["eq"]:
        port = words[10]
    elif words[9] in ["object-group"]:
        port = words[10]
    else:
        port = words[9]
    
    outf.write("Good original=%s\n" % line)
    outf.write("    policy: %s protocol:%s action:%s source:%s dest:%s port=%s.\n" % (words[1], words[4], words[3], sr, dr, port) )
    
    
     

outf.close()
destf.close()




