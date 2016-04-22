#!/bin/bash

netfile=../networks/facebook/facebook_combined.txt
prefix=fbc
ntrials=10
lexcount=20
maxiter=-1
max_csize=1
community_type=1
#community_type=2
#community_type=3
#max_csizes="2 4 8 16 32 64 128 256 512 1024 2048 4096"
maxiters="2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072"

#for max_csize in $max_csizes; do
for maxiter in $maxiters; do
    output="${prefix}-trials:${ntrials}-lexcount:${lexcount}-maxiter:${maxiter}-csize:${max_csize}-ctype:${community_type}.json"
    echo
    echo $output
    echo
    ./pre_calc_communities.py \
        --input ${netfile} \
        --output $output \
        --n-trials $ntrials \
        --lex-count $lexcount \
        --max-iterations $maxiter \
        --max-community-size $max_csize \
        --community-type $community_type
done
