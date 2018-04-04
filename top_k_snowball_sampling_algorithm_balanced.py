from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
import time
import copy 
import os
import sys
###############################################################################################################
#parameters:
#    total_communities: 
#        number of leaders we will be based on
#    threshold_common_neighbors: 
#        every pair of leaders should share total common neighbors less than this threshold
#    option_conditions: 
#        other conditions used to in the initialization of leaders, including
#       
#return:
#    leader_list
###############################################################################################################
def init_leaders_without_k_higher(G, node_list, edge_list, total_communities = 3, threshold_common_neighbors = 5, option_conditions = []):

    leader_list = [];

    degree_dic = {}
    for i in node_list:
        neighbor_list = G.neighbors(i)
        degree_dic[i] = len(neighbor_list)
    
    degree_list =  sorted(degree_dic.iteritems(), key=lambda item:item[1], reverse = True ) 
    #format of element in degree list: tuple (x,y), where x denotes the name of node, y denotes the degree of node   

    leaders_having_been_sampled = 0

    for i in degree_list:

        node = i[0] #get the name of node
        degree = i[1]
      
        if (len(leader_list) == 0): #no nodes has been sampled as leaders, so we start from the one with the highest degree in network

            leader_list.append(i)
            leaders_having_been_sampled = leaders_having_been_sampled + 1

        else:

            flag_satisfying_leader_conditions = 1; #1:it is a leader 0:it is not a leader

	    for leader, degree in leader_list:
               
                if ('--not_direct_neighbors' in option_conditions): #with this condition, leaders should not be connected directly
                    neighbor_list = G.neighbors(node)
                    if (leader in neighbor_list):
                       #print "leaders should not been connected directly!"
		       flag_satisfying_leader_conditions = 0
                       break;

                G_common_neighbors = nx.common_neighbors(G, leader, node)
                common_neighbor_list = ([x for x in G_common_neighbors])                
                if (len(common_neighbor_list) >= threshold_common_neighbors):
		    flag_satisfying_leader_conditions = 0
                    break;

            if (flag_satisfying_leader_conditions == 1):
                leader_list.append(i)
                leaders_having_been_sampled = leaders_having_been_sampled + 1
        
        if (leaders_having_been_sampled == total_communities):
            break;

   
    return leader_list
    
def init_leaders(G, node_list, edge_list, total_communities = 3, threshold_common_neighbors = 5, option_conditions = []):

    leader_list = [];

    degree_dic = {}
    for i in node_list:
        neighbor_list = G.neighbors(i)
        degree_dic[i] = len(neighbor_list)
    
    degree_list =  sorted(degree_dic.iteritems(), key=lambda item:item[1], reverse = True ) 
    #format of element in degree list: tuple (x,y), where x denotes the name of node, y denotes the degree of node   

    leaders_having_been_sampled = 0

    for i in degree_list:

        node = i[0] #get the name of node
        degree = i[1]
      
        if (len(leader_list) == 0): #no nodes has been sampled as leaders, so we start from the one with the highest degree in network

            leader_list.append(i)
            leaders_having_been_sampled = leaders_having_been_sampled + 1

        else:

            flag_satisfying_leader_conditions = 1; #1:it is a leader 0:it is not a leader

	    for leader, degree in leader_list:
               
                if ('--not_direct_neighbors' in option_conditions): #with this condition, leaders should not be connected directly
                    neighbor_list = G.neighbors(node)
                    if (j in neighbor_list):
                       #print "leaders should not been connected directly!"
		       flag_satisfying_leader_conditions = 0
                       break;

                G_common_neighbors = nx.common_neighbors(G, leader, node)
                common_neighbor_list = ([x for x in G_common_neighbors])                
                if (len(common_neighbor_list) >= threshold_common_neighbors):
		    flag_satisfying_leader_conditions = 0
                    break;

            if (flag_satisfying_leader_conditions == 1):
                leader_list.append(i)
                leaders_having_been_sampled = leaders_having_been_sampled + 1
        
        if (leaders_having_been_sampled == total_communities):
            break;

   
    return leader_list


#########################################################################
#paraments:
#    neighbors_of_sampling_set: N(S), |N(S)| = len(neighbors_of_sampling_set)
#    sampling_set:S, |S| = len(sampling_set)
#return:
#    |N(S)|/|S|
##########################################################################
def calc_expansion_factor(neighbors_of_sampling_set, sampling_set):
    return len(neighbors_of_sampling_set) / len(sampling_set)

##########################################################################
#return:
#    N(v) - (N(S) U S)
##########################################################################
def calc_extra_neighbors_of_v(G, v, neighbors_of_sampling_set, sampling_set):
      
    neighbors_of_v = G.neighbors(v) #N(v)
    extra_neighbors_of_v = copy.deepcopy(neighbors_of_v)

    for i in neighbors_of_v:  
        #if v belongs to (N(S) U S), remove it from N(v)
        if ((i in neighbors_of_sampling_set) or (i in sampling_set)): 
            extra_neighbors_of_v.remove(i)
      
      
    return (extra_neighbors_of_v)

def update_set(sampling_set, neighbors_of_sampling_set, selected_node, extra_neighbors_of_selected_node):
    sampling_set.append(selected_node)
    neighbors_of_sampling_set.remove(selected_node)
    for i in extra_neighbors_of_selected_node:
        neighbors_of_sampling_set.append(i)

def sampling_a_best_node(G, neighbors_of_sampling_set, sampling_set):

    #print "Before:"
    #print "Sampling set:"
    #print sampling_set
    #print "Neighbors_of_sampling_set:"
    #print neighbors_of_sampling_set  

    selected_node = 0 
    extra_neighbors_value_of_selected_node = 100000000
    extra_neighbors_of_selected_node = []

    for v in neighbors_of_sampling_set:
        extra_neighbors_of_v = [];
        extra_neighbors_of_v = calc_extra_neighbors_of_v(G, v, neighbors_of_sampling_set, sampling_set)
       
        #print "node %d 's |N(v) - (N(S) U S)| = %d" %(v, len(extra_neighbors_of_v))
 
        if (extra_neighbors_value_of_selected_node  > len(extra_neighbors_of_v)): #|N(v) - (N(S) U S)|
            #print "biggger than current min value, better than current selected node"
            selected_node = v
            extra_neighbors_value_of_selected_node  = len(extra_neighbors_of_v)
            extra_neighbors_of_selected_node = extra_neighbors_of_v
    
        
    #print "After:"
    #print "Selected node = %d" %selected_node
    #print "extra neighbors of %d:" %selected_node
    #print extra_neighbors_of_selected_node

    update_set(sampling_set, neighbors_of_sampling_set, selected_node, extra_neighbors_of_selected_node)

    #print "New sampling set:"
    #print sampling_set
    #print "New neighbors of sampling set:"
    #print neighbors_of_sampling_set
    #print "New |N(S)|/|S|:"
    #print calc_expansion_factor(neighbors_of_sampling_set, sampling_set)

def sample_a_node(sampling_nodes, number_of_sampled_nodes, node):
    if (node not in sampling_nodes):
        sampling_nodes.append(node)
        number_of_sampled_nodes = number_of_sampled_nodes + 1
    return number_of_sampled_nodes
def sampling_process_with_balanced_principle(G, leader_list, sample_size):
    
    sampling_nodes = [];

    number_of_communities = len(leader_list)
    number_of_nodes_in_each_community = sample_size / number_of_communities

    number_of_sampled_nodes = 0
    i = 0;

    #let sampling begin
    # number_of_sampled_nodes = number_of_communities  
    while (i < number_of_communities):
    
        print "Now we begin to sample community %d" %i
        #print "This community should contain %d nodes" %(number_of_nodes_in_each_community)

        leader = leader_list[i][0] #select a leader
        sampling_community_set = []
        neighbors_of_sampling_community_set = []
        sampling_community_set.append(leader)
        neighbors_of_sampling_community_set = G.neighbors(leader)
        
        j = 1;        
        #print "Original sampling set:"
        #print sampling_community_set
        #print "Original neighbors of sampling set:"
        #print neighbors_of_sampling_community_set
        #print "Original |N(S)|/|S|:"
        #print calc_expansion_factor(neighbors_of_sampling_community_set, sampling_community_set)

        while (j < number_of_nodes_in_each_community): #sampling nodes for community i
            
            selected_node = 0 
            extra_neighbors_value_of_selected_node = sys.maxint
            extra_neighbors_of_selected_node = []

            if (len(neighbors_of_sampling_community_set) != 0):
                for v in neighbors_of_sampling_community_set:

                    if (v in sampling_nodes): #this nodes have been selected, it should not be taken into consideration
                        print "node %d has been activated before" %v
                        continue;

                    extra_neighbors_of_v = [];
                    extra_neighbors_of_v = calc_extra_neighbors_of_v(G, v, neighbors_of_sampling_community_set, sampling_community_set)

                    if (len(extra_neighbors_of_v) == 0): #|N(v) - (N(S) U S)| cannot be smaller than 0. So it is an internal node and must be sampled
                        selected_node = v
                        extra_neighbors_value_of_selected_node  = len(extra_neighbors_of_v)
                        extra_neighbors_of_selected_node = extra_neighbors_of_v
                        # print "++++++selected_node:%d" %v
                        break;

                    elif (extra_neighbors_value_of_selected_node  > len(extra_neighbors_of_v)): #|N(v) - (N(S) U S)|
                        selected_node = v
                        extra_neighbors_value_of_selected_node  = len(extra_neighbors_of_v)
                        extra_neighbors_of_selected_node = extra_neighbors_of_v
                        # print "--------selected_node:%d" %v

                if (len(neighbors_of_sampling_community_set) != 0 and selected_node !=0):
                    # print "selected v:"
                    # print v
                    # print "Selected node = %d" %selected_node

                    # print "neighbors before:"
                    # print neighbors_of_sampling_community_set
                    # print "extra neighbors:" 
                    # print extra_neighbors_of_selected_node                  
                    update_set(sampling_community_set, neighbors_of_sampling_community_set, selected_node, extra_neighbors_of_selected_node)
                    # print "neighbors after:"
                    # print neighbors_of_sampling_community_set  

                elif (selected_node ==0):   
                    print "all the neighbour are already been sampled, so we do not need to expand this community"           
                    break 
                # print "New sampling set:"
                # print sampling_community_set
                # print "New neighbors of sampling set:"
                # print neighbors_of_sampling_community_set
                
                #print "New |N(S)|/|S|:"
                #print calc_expansion_factor(neighbors_of_sampling_community_set, sampling_community_set)

            j = j + 1           
            #print "\n"        
            #time.sleep(1)
        #print "\n"                           
        
        for node in sampling_community_set:
            sampling_nodes.append(node)

        i = i + 1;


    #zjp add if the number_of_sampled_nodes is less than sample_size
    number_of_sampled_nodes =len(sampling_nodes)
    print "number of sampling set before adding complementray set:"
    print number_of_sampled_nodes
    print "the sample size should be:"
    print sample_size
    if (number_of_sampled_nodes < sample_size):
        unsampled_nodes =  list(set(G.nodes()).difference(set(sampling_nodes)))
        while (number_of_sampled_nodes < sample_size):
            max_degree = 0
            for unsampled_node in unsampled_nodes:
                # neighbours = G.neighbors(sampled_node)
                unsampled_node_degree = G.degree(unsampled_node)
                if (unsampled_node_degree  > max_degree): 
                    max_degree = unsampled_node_degree
                    temp_node = unsampled_node
                else:
                    continue
            unsampled_nodes.remove(temp_node)                    
            sampling_nodes.append(temp_node)
            number_of_sampled_nodes= number_of_sampled_nodes+1

        print "number of sampling set after adding complementray set:"
        print number_of_sampled_nodes

    return sampling_nodes

def build_sample_graph(node_list, edge_list):
    S = nx.Graph()
    S.add_nodes_from(node_list)
    S.add_edges_from(edge_list)
    return S

def top_k_snowball_sampling_algorithm_balanced(G, sample_ratio, number_of_communities, option):
    
    node_list = G.nodes()
    edge_list = G.edges()
    
    #step I: initialize_leaders
    print "Step I: the initialization of leaders"
    
    leader_list = []
    leader_list = init_leaders(G, node_list, edge_list, total_communities = number_of_communities, option_conditions = option) #for football data set

    print "leader_list:"
    print leader_list
    print "Step I completed."
    print "\n"

    #print "leader_list:"
    #print leader_list
    #print "\n"

    #step II: sample nodes for each community
    print "Step II: sampling processsing"
    sample_size =  sample_ratio * len(node_list)
    sampling_nodes = []
    sampling_nodes = sampling_process_with_balanced_principle(G, leader_list, sample_size)

    # print "sampling nodes:"
    # print sampling_nodes
    print "\n"
    print "Step II completed."

    #step III: sample all the edges according to sample nodes
    sampling_edges = []
    for i in edge_list:
        node_sour = i[0]
        node_dest = i[1]
        if ((node_sour in sampling_nodes) and (node_dest in sampling_nodes)):
            sampling_edges.append(i)
    #print sampling_edges
    #print "%d edges" %len(sampling_edges)

    #step III: draw a graph
    S = build_sample_graph(sampling_nodes, sampling_edges)
    print S.nodes()
    print "%d nodes" %S.number_of_nodes()
    print S.edges()
    print "%d edges" %S.number_of_edges()
    return S

if __name__ == '__main__':

    #filename = './karate/karate.gml'
    #filename = './polbooks/polbooks.gml'
#==============================================================================
#     filename = './football/network_v1.dat'
#     ge=open(filename, 'rb')
#     original_=nx.read_edgelist(ge, nodetype=int, create_using=nx.Graph())    
#     #option_conditions_in_initialization = ['--not_direct_neighbors']
#     option_conditions_in_initialization = []
#     top_k_snowball_sampling_algorithm_balanced(original_, 0.5, 12, option_conditions_in_initialization)
#==============================================================================
 
    s = os.sep
    cwd = os.getcwd()
    parent_path = os.path.dirname(cwd)
    rootdir = parent_path + s + "Networks_with_ground_truth_communities" + s;

    list_dirs = os.walk(rootdir)
    for parent, dirnames, filenames in list_dirs:
        #for dirname in dirnames:
        #    print 'parent is %s' %parent
        #    print 'dirname is %s' %dirname
        for filename in filenames:
            split_filename = filename.split('.');
            if filename == 'network_v1.dat':
                print 'start to draw %s, its parent is %s' %(filename, parent)
                full_name = os.path.join(parent, filename);
                original_ = nx.read_edgelist(full_name, nodetype=int)  
                sample_rate= 0.5
                #option_conditions_in_initialization = ['--not_direct_neighbors']
                option_conditions_in_initialization = []
                sample_ = top_k_snowball_sampling_algorithm_balanced(original_, sample_rate, 12, option_conditions_in_initialization)
                    
                fh=open("test.edgelist",'wb')
#                nx.write_edgelist(S,fh,data=False)
                nx.write_edgelist(sample_, parent+os.sep+"network_sample_p"+str(int(100*float(sample_rate)))+"_v1.dat", data=False)   
                
                fh.close()
                
#            elif filename == 'network_v1_subgraph_speed_up.dat':
#                print 'start to draw %s, its parent is %s' %(filename, parent)
#                full_name = os.path.join(parent, filename);
#                G = nx.read_edgelist(full_name, nodetype=int)                
#                S = top_k_snowball_sampling_algorithm(G, 0.15, 5000)
#                fh=open("test.edgelist",'wb')
#                nx.write_edgelist(S,fh,data=False)
#                nx.write_edgelist(S, full_name+"_test.edgelist", data=False)
            else:            
                continue

