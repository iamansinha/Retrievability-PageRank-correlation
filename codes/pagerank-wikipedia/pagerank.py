#!/usr/bin/env python3

import sys
import time
import argparse

def makeDictWithOutlinksCounts(leftSorted_linkFile, start_value):
    nodes_dict = {}
    prev_from_node = None
    outlinks_count = 1
    with open(leftSorted_linkFile, encoding="utf-8") as f:
        for line in f:
            from_node, to_node = (int(qid.strip()) for qid in line.split('\t')[:2])
            
            if prev_from_node == None:
                prev_from_node = from_node
                continue
            elif from_node == prev_from_node:
                outlinks_count += 1
            else:
                # qid change in 1st col of left-sorted file means node change
                # adding node and its outlink count with some other values that
                # will be helpful later while computing pagerank
                nodes_dict[prev_from_node] = [outlinks_count, start_value, start_value, False]
                outlinks_count = 1
            prev_from_node = from_node
        
        # last line node adding in nodes_dict
        if prev_from_node != None:
            nodes_dict[prev_from_node] = [outlinks_count, start_value, start_value, False]
    return nodes_dict


def pagerank(nodes_dict, rightSorted_linkFile, d, start_value, precision, max_iterations = 50):
    tol = 10**(-1*precision)
    for i in range(1,max_iterations+1):
        print(f'{i}.', end='', flush=True, file=sys.stderr)
        
        prev_to_node = None
        # alternating prev and curr index values with iterations 
        # since after one iteration curr becomes prev and at the
        # place of prev, curr pagerank values will be replaced.
        prev_pagerank_index = (i-1)%2 + 1
        curr_pagerank_index = i%2 + 1
        
        flag = True
        with open(rightSorted_linkFile, encoding='utf-8') as f:
            for line in f:
                in_link, curr_to_node = (int(qid.strip()) for qid in line.split('\t')[:2])
                if prev_to_node != curr_to_node:
                    if prev_to_node != None:
                        pagerank = (1-d) + d*pagerank
                        nodes_dict[prev_to_node][curr_pagerank_index] = pagerank
                        # check convergence precision for curr_to_node pagerank value
                        if abs(nodes_dict[prev_to_node][curr_pagerank_index]-nodes_dict[prev_to_node][prev_pagerank_index]) >= tol:
                            flag = False
                        # mark current node as 'touched' (it has incoming links)
                        if i == 1:
                            nodes_dict[prev_to_node][3] = True
                    # reset sum container var
                    pagerank = 0
                    # if a node didn't had any outlinks, it wouldn't be in nodes_dict 
                    # so need to initialize such nodes in nodes_dict
                    if curr_to_node not in nodes_dict:
                        nodes_dict[curr_to_node] = [0, start_value, start_value, False]
                
                prev_pagerank = nodes_dict[in_link][prev_pagerank_index]
                numOutlinks = nodes_dict[in_link][0]
                
                pagerank += prev_pagerank/numOutlinks
                
                prev_to_node = curr_to_node
            
            # handling last line node
            if prev_to_node != None:
                pagerank = (1-d) + d*pagerank
                nodes_dict[prev_to_node][curr_pagerank_index] = pagerank
                # check convergence precision for curr_to_node pagerank value
                if abs(nodes_dict[prev_to_node][curr_pagerank_index]-nodes_dict[prev_to_node][prev_pagerank_index]) > tol:
                    flag = False
                # mark current node as 'touched' (it has incoming links)
                if i == 1:
                    nodes_dict[prev_to_node][3] = True
                
        # set pagerank score (1-d) to 'untouched' nodes (they do not have incoming links)
        if i == 1:
            for node in nodes_dict:
                if not nodes_dict[node][3]:
                    nodes_dict[node][prev_pagerank_index] = (1-d)
                    nodes_dict[node][curr_pagerank_index] = (1-d)
        # if all nodes' pagerank within tol, then break out of loop. Computation complete!
        if flag==True:
            break
    print('', file=sys.stderr)
    return nodes_dict, i
        

def main():
    parser = argparse.ArgumentParser(prog='python3 pagerank.py', description='wiki-pagerank' +
                                     ' - Compute PageRank on large graphs with ' +
                                     'off-the-shelf hardware.')
    parser.add_argument('left_sorted', type=str, help='A two-column, ' +
                        'tab-separated file sorted by the left column.')
    parser.add_argument('right_sorted', type=str, help='The same ' +
                        'file as left_sorted but sorted by the right column.')
    parser.add_argument('damping', type=float, help='PageRank damping factor' +
                        '(between 0 and 1).', default=0.85)
    parser.add_argument('start_value', type=float, help='PageRank starting value '+
                        '(>0).', default=1)
    parser.add_argument('precision', type=int, help='Number of places after '+
                        'the decimal point.', default=4)
    parser.add_argument('-m', '--max_iterations', type=int, help='Number of PageRank ' +
                        'iterations (>=0).', default=100)
    # parser.add_argument('-i', '--int_only', action='store_true', help='All nodes are integers '+
    #                     '(flag)')
    args = parser.parse_args()
    if args.max_iterations < 0 or args.damping > 1 or args.damping < 0 or args.start_value <= 0 or args.precision < 0:
        print(f"ERROR: Provided PageRank parameters\n[max_iterations ({args.max_iterations}), damping ({args.damping}),",
            f"start value ({args.start_value}), precision ({args.precision})]\n out of allowed range.\n\n")
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    leftSorted_linkFile = args.left_sorted
    rightSorted_linkFile = args.right_sorted
    d = args.damping
    start_value = args.start_value
    precision = args.precision
    max_iterations = args.max_iterations
    
    start = time.time()
    
    nodes_dict = makeDictWithOutlinksCounts(leftSorted_linkFile, start_value)
    
    if rightSorted_linkFile:
        nodes_dict, iterations = pagerank(nodes_dict, rightSorted_linkFile, d, start_value, precision, max_iterations)
    else:
        raise FileNotFoundError('Right-sorted link file missing from the arguments!')
    
    print(f'PageRank computation took {time.time()-start:.2f} seconds and {iterations} iterations', file=sys.stderr)
    
    final_pagerank_index = iterations%2 + 1
    for node in nodes_dict:
        print(f'{node}\t{nodes_dict[node][final_pagerank_index]:.{precision}f}')


if __name__=='__main__':
    main()