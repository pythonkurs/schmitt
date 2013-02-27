#!/usr/bin/env python
#
# Thomas Schmitt thms.schmitt@gmail.com
# 

from __future__ import print_function
import sys
import argparse
import multiprocessing
from collections import Counter
from IPython.parallel import Client
from schmitt import session7
import itertools

def main(args,printHelp):
    """ Prints a 'histogram' of the times unique counts factors """
    runMode = { "s" : serial, "m" : multiproc , "i" : parallel }
    
    mode=args.args[0].lower()
    start = args.start
    end = args.end + 1
    
    if mode not in runMode or start < 1 or end < start:
        printHelp()
        
    numUniqFactors = runMode[mode](start,end)
    c = Counter((numUniqFactors))
    print(dict(c))
    
    
def serial(start,end):
    """ Counts the unique factors for all numbers from start to end  in a serial fashion"""
    return (uniqFactors(n) for n in xrange(start,end))
    
    
def multiproc(start,end):
    """ Counts the unique factors for all numbers from start to end using the multiprocessing module"""
    numCores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=numCores)    
    return pool.map(uniqFactors,xrange(start,end))
    
    
def parallel(start,end):
    """ Counts the unique factors for all numbers from start to end using the ipython.parallel module.
        Why is this so slow? """
    client = Client()
    view = client[:]
     
    with view.sync_imports():
       from schmitt import session7

    view.scatter("nList", xrange(start,end))
    asyncResult =  view.apply_async(uniqMultiFactors)
    return itertools.chain.from_iterable(asyncResult.get())
    

def uniqMultiFactors():
    """ Counts the unique factors for all n in nList"""
    return [ len(set(session7.factorize(n))) for n in nList ]


def uniqFactors(n):
    """ Counts the unique factors for the number n"""
    factors = session7.factorize(n)
    return len(set(factors))

    
if __name__ == "__main__":

    argParser = argparse.ArgumentParser(description='Process description ...')
    argParser.add_argument('args', metavar='M', type=str, nargs=1, help='mode: s=serial m=multiprocessing i=IPython.parallel')
    argParser.add_argument('-s','--start',default=2,type=int,help='first number to factorize')
    argParser.add_argument('-e','--end',default=500000,type=int,help='last number to factorize')
    
    def printHelp():
        argParser.print_help(sys.stderr)
        exit(-1)

    main(argParser.parse_args(),printHelp)
    