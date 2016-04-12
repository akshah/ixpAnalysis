#!/usr/bin/python3

from customUtilities.helperFunctions import *
from customUtilities.logger import logger
from contextlib import closing
import configparser
import getopt
import pymysql
import traceback
import pprint
from peeringdb import PeeringDB
from geoInfo.MaxMindRepo import MaxMindRepo


def usage(msg="Usage"):
    print(msg)
    print('python3 '+sys.argv[0]+' [-l LOGFILE] -c CONFIG_FILE [-h]')
    sys.exit(2)

def getIXPFromPeeringDB(AS):
    pdb = PeeringDB()
    countriesSet=set()
    retValList=eval(pdb.asn(AS))
    netIXPsList=eval(retValList[0]['netixlan_set'])
    for netixp in netIXPsList:
        localCountrySet=mm.ipToCountry(netixp['ipaddr4'])
        for ct in localCountrySet:
            countriesSet.add(ct)
    return countriesSet

def getIXPList(db,AS):
    ixpDict={}
    with closing(db.cursor()) as cur:
        try:
            query = "SELECT p.ID,ASn,ShortName,Name,City,Country,Continent FROM participants p ,ixps i where  p.ID=i.ID and ASn = '{0}'".format(AS)
            cur.execute(query)
            row = cur.fetchone()
            while row is not None:
                (ixpid,asn,shortName,name,city,country,continent)=row
                ixpDict[ixpid]={}
                ixpDict[ixpid]['asn']=asn
                ixpDict[ixpid]['shortName']=shortName
                ixpDict[ixpid]['name']=name
                ixpDict[ixpid]['city']=city
                ixpDict[ixpid]['country']=country
                ixpDict[ixpid]['continent']=continent
                row = cur.fetchone()
        except:
            logger.error('IXP fetch failed!')
    return ixpDict

def getCountriesFromIXPDict(ixpDict):
    countrySet=set()
    for ixpID in ixpDict.keys():
        countrySet.add(ixpDict[ixpID]['country'])
    return countrySet

if __name__ == "__main__":

    if sys.version_info < (3,0):
        print("ERROR: Please use python3.")
        exit(0)

    logfilename=None
    configfile=None
    ASN=None

    try:
        opts,args = getopt.getopt(sys.argv[1:],'c:a:h',['configfile','asn','help'])
    except getopt.GetoptError:
        usage('GetoptError: Arguments not correct')

    for opt,arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-c', '--configfile'):
            configfile = arg
        elif opt in ('-a', '--asn'):
            ASN = arg

    if not ASN:
        print('Give an ASN.')
        exit(0)

    #Load config file
    if not configfile:
        configfile="conf/ixpAnalysis.conf"
    config = configparser.ConfigParser()
    try:
        config.sections()
        config.read(configfile)
    except:
        print('Missing config: ' + configfile)
        exit(0)

    #Logger
    try:
        logfilename = config['DEFAULT']['logDir']+'/'+config['DEFAULT']['logFile']
    except:
        scriptname=sys.argv[0].split('.')
        logfilename=scriptname[0]+'.log'
    logger=logger(logfilename)

    mm=MaxMindRepo('')

    try:
        db = pymysql.connect(host=config['MySQL']['serverIP'],
                                  port=int(config['MySQL']['serverPort']),
                                  user=config['MySQL']['user'],
                                  passwd=config['MySQL']['password'],
                                  db=config['MySQL']['dbname'])
        logger.info('Test connection to MySQL server on ' + config['MySQL']['serverIP'] + ":" + config['MySQL']['serverPort'] + ' successful.')
        #Lookup AS

        ixpDict=getIXPList(db,ASN)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(ixpDict)
        countriesSet=getCountriesFromIXPDict(ixpDict)
        pp.pprint(countriesSet)
        db.close()
        countriesFromPeerinDB=getIXPFromPeeringDB(ASN)
        pp.pprint(countriesFromPeerinDB)
    except:
        traceback.print_exc()
        logger.warn('DB connection not valid.')



