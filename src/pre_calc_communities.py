#!/usr/bin/env python

import snap
import os, sys, getopt, json, random, time
sys.path.append('information_spread')
import random_seed as RS
import compact_community_seed as CCS
import distance_seed as DST
import independent_cascade as IC
import hueristic_degree_centered_seed as HDCS
import compact_community

def usage(args):
    print "usage: %s [ --help ]" % (sys.argv[0])
    print "-i|--input [%s]   : graph file name" % (args['input'], )
    print "-o|--output [%s]   : file name to store community json" % (args['output'], )
    print "-n|--n-trials [%s]   : number of trials to do" % (args['n-trials'], )
    print "   --lex-count [%s]   : LexDFS repeat count" % (args['lex-count'], )
    print "   --max-iterations [%s]   : community union iteration maximum" % (args['max-iterations'], )
    print "   --max-community-size [%s]   : community union maximum size" % (args['max-community-size'], )
    print "   --community-type [%s]   : community type 1-maxiter 2-maxsize 3-maxunion" % (args['community-type'], )
    print "-?|-h|--help [%s]  : show this message and exit" % (args['help'], )
    
    return

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:n:h?",
                                   [ "input=", "output=", "n-trials=", 
                                     "lex-count=", "max-iterations=", "max-community-size=", "community-type=",
                                     "help", ])
    except getopt.GetoptError as e:
        print str(e)
        usage()
        sys.exit(1)
        
    args = {
        'help': False,
        'input': 'graph.txt',
        'output': 'results.json',
        'n-trials': 1,
        'lex-count': 10,
        'max-iterations': -1,
        'max-community-size': 250,
        'community-type': compact_community.LIMIT_CLUSTER_SIZE,
    }
    for o, a in opts:
        if o in ("-?", "-h", "--help"):
            args['help'] = True
        elif o in ("-i", "--input"):
            args['input'] = a
        elif o in ("-o", "--output"):
            args['output'] = a
        elif o in ("-n", "--n-trials"):
            args['n-trials'] = int(a)
        elif o in ("--lex-count"):
            args['lex-count'] = int(a)
        elif o in ("--max-iterations"):
            args['max-iterations'] = int(a)
        elif o in ("--max-community-size"):
            args['max-community-size'] = int(a)
        elif o in ("--community-type"):
            args['community-type'] = int(a)
        else:
            print "Unexpected option: %s" % (o)
            usage(args)
            sys.exit(1)

    if args['help']:
        usage(args)
        sys.exit(1)

    if not os.path.exists(args['input']):
        print ""
        print "The input graph file must exist."
        print ""
        usage(args)
        sys.exit(1)

    if os.path.exists(args['output']):
        print ""
        print "The output json file must not exist."
        print ""
        usage(args)
        sys.exit(1)

    if args['n-trials'] < 1:
        print ""
        print "Must do at least one trial."
        print ""
        usage(args)
        sys.exit(1)

    build_communities(args)

    return


def build_communities(args):
    file_name = args['input']
    if not os.path.exists(file_name):
        print "You must create %s.  Try unzipping the file from the network directory" % (file_name, )
        return

    graph = snap.LoadEdgeList(snap.PNGraph, file_name)
    graph = snap.ConvertGraph(snap.PNEANet, graph)
    number_of_trials = args['n-trials']
    if args['community-type'] == compact_community.UNTIL_ITERATION:
        parameter = args['max-iterations']
    elif args['community-type'] == compact_community.UNTIL_MAXSIZE:
        parameter = args['max-community-size']
    elif args['community-type'] == compact_community.LIMIT_CLUSTER_SIZE:
        parameter = args['max-community-size']
    else:
        raise Exception("Bad community type")

    results = { 'trials': [],
                'input': file_name,
                'parameter': parameter,
                'community-type': args['community-type'],
                'lex-count': args['lex-count'],
                'average-generation-time': 0.0,
            }

    print "generating ", args['lex-count'], args['community-type'], parameter,
    sys.stdout.flush()
    t0 = time.clock()
    for i in range(args['n-trials']):
        sys.stdout.write("."); sys.stdout.flush()
        communities = compact_community.compact_community(graph, args['lex-count'], args['community-type'], parameter)
        community_list = communities.get_sets()
        results['trials'].append( community_list )
    generation_time = time.clock() - t0
    results['average-generation-time'] = float(generation_time) / float(args['n-trials'])
    print "completed in", generation_time, "seconds, with average", results['average-generation-time']

    fout = open(args['output'], "w")
    fout.write(json.dumps(results, indent=1))
    fout.close()
    return
    
if __name__ == "__main__":
    main()
