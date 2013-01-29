#!/usr/bin/env python
# 
# Prints faction of escalators outage in the New York city subway system with reason repair.
#
# Thomas Schmitt thms.schmitt@gmail.com
# 

from __future__ import print_function
import sys
import getopt

from schmitt import loadEscalatorOutage
from schmitt import countEscalatorOutageReason

def main(options,argv):
    """Prints faction of escalators outage in the New York city subway system with reason repair."""
    
    try:
        esculatorOutage = loadEscalatorOutage()
    except Exception as e:
        print("Unable to load escalators outage status.",file=sys.stderr)
        print(e,file=sys.stderr)
        exit(-1)

    try:
        repair,total = countEscalatorOutageReason(esculatorOutage)
    except Exception as e:
        print("Invalid outage status.",file=sys.stderr)
        print(e,file=sys.stderr)
        exit(-1)

    print('Total outages: %d, outages with reason "Repair": %d, fraction: %f' %(total,repair,float(repair)/total))


def _printHelpAndExit():
    
    print("USAGE:  %s" % (sys.argv[0]),file=sys.stderr)
    print("Prints the faction of outages of escalators in the NYC subway system caused by repairs.\n",file=sys.stderr)
    print("  -h  or --help",file=sys.stderr)
    print("              shows this help text",file=sys.stderr)
    exit(-1) 


if __name__ == "__main__":

    try:
        options,argv = getopt.getopt(sys.argv[1:],"h",["help"])
        options = dict(options)
    except:
        _printHelpAndExit()

    if "-h" in options:
        _printHelpAndExit()
    
    main(options,argv)
    