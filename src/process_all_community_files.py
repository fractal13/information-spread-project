#!/usr/bin/env python

import os, sys, getopt, re

def usage(args):
    print "usage: %s [ --help ]" % (sys.argv[0])
    print "-d|--directory [%s] : directory to find the files in" % (args['directory'], )
    print "-?|-h|--help [%s]  : show this message and exit" % (args['help'], )
    
    return

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:h?",
                                   [ "directory=",
                                     "help", ])
    except getopt.GetoptError as e:
        print str(e)
        usage()
        sys.exit(1)
        
    args = {
        'help': False,
        'directory': ".",
    }
    for o, a in opts:
        if o in ("-?", "-h", "--help"):
            args['help'] = True
        elif o in ("-d", "--directory"):
            args['directory'] = a
        else:
            print "Unexpected option: %s" % (o)
            usage(args)
            sys.exit(1)

    if args['help']:
        usage(args)
        sys.exit(1)

    if not os.path.exists(args['directory']):
        print ""
        print "The directory doesn't exist."
        print ""
        usage(args)
        sys.exit(1)

    process_files(args)

    return

def process_files(args):
    all_files = os.listdir(args['directory'])
    files = []
    for f in all_files:
        match = re.match('^fbc-trials:([0-9]+)-lexcount:([0-9]+)-maxiter:(-?[0-9]+)-csize:([0-9]+)-ctype:([0-9]+)\.json$', f)
        if match:
            fd = { 'name': f,
                   'trials': int(match.group(1)),
                   'lexcount': int(match.group(2)),
                   'maxiter': int(match.group(3)),
                   'csize': int(match.group(4)),
                   'ctype': int(match.group(5)),
               }
            files.append(fd)
            
    #known_seeds = [ "random", "compactdegree", "compactdistance", "distance", "degree", "compactgreedy", "greedy" ]
    known_seeds = [ "compactdegree", "compactdistance", "compactgreedy" ]
    known_seeds = [ "compactgreedy" ]
    known_seeds = [ "compactdegree" ]
    known_seeds = [ "compactdistance" ]
    max_k = 30
    net_file = "../networks/facebook/facebook_combined.txt"
    spread_probability = 0.05
    
    for fd in files:
        for seed in known_seeds:
            for community_choice in (1, 2, 3):
                if community_choice > 1 and seed not in ["compactdegree", "compactdistance", "compactgreedy" ]:
                    break

                # takes too long to calculate
                if seed == "compactdistance":
                    if fd['maxiter'] > 4096:
                        print "skipping:", seed, "maxiter:", fd['maxiter']
                        continue
                    if fd['csize'] > 512:
                        print "skipping:", seed, "csize:", fd['csize']
                        continue
                if seed == "compactgreedy":
                    if fd['maxiter'] > 2048:
                        print "skipping:", seed, "maxiter:", fd['maxiter']
                        continue
                    if fd['csize'] > 1024:
                        print "skipping:", seed, "csize:", fd['csize']
                        continue
                    
                output_file = "fbc-results-seed:%s-max-k:%d-trials:%d-rate:%f-lexcount:%d-maxiter:%d-csize:%d-ctype:%d-cchoice:%d.json" % \
                              (seed, max_k, fd['trials'], spread_probability, fd['lexcount'], fd['maxiter'], fd['csize'], fd['ctype'], community_choice)
                if os.path.exists(output_file):
                    print "already completed", output_file
                    continue
                    
                cmd = "./measure_seed_selector.py --seed %s --max-k %d --input %s --output %s --n-trials %d --spread-probability %f --lex-count %d --max-iterations %d --max-community-size %d --community-type %d --community-file %s --community-choice %d" % \
              (seed, max_k, net_file, output_file, fd['trials'], spread_probability, fd['lexcount'], fd['maxiter'], fd['csize'], fd['ctype'], fd['name'], community_choice)
                #print fd
                print cmd
                os.system(cmd)
                #print
    
    return
    
if __name__ == "__main__":
    main()
