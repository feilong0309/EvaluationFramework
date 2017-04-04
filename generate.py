## Author: Scott Emmons (scott@scottemmons.com)
## Purpose: A script to generate multiple LFR benchmark graphs based on the given parameters
## Date: January 2, 2014

import argparse
import os
import shutil
import errno
import subprocess
import networkx as nx
import random
import time
import math
from sampling.sampling_algorithms import *
import analytics
#from sampling.sampling_algorithms import induced_weighted_random_vertex_sampler
#import sampling.sampling_algorithms

####################
# Global Variables #
####################

flag_file_name = "myflags.dat"

##################
# Main Functions #
##################

def handleArgs():
    """Handle command-line input arguments."""

    parser = argparse.ArgumentParser(description="Generate LFR benchmark graphs.")
    parser.add_argument("-n", "--nodes", type=int, required=True, help="the number of nodes", dest="N")
    parser.add_argument("-k", "--avgdegree", default=25, type=int, help="the average degree of the nodes, defaults to 25", dest="k")
    parser.add_argument("--maxk", "--maxdegree", type=int, required=True, help="the maximum degree of the nodes", dest="maxk")
    parser.add_argument("--mu", type=float, required=True, help="the mixing parameter", dest="mu")
    parser.add_argument("--minc", default=50, type=int, help="the minimum community size, defaults to 50", dest="minc")
    parser.add_argument("--maxc", type=int, required=True, help="the maximum community size", dest="maxc")
    parser.add_argument("-s", "--start", default=1, type=int, help="the file number at which to start, inclusive", dest="start")
    parser.add_argument("-e", "--end", default=10, type=int, help="the file number at which to end, inclusive", dest="end")
    parser.add_argument("-b", "--benchmark", default="binary_networks/", help="the path to the installed LFR generation software", dest="bench_directory_stem")
    parser.add_argument("-o", "--output", default="generated_benches/", help="the output path, defaults to 'generated_benches/'", dest="out_directory_stem")

    global args
    args = parser.parse_args()

def createPathIfNeeded(path):
    """Credits to user 'Heikki Toivonen' on SO: http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary"""
    try:
        os.makedirs(path)
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise

def deletePathIfNeeded(path):
    try:
        shutil.rmtree(path)
    except OSError as error:
        if error.errno != errno.ENOENT:
            raise

def getMinEdgelistId(edgelist_file, separator):
    """"""

    with open(edgelist_file, 'r') as f:
        source_id, destination_id = f.readline().split(separator)
        destination_id = destination_id[:-1] #remove newline character
        min_id = min(int(source_id), int(destination_id))
        for line in f:
            source_id, destination_id = line[:-1].split(separator) #line[:-1] removes newline character from destination_id 
            min_id = min(int(source_id), int(destination_id), min_id)

    return min_id

def rewriteEdgelistFromZero(graph_file, separator):
    """"""

    temporary_file = 'temporary_program_file_s_' + str(args.start) + '_e_' + str(args.end) + '.dat'
    assert not os.path.isfile(temporary_file)

    min_id = getMinEdgelistId(graph_file, separator)
    source = open(graph_file, 'r')
    destination = open(temporary_file, 'wb')

    for line in source:
        source_id, destination_id = line[:-1].split(separator) #line[:-1] removes newline character from destination_id
        source_id = str(int(source_id) - min_id)
        destination_id = str(int(destination_id) - min_id)
        destination.write(source_id + separator + destination_id + '\n')

    source.close()
    destination.close()

    shutil.move(temporary_file, graph_file)

def getMinClusteringId(clustering_file, separator):
    """"""
    
    with open(clustering_file, 'r') as f:
        min_id = int(f.readline().split(separator)[0])
        for line in f:
            node_id = int(line.split(separator)[0])
            min_id = min(node_id, min_id)

    return min_id

def rewriteClusteringFromZero(clustering_file, separator):
    """"""

    temporary_file = 'temporary_program_file_s_' + str(args.start) + '_e_' + str(args.end) + '.dat'
    assert not os.path.isfile(temporary_file)

    min_id = getMinClusteringId(clustering_file, separator)
    source = open(clustering_file, 'r')
    destination = open(temporary_file, 'wb')

    for line in source:
        node_id, cluster_id = line[:-1].split(separator) #line[:-1] removes newline character from cluster_id
        node_id = str(int(node_id) - min_id)
        destination.write(node_id + separator + cluster_id + '\n')

    source.close()
    destination.close()

    shutil.move(temporary_file, clustering_file)

def sampleCommunities(sample, clustering_file, write_file, separator):
    """Given a network file separated by separator, removes edges such that the final network file_name
    contains no two edges that connect the same pair of nodes.
    Assumes node ids and cluster ids are integers.
    If assume_one_max, the function will assume that there are at most two
    edges in the original file connecting the same pair of nodes."""
    sample_nodes=set(sample.nodes())
    read_file = clustering_file
    #write_file ="sample_"+read_file
    assert not os.path.isfile(write_file)

    with open(read_file, 'r') as read_f:
        with open(write_file, 'wb') as write_f:
            for line in read_f:
                node_id, cluster_id = line[:-1].split(separator)
                node_id = int(node_id)
                if  node_id in sample_nodes:
                    write_f.write(str(node_id) + separator + str(cluster_id) + '\n')                 
    
    #shutil.move(write_file, read_file)  

def generateFlagFile(file_name, out_directory_stem, N, k, maxk, mu, minc, maxc):
    """file_name: String
    out_directory_stem: String
    N: int
    mu: float"""

    to_write = ""

    to_write += "-N " + str(N) + "\n"
    to_write += "-k " + str(k) + "\n"
    to_write += "-maxk " + str(maxk) + "\n"
    to_write += "-mu " + str(mu) + "\n"
    to_write += "-t1 2\n"
    to_write += "-t2 1\n"
    to_write += "-minc " + str(minc) + "\n"
    to_write += "-maxc " + str(maxc) + "\n"
    to_write += "-on 0\n"
    to_write += "-om 0\n"

    f = open(out_directory_stem + file_name, 'w')
    f.write(to_write)

def removeDuplicateEdges(filename, separator, assume_one_max = False):
    """Given a network file separated by separator, removes edges such that the final network file_name
    contains no two edges that connect the same pair of nodes.
    Assumes node ids and cluster ids are integers.
    If assume_one_max, the function will assume that there are at most two
    edges in the original file connecting the same pair of nodes."""

    read_file = filename
    write_file = "temporary_function_execution_s_" + str(args.start) + "_e_" + str(args.end) + ".dat"
    assert not os.path.isfile(write_file)

    with open(read_file, 'r') as read_f:
        with open(write_file, 'wb') as write_f:
            redundant_edges = {}
            empty_set = set() 
            for line in read_f:
                source, destination = line.split(separator)
                source = int(source)
                destination = int(destination.rstrip()) # remove newline character and trailing spaces
                if not destination in redundant_edges.get(source, empty_set):
                    write_f.write(str(source) + separator + str(destination) + '\n')
                    redundant_edges[destination] = redundant_edges.get(destination, empty_set)
                    redundant_edges[destination].add(source)
                    empty_set = set() # reverse mutation due to previous line
                elif assume_one_max:
                    redundant_edges[source].remove(destination)
    
    #shutil.move(read_file, read_file + 'a')
    shutil.move(write_file, read_file)
    

if __name__ == "__main__":

    handleArgs()

    generateFlagFile(flag_file_name, args.bench_directory_stem, args.N, args.k, args.maxk, args.mu, args.minc, args.maxc)
    deletePathIfNeeded(args.out_directory_stem)    
    createPathIfNeeded(args.out_directory_stem)
    
    for i in xrange(args.start, args.end + 1):
        # Does seed file need to be handled here?
        subprocess.call(['./benchmark', '-f', flag_file_name], cwd = args.bench_directory_stem)
        shutil.move(args.bench_directory_stem + 'network.dat', args.out_directory_stem + 'network_v' + str(i) + '.dat')
        shutil.move(args.bench_directory_stem + 'community.dat', args.out_directory_stem + 'community_v' + str(i) + '.dat')
        shutil.move(args.bench_directory_stem + 'statistics.dat', args.out_directory_stem + 'statistics_v' + str(i) + '.dat')
        # Remove duplicate edges from edgelist file and rewrite edgelist file such that node ids start from zero for compatibility with clustering program input formats
        removeDuplicateEdges(args.out_directory_stem + 'network_v' + str(i) + '.dat', '\t', assume_one_max = True)
        rewriteEdgelistFromZero(args.out_directory_stem + 'network_v' + str(i) + '.dat', '\t')
        # Rewrite clustering file such that node ids start from zero to maintain consistency with edgelist file node ids
        rewriteClusteringFromZero(args.out_directory_stem + 'community_v' + str(i) + '.dat', '\t')
        
        
        ###zjp add sampling stragegy
        re=open(args.out_directory_stem + 'network_v' + str(i) + '.dat', 'rb')
        G=nx.read_edgelist(re, nodetype=int)
        re.close() 
        
        #G = nx.read_edgelist(path=readfile, delimiter=",", nodetype=int,  create_using=nx.Graph())
        start = 0
        G_ = nx.convert_node_labels_to_integers(G, first_label=start)
        numNodes = len(nx.nodes(G_))
        
        percentages = [0.1, 0.3, 0.5, 0.7]
        sampling_conditions = ['induced_random_edge','induced_random_vertex','induced_weighted_random_vertex','kk_path','km_path','random_path','random_vertex','random_edge','random_walk','metropolis_subgraph','metropolized_random_walk','weighted_vertex']
        
        #sampling strategy
        sampling_condition = str(sampling_conditions[10])
        if not sampling_condition in sampling_conditions:
            raise ValueError('Invalid stopping criteria, please choose one from ['+'"UNIQUE_NODES", "UNIQUE_EDGES", "NODES", "EDGES"'+']')
        for val in percentages:       
            sample_size = int(math.ceil(float(numNodes)*val))        
            t=time.time()
            if sampling_condition=='induced_random_vertex':
                sample = induced_random_vertex_sampler(G, sample_size, with_replacement=False)
            elif sampling_condition=='induced_random_edge':
                sample = induced_random_edge_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', with_replacement=True)
            elif sampling_condition=='induced_weighted_random_vertex':#invalid
                sample = sampling.sampling_algorithms.induced_weighted_random_vertex_sampler(G, sample_size, weights=None, with_replacement=True)
            elif sampling_condition=='kk_path':#invalid                
                sample = kk_path_sampler(G, sample_size, K=None, vantage_points=None, stopping_condition='UNIQUE_NODES', fuzzy_select=True, include_last_path_when_exceeds=True)
            elif sampling_condition=='km_path':#invalid
                sample = km_path_sampler(G, sample_size, K=None, M=None, source_nodes=None, destination_nodes=None, source_destination_nodes_can_overlap=False, stopping_condition='UNIQUE_NODES', fuzzy_select=True, include_last_path_when_exceeds=True)
            elif sampling_condition=='random_path':
                sample = random_path_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', include_last_path_when_exceeds=True)
            elif sampling_condition=='random_vertex': #just nodes 
                sample = random_vertex_sampler(G, sample_size, with_replacement=False)
            elif sampling_condition=='random_edge':
                sample = random_edge_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', with_replacement=True, include_last_edge_when_exceeds=True)
            elif sampling_condition=='random_walk':
                sample = random_walk_sampler(G, sample_size, initial_node=None, stopping_condition='UNIQUE_NODES', metropolized=False, excluded_initial_steps=0)
            elif sampling_condition=='metropolis_subgraph':
                p=10*G.number_of_edges()*log10(G.number_of_nodes())/G.number_of_nodes() 
                best, div=metropolis_subgraph_sampler(G, 100, analytics.DivergenceMetrics.JensenShannonDivergence, smp.SimpleGraphDegree(), 1000, p, 10, 2)
                sample = best
            elif sampling_condition=='metropolized_random_walk':
                sample = metropolized_random_walk_sampler(G, sample_size, stopping_condition='UNIQUE_NODES', excluded_initial_steps=0)
            elif sampling_condition=='weighted_vertex':
                sample = weighted_vertex_sampler(G, sample_size, weights, with_replacement=True)
                
            print time.time()-t  
            print 'number of unique nodes:',sample.number_of_nodes()
            print 'number of unique edges:',sample.number_of_edges()
            print 'number of nodes:',sample.graph.get('number_of_nodes_repeated',0)
            print 'number of edges:',sample.graph.get('number_of_edges_repeated',0)
            print 'nodes',sample.nodes()
        
        #def sampleCommunities(sample,clustering_file, separator):
            sampleCommunities(sample,args.out_directory_stem + 'community_v' + str(i) + '.dat', args.out_directory_stem + 'community_sample_p'+str(int(100*val))+'_v' + str(i) + '.dat','\t')
            we=open(args.out_directory_stem + 'network_sample_p'+str(int(100*val))+'_v' + str(i) + '.dat','wb')
            nx.write_edgelist(sample, we ,data=False)
            we.close()
        

 
    shutil.move(args.bench_directory_stem + flag_file_name, args.out_directory_stem + "flags.dat")
