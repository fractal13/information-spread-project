#!/bin/bash

#netfile=../networks/twitter/twitter_combined.txt
#prefix=tc
netfile=../networks/facebook/facebook_combined.txt
prefix=fbc
k=30
ntrials=10
rate=05

#seed_styles="random" "compactdegree:100" "compactdegree:200" "compactdegree:400" "compactdistance:100" "compactdistance:200" "compactdistance:400" "distance" "degree"

seed_styles="compactdegree:8192 compactdegree:4096 compactdegree:2048 compactdegree:1024 compactdegree:512 compactdegree:256 compactdegree:128 compactdegree:64 compactdegree:32 compactdegree:16"

for seed in $seed_styles; do
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
        --community-type 3 \
        -p 0.${rate}
done
