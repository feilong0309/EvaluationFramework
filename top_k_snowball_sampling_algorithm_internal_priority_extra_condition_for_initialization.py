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
        node_degree = i[1]
      
        if (len(leader_list) == 0): #no nodes has been sampled as leaders, so we start from the one with the highest degree in network
            leader_list.append(i)
            leaders_having_been_sampled = leaders_having_been_sampled + 1

        else:
            flag_satisfying_leader_conditions = 1; #1:it is a leader 0:it is not a leader

            for leader, degree in leader_list:
               
                neighbor_list = G.neighbors(node)
               
                #not direct condition
                if ('--not_direct_neighbors' in option_conditions): #with this condition, leaders should not be connected directly
                    if (leader in neighbor_list):
                        #print "leaders should not been connected directly!"
                        flag_satisfying_leader_conditions = 0
                        break;
            
                #few neighbors condition
                G_common_neighbors = nx.common_neighbors(G, leader, node)
                common_neighbor_list = ([x for x in G_common_neighbors])                
                if (len(common_neighbor_list) >= threshold_common_neighbors):
                    flag_satisfying_leader_conditions = 0
                    break;
                    
            #our new condition, the degree of leader should not be smaller than at most k-1 nodes in its neighbors
            competitive_nodes = 0
            for neighbor in neighbor_list:
                neighbor_degree = len(G.neighbors(neighbor))
                if(neighbor_degree >= node_degree):
                    competitive_nodes = competitive_nodes + 1
                if(competitive_nodes >= total_communities):
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

def init_sampling_nodes(leader_list): #initialze sampling nodes for corresponding leaders
    sampling_nodes = [];
    for leader in leader_list:
        node = leader[0]
        sampling_nodes.append(node)
    return sampling_nodes

def init_sampling_communities(leader_list, number_of_communities): #initialize communities for corresponding leaders    
    sampling_communities = [];
    i = 0;
    while (i < number_of_communities):
        sampling_communities.append([leader_list[i][0]])
        i = i + 1
    return sampling_communities

def init_neighbors_of_sampling_communities(G, leader_list, number_of_communities): #initialize neighbors for corresponding communites
    neighbors_of_sampling_communities = [];
    i = 0;
    while (i < number_of_communities):
        neighbors_of_sampling_communities.append(G.neighbors(leader_list[i][0]))
        i = i + 1
    return neighbors_of_sampling_communities

def sample_a_node(sampling_nodes, number_of_sampled_nodes, node):
    if (node not in sampling_nodes):
        sampling_nodes.append(node)
        number_of_sampled_nodes = number_of_sampled_nodes + 1
    return number_of_sampled_nodes

def sampling_process_with_internal_principle(G, leader_list, sample_size):
    print "We decide to sample %d nodes:" %sample_size
    number_of_communities = len(leader_list)
    
    #intialize communities for corresponding leader, each communities has only one node (the leader) in the 
    sampling_nodes = init_sampling_nodes(leader_list)
    sampling_communities_list = init_sampling_communities(leader_list, number_of_communities) 
    neighbors_of_sampling_communities_list = init_neighbors_of_sampling_communities(G, leader_list, number_of_communities)
     
    # print "sampling_nodes:"
    # print sampling_nodes
    # print "sampling_communities_list:"
    # print sampling_communities_list
    # print "neighbors_of_sampling_communities_list:"
    # print neighbors_of_sampling_communities_list
    # print '\n'

    #let sampling begin
    number_of_sampled_nodes = number_of_communities
    while ((number_of_sampled_nodes < sample_size)):
        i = 0;
        while (i < number_of_communities):
            sampling_community_set = sampling_communities_list[i] #Ci
            neighbors_of_sampling_community_set =  neighbors_of_sampling_communities_list[i] #N(Ci)
            extra_neighbors_list = [] 
            number_of_extra_neighbors_list = []
            
            #print "neighbors_of_sampling_community_set:"
            #print neighbors_of_sampling_community_set

            selected_node = 0 
            extra_neighbors_value_of_selected_node = 100000000
            extra_neighbors_of_selected_node = []
            flag_no_extra_neighbors = 0 #1: there are some nodes in N(Ci) providing no extra neighbors        

            if (len(neighbors_of_sampling_community_set) != 0):
                #for v in neighbors_of_sampling_community_set:
                j = 0; 
                while (j < len(neighbors_of_sampling_community_set)):
                    v = neighbors_of_sampling_community_set[j]
                    extra_neighbors_of_v = calc_extra_neighbors_of_v(G, v, neighbors_of_sampling_community_set, sampling_community_set)
                    extra_neighbors_list.append(extra_neighbors_of_v)
                    number_of_extra_neighbors_list.append(len(extra_neighbors_of_v))
                    if (len(extra_neighbors_of_v) == 0): #|N(v) - (N(S) U S)| cannot be smaller than 0. So it is an internal node and must be sampled
                        # print"sample node %d into community %d, reason: |N(v) - N(Ci) U Ci| = 0" %(v, i)
    
                        #update related information
                        flag_no_extra_neighbors = 1
                        sampling_community_set.append(v)
                        neighbors_of_sampling_community_set.remove(v)
                        
                        #sample this node
                        number_of_sampled_nodes = sample_a_node(sampling_nodes, number_of_sampled_nodes, v)   
                        continue;  # neighbors_of_sampling_community_set has been shorted, so prevent j from increasing
                    
                    elif ((extra_neighbors_value_of_selected_node  > len(extra_neighbors_of_v))): #|N(v) - (N(S) U S)|
                        selected_node = v
                        extra_neighbors_value_of_selected_node  = len(extra_neighbors_of_v)
                        extra_neighbors_of_selected_node = extra_neighbors_of_v                     
                    j = j + 1
   
                if (flag_no_extra_neighbors == 0): #add the node with the min |N(v) - N(Ci) U Ci| into Ci    
                    # print "sample node %d into community %d, reason: min |N(v) - N(Ci) U Ci|=%d" %(selected_node, i, len(extra_neighbors_of_selected_node))
                    # print "neighbors before:"
                    # print neighbors_of_sampling_community_set
                    if (len(neighbors_of_sampling_community_set) != 0):                    
                    #update related information
                        update_set(sampling_community_set, neighbors_of_sampling_community_set, selected_node, extra_neighbors_of_selected_node)
    
                    # print "neighbors after:"
                    # print neighbors_of_sampling_community_set
    
                    #sample this node
                    number_of_sampled_nodes = sample_a_node(sampling_nodes, number_of_sampled_nodes, selected_node)

            #print "number_of_extra_neighbors_list:"
            #print number_of_extra_neighbors_list
            #print "sampling_communities_list:"
            #print sampling_communities_list
            #print "neighbors_of_sampling_communities_list:"
            #print neighbors_of_sampling_communities_list
            #print "now %d nodes have been sampled:" %number_of_sampled_nodes
            #print "\n"
            #time.sleep(1)
            i = i + 1
        
        #print "number_of_extra_neighbors_list:"
        #print number_of_extra_neighbors_list
        #print "sampling_communities_list:"
        #print sampling_communities_list
        #print "neighbors_of_sampling_communities_list:"
        #print neighbors_of_sampling_communities_list
        #print "now %d nodes have been sampled:" %number_of_sampled_nodes
        #print "\n"
        #time.sleep(1)
        
    #zjp add if the number_of_sampled_nodes is larger than sample_size
    while (number_of_sampled_nodes > sample_size):
        min_degree = sys.maxint
        for sampled_node in sampling_nodes:
            # neighbours = G.neighbors(sampled_node)
            node_degree = G.degree(sampled_node)
            if (node_degree  < min_degree): 
                min_degree = node_degree
                temp_node = sampled_node
            else:
                continue
        sampling_nodes.remove(temp_node)
        number_of_sampled_nodes= number_of_sampled_nodes-1

    return sampling_nodes

def build_sample_graph(node_list, edge_list):
    S = nx.Graph()
    S.add_nodes_from(node_list)
    S.add_edges_from(edge_list)
    return S

def top_k_snowball_sampling_algorithm_internal_priority_extra(G, sample_ratio, number_of_communities, option):
    
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
    sampling_nodes = sampling_process_with_internal_principle(G, leader_list, sample_size)

    # print "sampling nodes:"
    # print sampling_nodes
    # print "\n"
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

    #step4: draw a graph
    S = build_sample_graph(sampling_nodes, sampling_edges)
    #print S.nodes()
    #print "%d nodes" %S.number_of_nodes()
    #print S.edges()
    #print "%d edges" %S.number_of_edges()
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

