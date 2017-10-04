Evaluation Framework for Graph Sample Clustering

This repository contains a set of command-line utilities useful for benchmaring
graph sample clustering process on synthetic and real networks with ground-truth (or meta-data). This document includes instructions on how to evaluation the entire sampling clustering process on
these datasets.

1. Environment:
============
Python 2.7 and the scientific programming libraries listed below in the Dependencies section. By the way, our implemention is developed based on the clustering algorithms implemention from https://github.com/scottemmons/STHClusterAnalysis.

2. Installation
1) Unzip binary_networks.tar.gz
2) Execute the terminal command `make` inside the binary_networks directory
3) Unzip and intall mutual3.tar.gz
4) Unzip and intall clustering_programs.tar.gz
5) Unzip and intall gmap.zip

3. Main core functions:
============
This repository contains five core functions.
1) generate_real_graph.py & generate_original: generates real-graph networks and synthetic graphs used as benchmarks for cluster analysis, respectively.
2) sample.py: samples the network to the subgraphs using differnt sampling strategies.
3) cluster.py: runs various clustering algorithms over these sampled graphs.
4) measure_developing.py: measure the supervised and unsupervised evaluation metrics over clusterings of the sampled counterpart with the original graph. 
Our supervised metrcis including: NMI, ARI, Variant NMI and the new proposed metrics (i.e., \delta-precision, \delta-recall, ANC, NLS, etc.). The unsupervised metrics are modularity, conductance and coverage.
5) visualize_developing.py: visualizes, draws and analyzes the results of the clustering quality metrics. 

These core functions can be run separately for their respective functionalities. Meanwhile, the function "combined_developing_real_graph.py" intergates all the functionality of the individual files to run the entire sample clustering evaluation workflow. For example:
python combined_developing_real_graph.py -n 317080 --mu 0.4 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.15 -delta 0.8 0.9 1.0  -sac induced_random_edge
***Note that because the real grah is so large-scale and the results are big and we can not put in put in this folder, you can contact with me to ask for the preprocessed real graphs and more test codes (email: j.zhang.4@tue.nl).

Dependencies
============
The entire package is built on Python 2.7, which is required. In addition, individual files have the following dependencies:

generate_real_graph.py and generate_original.py
   - python module networkX
generate_syn.py
   - Lancich. benchmark generation "binary_networks/" @ https://sites.google.com/site/andrealancichinetti/files/binary_networks.tar.gz
sample.py
   - python module igraph
   - python module networkX
   - Sampling algorithms from "https://github.com/emrahcem/cons-python, A subfolder is created for each  graph to keep the analysis results. Inside each subfolder, a subfolder is created for each sampling method to keep the results of the sampling algorithm. 
   - all the sampling algorithms includes: 'induced_random_edge','induced_random_vertex','induced_weighted_random_vertex','kk_path','km_path','random_path','random_vertex','random_edge','random_walk','metropolis_subgraph','metropolized_random_walk','weighted_vertex'. 

cluster.py
   - Lancich. clustering repository: "clustering_programs_5_2/" @ https://sites.google.com/site/andrealancichinetti/clustering_programs.tar.gz 
   -jar package: "ModularityOptimization.jar" @ http://www.ludowaltman.nl/slm/ModularityOptimizer.jar
   - Louvain method implements modularity maximization heuristic described in the paper [Fast unfolding of community hierarchies in large networks] by V. Blondel, J.-L. Guillaume, R. Lambiotte, E. Lefebvre. 

measure_developing.py
   - The new \delta-precision, \delta-recall, ANC, NLS module 
   - python module igraph
   - python module sklearn
   - my fork of GMap "~/Documents/gmap/external/eba" @ https://github.com/scottemmons/gmap.git
   - Lancich. NMI "mutual3/" @ https://sites.google.com/site/andrealancichinetti/mutual3.tar.gz

visualize_developing.py
   - python module pandas
   - python module numpy
   - python module matplotlib (specifically matplotlib.pyplot)
   
Some example codes:
====================
1)Generate the synthetic graphs and real graphs
python generate_original.py -n 1000 --maxk 100 --mu 0.4 --minc 50 --maxc 100 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_1000/
python generate_original.py -n 1000 --maxk 100 --mu 0.4 --minc 50 --maxc 100 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_1000/
python generate_original.py -n 5000 --maxk 500 --mu 0.4 --minc 50 --maxc 500 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_5000/
python generate_original.py -n 10000 --maxk 1000 --mu 0.4 --minc 50 --maxc 1000 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_10000/
python generate_original.py -n 50000 --maxk 5000 --mu 0.4 --minc 50 --maxc 5000 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_50000/
python generate_original.py -n 100000 --maxk 10000 --mu 0.4 --minc 50 --maxc 10000 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_100000/
python generate_original.py -n 1000000 --maxk 100000 --mu 0.4 --minc 50 --maxc 100000 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_1000000/
python generate_real_graph.py -n 317080 --maxk 31708 --mu 0.5 --minc 50 --maxc 31708 -s 1 -e 1 -b /home/jzhang4/STHClusterAnalysis_real/Networks_with_ground_truth_communities/ -o generated_benches_u50_p_10_condition_induced_random_edge/n_317080/

2)Sample on the original graph using different sampling algorithms
python sample.py -n 1000  -s 1 -e 3 -o generated_benches/n_1000/ --sample_percentage  0.3 0.5 0.7 --sampling_condition induced_random_edge
python sample.py -n 65608366-s 1 -e 1 -o generated_benches_u60_p_10_condition_induced_random_edge/n_50000/ --sample_percentage 0.1 --sampling_condition induced_random_edge

3) Cluster on the subgraph using different clustering algorithms
python cluster.py -m blondel infomap label_propagation oslom modularity_optimization -sample 0.7 -t 2 -u --gpre generated_benches/n_1000/network_sample_p70_v --gsuf .dat -s 1 -e 3 --lp clustering_programs_5_2/ -o generated_benches/n_1000/
python cluster.py -m blondel infomap label_propagation oslom modularity_optimization -sample 0.7 -t 2 -u --gpre generated_benches/n_5000/network_sample_p70_v --gsuf .dat -s 1 -e 3 --lp clustering_programs_5_2/ -o generated_benches/n_5000/
python cluster.py -m blondel infomap label_propagation oslom modularity_optimization -sample 0.7 -t 2 -u --gpre generated_benches/n_10000/network_sample_p70_v --gsuf .dat -s 1 -e 3 --lp clustering_programs_5_2/ -o generated_benches/n_10000/
python cluster.py -m blondel infomap label_propagation oslom modularity_optimization -sample 0.7 -t 2 -u --gpre generated_benches/n_50000/network_sample_p70_v --gsuf .dat -s 1 -e 3 --lp clustering_programs_5_2/ -o generated_benches/n_50000/
python cluster.py -m blondel infomap label_propagation oslom modularity_optimization -sample 0.7 -t 2 -u --gpre generated_benches/n_100000/network_sample_p70_v --gsuf .dat -s 1 -e 3 --lp clustering_programs_5_2/ -o generated_benches/n_100000/

4) Measure the clustering results using various metrics
python measure.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_1000/network_sample_p70_v --gsuf .dat -u --srun --spre generated_benches/n_1000/community_sample_p70_v --ssuf .dat -s 1 -e 3 --cnames blondel infomap label_propagation oslom modularity_optimization --cpre generated_benches/n_1000/blondel_p70_clustering_v generated_benches/n_1000/infomap_p70_clustering_v generated_benches/n_1000/label_propagation_p70_clustering_v generated_benches/n_1000/oslom_p70_clustering_v generated_benches/n_1000/modularity_optimization_p70_clustering_v --csuf .dat --cnum 2 -o generated_benches/n_1000/ -delta 0.4 -sr 0.7
python measure.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_5000/network_sample_p70_v --gsuf .dat -u --srun --spre generated_benches/n_5000/community_sample_p70_v --ssuf .dat -s 1 -e 3 --cnames blondel infomap label_propagation oslom modularity_optimization --cpre generated_benches/n_5000/blondel_p70_clustering_v generated_benches/n_5000/infomap_p70_clustering_v generated_benches/n_5000/label_propagation_p70_clustering_v generated_benches/n_5000/oslom_p70_clustering_v generated_benches/n_5000/modularity_optimization_p70_clustering_v --csuf .dat --cnum 2 -o generated_benches/n_5000/
python measure.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_10000/network_sample_p70_v --gsuf .dat -u --srun --spre generated_benches/n_10000/community_sample_p70_v --ssuf .dat -s 1 -e 3 --cnames blondel infomap label_propagation oslom modularity_optimization --cpre generated_benches/n_10000/blondel_p70_clustering_v generated_benches/n_10000/infomap_p70_clustering_v generated_benches/n_10000/label_propagation_p70_clustering_v generated_benches/n_10000/oslom_p70_clustering_v generated_benches/n_10000/modularity_optimization_p70_clustering_v --csuf .dat --cnum 2 -o generated_benches/n_10000/
python measure.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_50000/network_sample_p70_v --gsuf .dat -u --srun --spre generated_benches/n_50000/community_sample_p70_v --ssuf .dat -s 1 -e 3 --cnames blondel infomap label_propagation oslom modularity_optimization --cpre generated_benches/n_50000/blondel_p70_clustering_v generated_benches/n_50000/infomap_p70_clustering_v generated_benches/n_50000/label_propagation_p70_clustering_v generated_benches/n_50000/oslom_p70_clustering_v generated_benches/n_50000/modularity_optimization_p70_clustering_v --csuf .dat --cnum 2 -o generated_benches/n_50000/
python measure_developing.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches_u50_p_10_condition_induced_random_edge/n_317080/network_sample_p10_v --gsuf .dat -u --spre generated_benches_u50_p_10_condition_induced_random_edge/n_317080/community_sample_p10_v --ssuf .dat -s 1 -e 1 --cnames blondel infomap label_propagation oslom mod_opt --cpre generated_benches_u50_p_10_condition_induced_random_edge/n_317080/blondel_p10_clustering_v generated_benches_u50_p_10_condition_induced_random_edge/n_317080/infomap_p10_clustering_v generated_benches_u50_p_10_condition_induced_random_edge/n_317080/label_propagation_p10_clustering_v generated_benches_u50_p_10_condition_induced_random_edge/n_317080/oslom_p10_clustering_v generated_benches_u50_p_10_condition_induced_random_edge/n_317080/mod_opt_p10_clustering_v --csuf .dat --cnum 1 -o generated_benches_u50_p_10_condition_induced_random_edge/n_317080/ -delta 0.8 0.9 1.0 -sr 0.1 --srun

5) Draw and analyze the metric results
python visualize_developing.py -f generated_benches_u10_p_70_condition_metropolis_subgraph/n_1000/raw_data.csv generated_benches_u10_p_70_condition_metropolis_subgraph/n_3000/raw_data.csv generated_benches_u10_p_70_condition_metropolis_subgraph/n_5000/raw_data.csv generated_benches_u10_p_70_condition_metropolis_subgraph/n_7000/raw_data.csv generated_benches_u10_p_70_condition_metropolis_subgraph/n_9000/raw_data.csv --names n_1000 n_3000 n_5000 n_7000 n_9000 --nodes 1000 3000 5000 7000 9000 --working_dir generated_benches_u10_p_70_condition_metropolis_subgraph/ 
python visualize.py -f generated_benches/n_1000/raw_data_s_1_e_3.csv generated_benches/n_5000/raw_data_s_1_e_3.csv generated_benches/n_10000/raw_data_s_1_e_3.csv generated_benches/n_50000/raw_data_s_1_e_3.csv --names n_1000 n_5000 n_10000 n_50000 --nodes 1000 5000 10000 50000

%Friendster mu=0.6
python combined_developing_real_graph.py -n 65608366--mu 0.6 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.1 -delta 0.8 0.9 1.0  -sac induced_random_edge

%DBLP mu=0.5
python combined_developing_real_graph.py -n 317080 --mu 0.5 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.1 -delta 0.8 0.9 1.0  -sac induced_random_edge
python combined_developing_real_graph.py -n 317080 --mu 0.5 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.2 -delta 0.8 0.9 1.0  -sac induced_random_edge
python combined_developing_real_graph.py -n 317080 --mu 0.5 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.3 -delta 0.8 0.9 1.0  -sac induced_random_edge
python combined_developing_real_graph.py -n 317080 --mu 0.5 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.4 -delta 0.8 0.9 1.0  -sac induced_random_edge
python combined_developing_real_graph.py -n 317080 --mu 0.5 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.5 -delta 0.8 0.9 1.0  -sac induced_random_edge

%Amzon mu=0.4 
python combined_developing_real_graph.py -n 317080 --mu 0.4 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.15 -delta 0.8 0.9 1.0  -sac induced_random_edge
python combined_developing_real_graph.py -n 317080 --mu 0.4 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.3 -delta 0.8 0.9 1.0  -sac induced_random_edge

%for mu=0.65 karate
python measure_developing.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches_u65_p_100_condition_induced_random_edge/n_34/network_sample_p100_v --gsuf .dat -u --srun --spre generated_benches_u65_p_100_condition_induced_random_edge/n_34/community_v --ssuf .dat -s 1 -e 1 --cnames blondel infomap label_propagation oslom mod_opt --cpre generated_benches_u65_p_100_condition_induced_random_edge/n_34/blondel_p100_clustering_v generated_benches_u65_p_100_condition_induced_random_edge/n_34/infomap_p100_clustering_v generated_benches_u65_p_100_condition_induced_random_edge/n_34/label_propagation_p100_clustering_v generated_benches_u65_p_100_condition_induced_random_edge/n_34/oslom_p100_clustering_v generated_benches_u65_p_100_condition_induced_random_edge/n_34/mod_opt_p100_clustering_v --csuf .dat --cnum 3 -o generated_benches_u65_p_100_condition_induced_random_edge/n_34/ -delta 0.5 0.6 0.7 0.8 0.9 1.0 -sr 1.0

%for mu=0.3 livejournal
python measure_developing.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/network_sample_p15_v --gsuf .dat -u --srun --spre generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/community_v --ssuf .dat -s 1 -e 1 --cnames blondel infomap label_propagation oslom mod_opt --cpre generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/blondel_p15_clustering_v generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/infomap_p15_clustering_v generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/label_propagation_p15_clustering_v generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/oslom_p15_clustering_v generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/mod_opt_p15_clustering_v --csuf .dat --cnum 1 -o generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/ -delta 0.5 0.6 0.7 0.8 0.9 1.0 -sr 0.15

for mu=0.2 youtube
python measure_developing.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches_u20_p_15_condition_induced_random_edge/n_72959/network_sample_p15_v --gsuf .dat -u --srun --spre generated_benches_u20_p_15_condition_induced_random_edge/n_72959/community_v --ssuf .dat -s 1 -e 1 --cnames blondel infomap label_propagation oslom mod_opt --cpre generated_benches_u20_p_15_condition_induced_random_edge/n_72959/blondel_p15_clustering_v generated_benches_u20_p_15_condition_induced_random_edge/n_72959/infomap_p15_clustering_v generated_benches_u20_p_15_condition_induced_random_edge/n_72959/label_propagation_p15_clustering_v generated_benches_u20_p_15_condition_induced_random_edge/n_72959/oslom_p15_clustering_v generated_benches_u20_p_15_condition_induced_random_edge/n_72959/mod_opt_p15_clustering_v --csuf .dat --cnum 1 -o generated_benches_u20_p_15_condition_induced_random_edge/n_72959/ -delta 0.5 0.6 0.7 0.8 0.9 1.0 -sr 0.15