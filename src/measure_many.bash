#!/bin/bash

#netfile=../networks/twitter/twitter_combined.txt
#prefix=tc
netfile=../networks/facebook/facebook_combined.txt
prefix=fbc
k=30
ntrials=10
rate=05

for seed in "random" "compactdegree:100" "compactdegree:200" "compactdegree:400" "compactdistance:100" "compactdistance:200" "compactdistance:400" "distance" "degree"; do
    echo
    echo $seed
    echo
    seed_name=`echo "$seed" | awk -F: '{print $1;}'`
    max_csize=`echo "$seed" | awk -F: '{if(NF > 1){print $2;}else{print 0;}}'`
    ./measure_seed_selector.py \
        -s ${seed_name} \
        -k $k \
        -i ${netfile} \
        -o ${prefix}-${seed_name}-k${k}-trials${ntrials}-rate${rate}-csize${max_csize}.json \
        -n $ntrials \
        --max-community-size $max_csize \
        -p 0.${rate}
done
