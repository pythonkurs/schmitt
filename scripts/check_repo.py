#!/usr/bin/env python
#
# Thomas Schmitt thms.schmitt@gmail.com
# 

from __future__ import print_function
import sys
import getopt
import os.path

from schmitt.session3 import CourseRepo, directoryContext

def main(options,argv):

    if len(argv) != 1:
        _printHelpAndExit()
        
    workDir = argv[0]
    
    if not os.path.isdir(workDir):
        print("{} doesn't exist or isn't a directory.".format(workDir),file=sys.stderr)
        exit(-1)
    
    surname = os.path.basename(os.path.normpath(workDir))
    
    repo = CourseRepo(surname)
    
    with directoryContext(workDir):
        if repo.check():
            print("PASS")
        else:
            print("FAIL")
    
    

def _printHelpAndExit():
    
    print("USAGE: {} REPO_DIR".format(os.path.basename(sys.argv[0])),file=sys.stderr)
    print("Checks if the course repository contains all required files for session 3.\n",file=sys.stderr)
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
    