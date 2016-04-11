#!/usr/bin/python3

from customUtilities.helperFunctions import *
from customUtilities.logger import logger
import configparser
import getopt

def usage(msg="Usage"):
    print(msg)
    print('python3 '+sys.argv[0]+' [-l LOGFILE] -c CONFIG_FILE [-h]')
    sys.exit(2)

def getIXPList(db,AS):
    ixpList=[]
    with closing(db.cursor()) as cur:
        try:
            query = "SELECT p.ID,ASn,ShortName,Name,City,Country,Continent FROM participants p ,ixps i where  p.ID=i.ID and ASn = '{0}'".format(AS)
            cur.execute(query)
            row = cur.fetchone()
            while row is not None:
                ixpList.append(row)
                row = cur.fetchone()
        except:
            logger.error('IXP fetch failed!')
    return ixpList

if __name__ == "__main__":

    if sys.version_info < (3,0):
        print("ERROR: Please use python3.")
        exit(0)

    logfilename=None
    configfile=None

    try:
        opts,args = getopt.getopt(sys.argv[1:],'c:h',['configfile','help'])
    except getopt.GetoptError:
        usage('GetoptError: Arguments not correct')

    for opt,arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-c', '--configfile'):
            configfile = arg

    #Load config file
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


    try:
        db = pymysql.connect(host=config['MySQL']['serverIP'],
                                  port=int(config['MySQL']['serverPort']),
                                  user=config['MySQL']['user'],
                                  passwd=config['MySQL']['password'],
                                  db=config['MySQL']['dbname'])
        logger.info('Test connection to MySQL server on ' + config['MySQL']['serverIP'] + ":" + config['MySQL']['serverPort'] + ' successful.')
        #Lookup AS
        AS="210"

        ixpList=getIXPList(db,AS)
        print(ixpList)
        db.close()
    except:
        logger.warn('DB connection not valid.')



