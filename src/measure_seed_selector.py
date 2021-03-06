#!/usr/bin/env python

import snap
import os, sys, getopt, json
sys.path.append('information_spread')
import random_seed as RS
import compact_community_seed as CCS
import distance_seed as DST
import independent_cascade as IC
import hueristic_degree_centered_seed as HDCS
import greedy_hill_climbing_seed as GHCS
import compact_community


def usage(args):
    print "usage: %s [ --help ]" % (sys.argv[0])
    print "-s|--seed [%s]   : seed type" % (args['seed'], )
    print "-k|--max-k [%s]   : maximum number of seeds" % (args['max-k'], )
    print "-i|--input [%s]   : graph file name" % (args['input'], )
    print "-o|--output [%s]   : file name to store json results" % (args['output'], )
    print "-n|--n-trials [%s]   : number of trials to average over" % (args['n-trials'], )
    print "-p|--spread-probability [%s]   : the probability of spread over a single edge" % (args['spread-probability'], )
    print "   --lex-count [%s]   : LexDFS repeat count" % (args['lex-count'], )
    print "   --max-iterations [%s]   : community union iteration maximum" % (args['max-iterations'], )
    print "   --max-community-size [%s]   : community union maximum size" % (args['max-community-size'], )
    print "   --community-type [%s]   : community type 1-maxiter 2-maxsize 3-maxunion" % (args['community-type'], )
    print "   --community-file [%s]   : file with pre-calculated communities" % (args['community-file'], )
    print "   --community-choice [%s]  : how to choose next community 1-random 2-rotate 3-biggest" % (args['community-choice'], )
    print "-?|-h|--help [%s]  : show this message and exit" % (args['help'], )
    
    return

def main():

    known_seeds = [ "random", "compactdegree", "compactdistance", "distance", "distanceFW", "distanceBFS", "degree", "greedy", "compactgreedy" ]

    args = {
        'help': False,
        'seed': "random",
        'max-k': 30,
        'input': 'graph.txt',
        'output': 'results.json',
        'n-trials': 1,
        'spread-probability': 0.05,
        'lex-count': 10,
        'max-iterations': -1,
        'max-community-size': 250,
        'community-type': compact_community.LIMIT_CLUSTER_SIZE,
        'community-file': None,
        'community-choice': 2,
    }
    
    try:
        opts, noargs = getopt.getopt(sys.argv[1:], "s:k:i:o:n:p:h?",
                                     [ "seed=", "max-k=",
                                       "input=", "output=", "n-trials=", "spread-probability=",
                                       "lex-count=", "max-iterations=", "max-community-size=",
                                       "community-type=", "community-file=", "community-choice=",
                                       "help", ])
    except getopt.GetoptError as e:
        print str(e)
        usage(args)
        sys.exit(1)
        
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
        elif o in ("--lex-count"):
            args['lex-count'] = int(a)
        elif o in ("--max-iterations"):
            args['max-iterations'] = int(a)
        elif o in ("--max-community-size"):
            args['max-community-size'] = int(a)
        elif o in ("--community-type"):
            args['community-type'] = int(a)
        elif o in ("--community-file"):
            args['community-file'] = a
        elif o in ("--community-choice"):
            args['community-choice'] = int(a)
        else:
            print "Unexpected option: %s" % (o)
            usage(args)
            sys.exit(1)

    if args['help']:
        usage(args)
        sys.exit(1)

    if args['seed'] not in known_seeds:
        print ""
        print "Known seed algorithims: %s" % (" ".join(known_seeds),)
        print "%s isn't one of them." % (args['seed'])
        print ""
        usage(args)
        sys.exit(1)
        
    if args['max-k'] < 1 or args['max-k'] > 30:
        print ""
        print "Max K should be in the range 1 - 30."
        print ""
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

    if args['spread-probability'] < 0.0 or args['spread-probability'] > 1.0:
        print ""
        print "The spread probability should be in range 0.0 to 1.0"
        print ""
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
    elif args['seed'] == "compactdegree":
        selector = CCS.CompactCommunityDegreeSeedSelector()
        selector.setLexCount(args['lex-count'])
        selector.setMaxIterations(args['max-iterations'])
        selector.setMaxCommunitySize(args['max-community-size'])
        selector.setCommunityType(args['community-type'])
        selector.setCommunityFile(args['community-file'])
        selector.setCommunityChoiceType(args['community-choice'])
    elif args['seed'] == "compactdistance":
        selector = CCS.CompactCommunityDistanceSeedSelector()
        selector.setLexCount(args['lex-count'])
        selector.setMaxIterations(args['max-iterations'])
        selector.setMaxCommunitySize(args['max-community-size'])
        selector.setCommunityType(args['community-type'])
        selector.setCommunityFile(args['community-file'])
        selector.setCommunityChoiceType(args['community-choice'])
    elif args['seed'] == "compactgreedy":
        selector = CCS.CompactCommunityGreedyHillClimbingSeedSelector()
        selector.setLexCount(args['lex-count'])
        selector.setMaxIterations(args['max-iterations'])
        selector.setMaxCommunitySize(args['max-community-size'])
        selector.setCommunityType(args['community-type'])
        selector.setCommunityFile(args['community-file'])
        selector.setCommunityChoiceType(args['community-choice'])
        selector.setSpreadProbability(spread_probability)
    elif args['seed'] == "distance":
        selector = DST.DistanceSeedSelector()
    elif args['seed'] == "distanceFW":
        selector = DST.FWDistanceSeedSelector()
    elif args['seed'] == "distanceBFS":
        selector = DST.BFSDistanceSeedSelector()
    elif args['seed'] == "degree":
        selector = HDCS.DegreeCenteredSeedSelector()
    elif args['seed'] == "greedy":
        selector = GHCS.GreedyHillClimbingSeedSelector()
        selector.setSpreadProbability(spread_probability)
    else:
        print "Unknown seed selector:", args['seed']
        return

    max_k = args['max-k']

    results = IC.measure_seed_sizes(graph, spread_probability, number_of_trials, selector, max_k, args['output'])

    fout = open(args['output'], "w")
    fout.write(json.dumps(results, indent=1))
    fout.close()
    return
    
if __name__ == "__main__":
    main()
