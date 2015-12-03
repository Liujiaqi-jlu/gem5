#!/usr/bin/python

#
# A Python script to run all multi-core experiments for PARSEC 2.1 benchmarks.
#
# Copyright (C) Min Cai 2015
#

import os


def run(bench, input_set, l2_size, l2_assoc, l2_tags, num_threads):
    dir = 'results/alpha_no_checkpoints/' + bench + '/' + input_set + '/' + l2_size + '/' + str(l2_assoc) + 'way/' + l2_tags + '/' + str(num_threads) + 'c/'

    os.system('rm -fr ' + dir)
    os.system('mkdir -p ' + dir)

    cmd_run = 'build/ALPHA_MESI_Two_Level/gem5.opt -d ' + dir + ' configs/example/fs.py --two-phase --cpu-type=timing --num-cpus=' \
              + str(num_threads) + ' --script=ext/parsec/2.1/run_scripts/' \
              + bench + '_' + str(num_threads) + 'c_' + input_set + '.rcS' \
              + ' --caches --l2cache --num-l2caches=1' \
              + ' --l1d_size=32kB --l1i_size=32kB --l2_size=' + l2_size + ' --l2_assoc=' + str(l2_assoc) + ' --l2_tags=' + l2_tags
    print cmd_run
    os.system(cmd_run)


def run_experiments(bench, input_set):
    run(bench, input_set, '256kB', 8, 'LRU', 4)
    run(bench, input_set, '512kB', 8, 'LRU', 4)
    run(bench, input_set, '1MB', 8, 'LRU', 4)
    run(bench, input_set, '2MB', 8, 'LRU', 4)
    run(bench, input_set, '4MB', 8, 'LRU', 4)
    run(bench, input_set, '8MB', 8, 'LRU', 4)

    run(bench, input_set, '256kB', 8, 'LRU', 1)
    run(bench, input_set, '256kB', 8, 'LRU', 2)
    run(bench, input_set, '256kB', 8, 'LRU', 8)
    run(bench, input_set, '256kB', 8, 'LRU', 16)

    run(bench, input_set, '256kB', 8, 'IbRDP', 4)
    run(bench, input_set, '256kB', 8, 'RRIP', 4)
    run(bench, input_set, '256kB', 8, 'DBRSP', 4)


# input_sets = ['simsmall', 'simmedium', 'simlarge']
# input_sets = ['simsmall']
input_sets = ['simmedium']
# input_sets = ['simlarge']

for input_set in input_sets:
    run_experiments('blackscholes', input_set)
    run_experiments('bodytrack', input_set)
    run_experiments('canneal', input_set)
    run_experiments('dedup', input_set)
    run_experiments('facesim', input_set)
    run_experiments('ferret', input_set)
    run_experiments('fluidanimate', input_set)
    run_experiments('freqmine', input_set)
    run_experiments('streamcluster', input_set)
    run_experiments('swaptions', input_set)
    run_experiments('vips', input_set)
    run_experiments('x264', input_set)
