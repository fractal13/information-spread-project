#!/usr/bin/env python

import os, sys, getopt, json

def usage(args):
    print "usage: %s [ --help ]" % (sys.argv[0])
    print "-i|--input [%s]   : json file name" % (args['input'], )
    print "-?|-h|--help [%s]  : show this message and exit" % (args['help'], )
    
    return

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:h?",
                                   [ "input=", "output=",
                                     "help", ])
    except getopt.GetoptError as e:
        print str(e)
        usage()
        sys.exit(1)
        
    args = {
        'help': False,
        'input': 'results.json',
    }
    for o, a in opts:
        if o in ("-?", "-h", "--help"):
            args['help'] = True
        elif o in ("-i", "--input"):
            args['input'] = a
        else:
            print "Unexpected option: %s" % (o)
            usage(args)
            sys.exit(1)

    if args['help']:
        usage(args)
        sys.exit(1)

    if not os.path.exists(args['input']):
        print ""
        print "The input json file must exist."
        print ""
        usage(args)
        sys.exit(1)

    fin = open(args['input'], "r")
    data = json.load(fin)
    fin.close()

    for d in data:
        for i in d:
            print i,
        print 
    return
    
if __name__ == "__main__":
    main()


