#!/usr/bin/python2.7

from customUtilities.helperFunctions import *
from peeringdb import PeeringDB
from contextlib import closing

def getIXPFromPeeringDB(AS):
    pdb = PeeringDB()
    ipList=[]
    retValList=eval(str(pdb.asn(AS)))
    netIXPsList=eval(str(retValList[0]['netixlan_set']))
    for netixp in netIXPsList:
        ipList.append(netixp['ipaddr4'])
    return ipList

if __name__ == "__main__":

    if sys.version_info > (2,8):
        print("ERROR: Please use python2.7. "+str(sys.version_info))
        exit(0)
    asIPDict={}
    with closing(open('asMasterList.txt','r')) as fp:
        for line in fp:
            asIPDict[line]=[]
    for AS in asList:
        asIPDict[line]=getIXPFromPeeringDB(ASN)
        with closing (open('asIXPLanIP.txt','a+')) as wrt:
            print(line+"|"+asIPDict[line])




