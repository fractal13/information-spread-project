#!/usr/bin/env python

import os, re, sys

def make_one_plot_file(all_files, combination):

    keeper_files = []
    for filename in all_files:
        # fbc-results-seed:compactgreedy-max-k:30-trials:10-rate:0.050000-lexcount:20-maxiter:1024-csize:1-ctype:1-cchoice:1.json
        pattern = "^fbc-results-seed:(.*)-max-k:([0-9]+)-trials:([0-9]+)-rate:(0\.[0-9]+)-lexcount:([0-9]+)-maxiter:(-?[0-9]+)-csize:(-?[0-9]+)-ctype:(-?[0-9]+)-cchoice:(-?[0-9]+).json$"
        match = re.match(pattern, filename)
        if match:
            seed = match.group(1)
            max_k = int(match.group(2))
            trials = int(match.group(3))
            rate = float(match.group(4))
            lexcount = int(match.group(5))
            maxiter = int(match.group(6))
            csize = int(match.group(7))
            ctype = int(match.group(8))
            cchoice = int(match.group(9))

            f = { 'seed': seed,
                  'max_k': max_k,
                  'trials': trials,
                  'rate': rate,
                  'lexcount': lexcount,
                  'maxiter': maxiter,
                  'csize': csize,
                  'ctype': ctype,
                  'cchoice': cchoice,
                  'filename': filename }
            
            if seed == combination[0] and ctype == combination[1] and cchoice == combination[2]:
                if ctype == 1:
                    f['parameter'] = f['maxiter']
                elif ctype == 2 or ctype == 3:
                    f['parameter'] = f['csize']
                keeper_files.append(f)

    keeper_files = sorted(keeper_files, key=lambda f: f['parameter'], reverse=True)

    png_file_name = "zz_%s_ctype%d_cchoice%d.png" % combination
    plot_file_name = "plot_%s_ctype%d_cchoice%d.gnuplot" % combination
    file_contents = """#!/usr/bin/env gnuplot
    
set terminal png enhanced size 893,355
set output "%s"
set xlabel "k (number of seeds)"
set ylabel "<active size> (average size of final active set)"
plot \\
""" % (png_file_name)

    for f in keeper_files:
        seed = f['seed']
        ctype = f['ctype']
        cchoice = f['cchoice']
        parameter = f['parameter']
        
        if seed == "compactgreedy":
            stitle = "CC Greedy"
        elif seed == "compactdegree":
            stitle = "CC Deg"
        elif seed == "compactdistance":
            stitle = "CC Dist"
        else:
            stitle = "%s" % (seed)

        if ctype == 1:
            stitle += " Iter:%d" % (parameter)
        elif ctype == 2:
            stitle += " MaxC:%d" % (parameter)
        elif ctype == 3:
            stitle += " EqualC:%d" % (parameter)
        else:
            stitle = stitle
                
        if cchoice == 1:
            stitle += " Rand"
        elif cchoice == 2:
            stitle += " Cycle"
        elif cchoice == 3:
            stitle += " BigC"
        else:
            stitle = stitle
                
        title = "%s" % (stitle)
        s = '"< ./print_result_file.py -i %s" using 1:2 with lines title "%s", \\\n' % \
            (f['filename'], title)
        file_contents += s

    file_contents += """


"""

    fout = open(plot_file_name, "w")
    fout.write(file_contents)
    fout.close()
    os.chmod(plot_file_name, 0755)
    os.system("./%s" % (plot_file_name))
    return
    
    


def main():
    combinations = [ ("compactdegree", 1, 1),
                     ("compactdegree", 1, 2),
                     ("compactdegree", 1, 3),
                     ("compactdegree", 2, 1),
                     ("compactdegree", 2, 2),
                     ("compactdegree", 2, 3),
                     ("compactdegree", 3, 1),
                     ("compactdegree", 3, 2),
                     ("compactdegree", 3, 3),
                     ("compactdistance", 1, 1),
                     ("compactdistance", 1, 2),
                     ("compactdistance", 1, 3),
                     ("compactdistance", 2, 1),
                     ("compactdistance", 2, 2),
                     ("compactdistance", 2, 3),
                     ("compactdistance", 3, 1),
                     ("compactdistance", 3, 2),
                     ("compactdistance", 3, 3),
                     ("compactgreedy", 1, 1),
                     ("compactgreedy", 1, 2),
                     ("compactgreedy", 1, 3),
                     ("compactgreedy", 2, 1),
                     ("compactgreedy", 2, 2),
                     ("compactgreedy", 2, 3),
                     ("compactgreedy", 3, 1),
                     ("compactgreedy", 3, 2),
                     ("compactgreedy", 3, 3) ]
    args = {}
    
    args['directory'] = "."
    
    all_files = os.listdir(args['directory'])
    for c in combinations:
        make_one_plot_file(all_files, c)
    return

if __name__ == "__main__":
    main()
