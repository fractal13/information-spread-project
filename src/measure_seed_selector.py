#!/usr/bin/env python

import snap
import os, sys, getopt, json
sys.path.append('information_spread')
import random_seed as RS
import compact_community_seed as CCS
import greedy_seed as GS
import independent_cascade as IC


def usage(args):
    print "usage: %s [ --help ]" % (sys.argv[0])
    print "-s|--seed [%s]   : seed type" % (args['seed'], )
    print "-k|--max-k [%s]   : maximum number of seeds" % (args['max-k'], )
    print "-i|--input [%s]   : graph file name" % (args['input'], )
    print "-o|--output [%s]   : file name to store json results" % (args['output'], )
    print "-n|--n-trials [%s]   : number of trials to average over" % (args['n-trials'], )
    print "-p|--spread-probability [%s]   : the probability of spread over a single edge" % (args['spread-probability'], )
    print "-?|-h|--help [%s]  : show this message and exit" % (args['help'], )
    
    return

def main():

    known_seeds = [ "random", "compact", "greedy", ]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:k:i:o:n:p:h?",
                                   [ "src=", "max-k=",
                                     "input=", "output=", "n-trials=", "spread-probability=",
                                     "help", ])
    except getopt.GetoptError as e:
        print str(e)
        usage()
        sys.exit(1)
        
    args = {
        'help': False,
        'seed': "random",
        'max-k': 30,
        'input': 'graph.txt',
        'output': 'results.json',
        'n-trials': 1,
        'spread-probability': 0.05,
    }
    for o, a in opts:
        if o in ("-?", "-h", "--help"):
            args['help'] = True
        elif o in ("-s", "--seed"):
            args['seed'] = a
        elif o in ("-k", "--max-k"):
            args['max-k'] = int(a)
        elif o in ("-i", "--input"):
            args['input'] = a
        elif o in ("-o", "--output"):
            args['output'] = a
        elif o in ("-n", "--n-trials"):
            args['n-trials'] = int(a)
        elif o in ("-p", "--spread-probability"):
            args['spread-probability'] = float(a)
        else:
            print "Unexpected option: %s" % (o)
            usage(args)
            sys.exit(1)

    if args['help']:
        usage(args)
        sys.exit(1)

    if args['seed'] not in known_seeds:
        print "Known seed algorithims: %s" % (" ".join(known_seeds),)
        print "%s isn't one of them." % (args['seed'])
        usage(args)
        sys.exit(1)
        
    if args['max-k'] < 1 or args['max-k'] > 30:
        print "Max K should be in the range 1 - 30."
        usage(args)
        sys.exit(1)

    if not os.path.exists(args['input']):
        print "The input graph file must exist."
        usage(args)
        sys.exit(1)

    if os.path.exists(args['output']):
        print "The output json file must not exist."
        usage(args)
        sys.exit(1)

    if args['n-trials'] < 1:
        print "Must do at least one trial."
        usage(args)
        sys.exit(1)

    if args['spread-probability'] < 0.0 or args['spread-probability'] > 1.0:
        print "The spread probability should be in range 0.0 to 1.0"
        usage(args)
        sys.exit(1)

    run_measurement(args)

    return


def run_measurement(args):
    file_name = args['input']
    if not os.path.exists(file_name):
        print "You must create %s.  Try unzipping the file from the network directory" % (file_name, )
        return

    graph = snap.LoadEdgeList(snap.PNGraph, file_name)
    graph = snap.ConvertGraph(snap.PNEANet, graph)

    number_of_trials = args['n-trials']
    spread_probability = args['spread-probability']
    if args['seed'] == "random":
        selector = RS.RandomSeedSelector()
    elif args['seed'] == "compact":
        selector = CCS.CompactCommunitySeedSelector()
    elif args['seed'] == "greedy":
        selector = GS.GreedySeedSelector()
    else:
        print "Unknown seed selector:", args['seed']
        return

    max_k = args['max-k']

    results = IC.measure_seed_sizes(graph, spread_probability, number_of_trials, selector, max_k)

    fout = open(args['output'], "w")
    fout.write(json.dumps(results, indent=1))
    fout.close()
    return
    
if __name__ == "__main__":
    main()
