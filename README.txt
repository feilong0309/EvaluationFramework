Installation
============

The brunt of installation work requires installing the package's dependencies (listed below). The package includes copies of all the dependencies that are not Python modules. All the dependencies besides the ModularityOptimizer and DEMON will need installation. Unzip all of the zip files, navigate to each resulting directory, and see the README's in each directory for installation instructions.

Example Installation Workflow
=============================

1. Unzip binary_networks.tar.gz
2. Execute the terminal command `make` inside the binary_networks directory
3. Unzip clustering_programs.tar.gz
4. Execute the terminal command `./compile.sh` inside the clustering_programs_5_2 directory. Note that this will work from a Unix terminal, and that to run the program on Windows you can install MinGW from http://www.mingw.org/ (I haven't tried to install the program on Windows)
5. Unzip mutual3.tar.gz
6. Execute the terminal command `make` inside the mutual3 directory
7. Unzip gmap.zip
8. Execute the terminal command `make` inside the gmap/external/eba directory. Note that only this subset of the entire gmap program needs to be installed.
9. Additionally, you can test whether or not ModularityOptimizer.jar works with your installed version of Java by downloading the file karate_club_network.txt from http://www.ludowaltman.nl/slm/karate_club_network.txt, running the command `java -jar ModularityOptimizer.jar karate_club_network.txt karate_club_communities.txt 1 1.0 3 10 10 0 0`, and verifying that the output file karate_club_communities.txt in your directory matches the one found at http://www.ludowaltman.nl/slm/karate_club_communities.txt; see http://www.ludowaltman.nl/slm/ for more information about ModularityOptimizer.jar.

The above workflow details the specific steps required to install the external programs which this program calls. This program also requires Python 2.7 and the scientific programming libraries listed below in the Dependencies section. I recommend installing Anaconda (https://store.continuum.io/cshop/anaconda/), a Python distribution pre-configured with many, if not all, of the Python libraries this program uses.

Use
===

This network_cluster_analysis_package contains files which each correspond to a core function.
   - generate.py generates synthetic network graphs to be used as benchmarks for cluster analysis
   - cluster.py runs clustering algorithms over these graphs
   - measure.py clusters evaluation metrics over clusterings of a network graph
   - visualize.py visualizes the results of the cluster evaluation metrics

These files can be run individually via the command line for their respective functionalities.

The file "combined.py" combines the functionality of the individual files to run a complete cluster analysis workflow. For example, if you would like to run the full workflow for sizes of N = 1000 and N = 10000 and synthetic graphs of mixing parameter = 0.4, execute the command:
  python combined.py -n 1000 10000 --mu 0.4

Alternatively, you can specify a set of the individual methods to run with the "-m" flag. This assumes that the necessary files for each individual method exist in directories of the structure that "combined.py" would create them.
For example, you could run only the generate.py functionality on graphs of size N = 1000 and of mixing parameter = 0.4 by executing the command:
  python combined.py -n 1000 --mu 0.4 -m generate
Then, you could at a later time run only the cluster.py and measure.py functionalities on the graphs of size N = 1000 that were generated earlier by executing the command:
  python combined.py -m cluster measure -n 1000 --mu 0.4

The file incrementor.py facilitates executing instances of this program in parallel by incrementing the seed for the random number generator in the binary_networks program. It should be called after executing the generate functionality of this code to increment the seed for later executions. If files are named and located according to installation defaults, no arguments to this script should be required, and it can be run with the command:
  python incrementor.py
  
Additionally, the start and end flags can be used to specify which trial numbers to execute. The defaults are start = 1 and end = 10, but the entire workflow could be run for only one trial by calling the command:
  python combined.py -n 1000 --mu 0.4
This functionality can be used to run multiple instances of the experiment in parallel. For example, to run three trials of the code in parallel, execute in parallel these three commands:
  python combined.py -n 1000 --mu 0.4 -s 1 -e 1
  python combined.py -n 1000 --mu 0.4 -s 2 -e 2
  python combined.py -n 1000 --mu 0.4 -s 3 -e 3
  
Example Use Workflow
====================

Here is a workflow for network graphs of size N = 1000 and mixing parameter = 0.4 broken down into its individual components:
1. Execute 'python combined.py -n 1000 --mu 0.4 -m generate'. This will generate synthetic graphs in the folder generated_benches/n_1000
2. Execute 'python combined.py -n 1000 --mu 0.4 -m cluster'. This will cluster the generated synthetic graphs, producing clustering files in the folder generated_benches/n_1000
3. Execute 'python combined.py -n 1000 --mu 0.4 -m measure'. This will measure the properties, using both gold standard comparison and stand-alone metrics, of the clusterings of the network graphs, producing measurement values of the prefix 'raw_data' in the folder generated_benches/n_1000
4. Execute 'python combined.py -n 1000 --mu 0.4 -m visualize'. This will create visualizations in the form of line graphs and box-and-whisker plots of the measurements produced by measure.py. The visualizations can be found in the generated_visualizations folder
5. Execute 'python incrementor.py' to increment the random number seed of the binary_networks program for future trials.

Functionality identical to the previous workflow can be achieved by using the -m flag to combine calls to combined.py:
1. Execute 'python combined.py -n 1000 --mu 0.4 -m generate cluster measure visualize'. This achieves steps 1-4 from the previous workflow.
2. Execute 'python incrementor.py' to increment the random number seed of the binary_networks program for future trials.
Note that as long as generate, cluster, measure, and visualize functionalities are called in that order, the program will execute correctly. Consequently, there are a variety of ways in which combined.py can be called to run these experiments, giving you control over which aspects of the experiments are run at any given time.

You could run fifty trials of the experiments for graphs of sizes N = 1000, N = 10000, and N = 100000 and mixing parameter = 0.4 with these commands:
1. python combined.py -n 1000 10000 100000 --mu 0.4 -m generate cluster measure visualize -s 1 -e 50
2. python incrementor.py
Note that visualize.py produces visualizations showing both how the values of one metric change with the size of the graph and comparing different metric values on one graph size.

Dependencies
============

The entire package is built on Python 2.7, which is required. In addition, individual files have the following dependencies:

generate.py
   - Lancich. benchmark generation "binary_networks/" @ https://sites.google.com/site/andrealancichinetti/files/binary_networks.tar.gz

cluster.py
   - Lancich. clustering repository "clustering_programs_5_2/" @ https://sites.google.com/site/andrealancichinetti/clustering_programs.tar.gz (Note that the version of this program in the .tar.gz file I shared is a slightly modified version of the original. Specifically, I modified the select.py and methods.py files in order not to run the 'cvis' step, which is auxiliary to the clusteirng functionality of the code and adds to its runtime.)
   - Leiden clustering jar "ModularityOptimization.jar" @ http://www.ludowaltman.nl/slm/ModularityOptimizer.jar
      - Java (i.e. JRE)
   - DEMON clustering archive, which must be unzipped into "demon_py/" @ http://www.michelecoscia.com/wp-content/uploads/2013/07/demon_py.zip
      - python module networkx

measure.py
   - python module igraph
   - python module sklearn
   - my fork of GMap "~/Documents/gmap/external/eba" @ https://github.com/scottemmons/gmap.git
   - Lancich. NMI "mutual3/" @ https://sites.google.com/site/andrealancichinetti/mutual3.tar.gz

visualize.py
   - python module pandas
   - python module numpy
   - python module matplotlib (specifically matplotlib.pyplot)

Notes
=====

Right now the combined.py code is set up to handle the random number seed correctly for 100 trials at the sizes N = 1000, 10000, 100000, and 1000000. If you want to run this experiment in a different way, look over how the random number seed is being handled and update the code accordingly to facilitate your workflow.
%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%zjp%%%%%%%%%%%%%
generate.py -n 1000 --mu 0.40 -s 1 -e 10 -b binary_networks/ -o generated_benches/n_1000/
                   -n 1000 --maxk 100 --mu 0.4 --minc 50 --maxc 100 -s 1 -e 2 -b binary_networks/ -o generated_benches/n_1000/
python generate.py -n 1000000 --maxk 10000 --mu 0.4 --minc 50 --maxc 100000 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_1000000/

cluster.py -m blondel infomap label_propagation slm -t 1 -u --gpre generated_benches/n_1000/network_v --gsuf .dat -s 1 -e 10 --lp generated_benches/n_1000/clustering_programs_5_2_s_1_e_10/ --Xmx 64m -o generated_benches/n_1000/

cluster.py -m blondel infomap label_propagation slm -t 1 -u --gpre generated_benches/n_1000/network_sample_v --gsuf .dat -s 1 -e 10 --lp clustering_programs_5_2/ -o generated_benches/n_1000/

cluster.py -m slm -t 1 -u --gpre generated_benches/n_1000/network_sample_v --gsuf .dat -s 1 -e 10 --lp clustering_programs_5_2/ -o generated_benches/n_1000/

cluster.py -m demon blondel infomap label_propagation slm -t 1 -u --gpre generated_benches/n_1000/network_v --gsuf .dat -s 1 -e 10 --lp clustering_programs_5_2/ -o generated_benches/n_1000/

======zjp add sampling======================================================
generate.py -n 1000 --maxk 100 --mu 0.4 --minc 50 --maxc 100 -s 1 -e 10 -b binary_networks/ -o generated_benches/n_1000/
generate.py -n 10000 --maxk 1000 --mu 0.4 --minc 50 --maxc 1000 -s 1 -e 10 -b binary_networks/ -o generated_benches/n_10000/
generate.py -n 50000 --maxk 5000 --mu 0.4 --minc 50 --maxc 5000 -s 1 -e 10 -b binary_networks/ -o generated_benches/n_50000/

#cluster.py -m blondel infomap label_propagation oslom demon hierarchical_infomap -sample 0.7 -t 3 -u --gpre generated_benches/n_10000/network_sample_p70_v --gsuf .dat -s 1 -e 2 --lp clustering_programs_5_2/ -o generated_benches/n_10000/

cluster.py -m blondel infomap label_propagation oslom -sample 0.7 -t 1 -u --gpre generated_benches/n_1000/network_sample_p70_v --gsuf .dat -s 1 -e 2 --lp clustering_programs_5_2/ -o generated_benches/n_1000/
cluster.py -m blondel infomap label_propagation oslom -sample 0.7 -t 3 -u --gpre generated_benches/n_10000/network_sample_p70_v --gsuf .dat -s 1 -e 2 --lp clustering_programs_5_2/ -o generated_benches/n_10000/

python cluster.py -m demon -sample 0.7 -t 3 -u --gpre generated_benches/n_1000/network_sample_p70_v --gsuf .dat -s 1 -e 2 --lp clustering_programs_5_2/ -o generated_benches/n_1000/

time python select.py -n /home/feilong0309/STHClusterAnalysis/generated_benches/n_10000/network_sample_p70_v1.dat -p 6 -f /home/feilong0309/STHClusterAnalysis/scratch_folder_s_1_e_2 -c 1

python launch.py /home/feilong0309/STHClusterAnalysis/generated_benches/n_10000/network_sample_p70_v1.dat

--gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_1000/network_v --gsuf .dat -u --srun --spre generated_benches/n_1000/community_v --ssuf .dat -s 1 -e 10 --cnames blondel infomap label_propagation slm --cpre generated_benches/n_1000/blondel_clustering_v generated_benches/n_1000/infomap_clustering_v generated_benches/n_1000/label_propagation_clustering_v generated_benches/n_1000/slm_clustering_v --csuf .dat --cnum 1 -o generated_benches/n_1000/
--gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_10000/network_sample_p70_v --gsuf .dat -u --srun --spre generated_benches/n_10000/community_sample_p70_v --ssuf .dat -s 1 -e 2 --cnames blondel infomap label_propagation oslom demon --cpre generated_benches/n_10000/blondel_p70_clustering_v generated_benches/n_10000/infomap_p70_clustering_v generated_benches/n_10000/label_propagation_p70_clustering_v generated_benches/n_10000/oslom_p70_clustering_v generated_benches/n_10000/demon_p70_clustering_v --csuf .dat --cnum 3 -o generated_benches/n_10000/





=======zjp add multiple trails==================
generate.py -n 1000 --maxk 100 --mu 0.4 --minc 50 --maxc 100 -s 1 -e 2 -b binary_networks/ -o generated_benches/n_1000/
generate.py -n 1000000 --maxk 10000 --mu 0.4 --minc 50 --maxc 100000 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_1000000/

cluster.py -m blondel infomap label_propagation -sample 0.7 -t 10 -u --gpre generated_benches/n_1000/network_sample_p70_v --gsuf .dat -s 1 -e 2 --lp clustering_programs_5_2/ -o generated_benches/n_1000/

python cluster.py -m demon blondel infomap slm label_propagation -sample 0.7 -t 3 -u --gpre generated_benches/n_1000/network_sample_p70_v --gsuf .dat -s 1 -e 2 --lp clustering_programs_5_2/ -o generated_benches/n_1000/

python cluster.py -m demon -sample 0.7 -t 3 -u --gpre generated_benches/n_1000/network_sample_p70_v --gsuf .dat -s 1 -e 2 --lp clustering_programs_5_2/ -o generated_benches/n_1000/

--gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_1000/network_v --gsuf .dat -u --srun --spre generated_benches/n_1000/community_v --ssuf .dat -s 1 -e 10 --cnames blondel infomap label_propagation slm --cpre generated_benches/n_1000/blondel_clustering_v generated_benches/n_1000/infomap_clustering_v generated_benches/n_1000/label_propagation_clustering_v generated_benches/n_1000/slm_clustering_v --csuf .dat --cnum 1 -o generated_benches/n_1000/


time java -Xmx64m -jar ModularityOptimizer.jar /home/feilong0309/STHClusterAnalysis/generated_benches/n_1000/network_sample_v1.dat
clustering_programs_5_2/modopt_output.txt 1 1.0 3 10 10 665601941440778278 0

--gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_1000/network_sample_p70_v --gsuf .dat -u --srun --spre generated_benches/n_1000/community_sample_p70_v --ssuf .dat -s 1 -e 2 --cnames blondel infomap label_propagation --cpre generated_benches/n_1000/blondel_p70_clustering_v generated_benches/n_1000/infomap_p70_clustering_v generated_benches/n_1000/label_propagation_p70_clustering_v --csuf .dat --cnum 3 -o generated_benches/n_1000/


python combined.py -m visualize -n 1000 --mu 0.4 -s 1 -e 2 -t 2
python combined.py -n 1000 10000 100000 --mu 0.4 -m visualize -s 1 -e 2


#sed â€˜s/\t/ /gâ€?network_sample_p70_v1.dat >network_sample_p70_v1.txt
java -jar ModularityOptimizer.jar network_sample_p70_v1.txt 1 1.0 3 10 10 0 0

python cluster.py -m oslom modularity_optimization -sample 0.7 -t 2 -u --gpre generated_benches/n_100000/network_sample_p70_v --gsuf .dat -s 1 -e 3 --lp clustering_programs_5_2/ -o generated_benches/n_100000/

=============importort sampling designed by jianpeng zhang ===================================
scp /etc/lilo.conf k@net67.ee.oit.edu.tw:/home/k
 
python generate_original.py -n 1000 --maxk 100 --mu 0.4 --minc 50 --maxc 100 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_1000/
python sample.py -n 1000  -s 1 -e 3 -o generated_benches/n_1000/ --sample_percentage  0.3 0.5 0.7 --sampling_condition induced_random_edge
sampling_conditions = ['induced_random_edge','induced_random_vertex','induced_weighted_random_vertex','kk_path','km_path','random_path','random_vertex','random_edge','random_walk','metropolis_subgraph','metropolized_random_walk','weighted_vertex']

python measure_developing.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches_u10_p_70_condition_metropolis_subgraph/n_1000/network_sample_p70_v --gsuf .dat -u --srun --spre generated_benches_u10_p_70_condition_metropolis_subgraph/n_1000/community_sample_p70_v --ssuf .dat -s 1 -e 2 --cnames blondel infomap label_propagation oslom modularity_optimization --cpre generated_benches_u10_p_70_condition_metropolis_subgraph/n_1000/blondel_p70_clustering_v generated_benches_u10_p_70_condition_metropolis_subgraph/n_1000/infomap_p70_clustering_v generated_benches_u10_p_70_condition_metropolis_subgraph/n_1000/label_propagation_p70_clustering_v generated_benches_u10_p_70_condition_metropolis_subgraph/n_1000/oslom_p70_clustering_v generated_benches_u10_p_70_condition_metropolis_subgraph/n_1000/modularity_optimization_p70_clustering_v --csuf .dat --cnum 2 -o generated_benches_u10_p_70_condition_metropolis_subgraph/n_1000/ -delta 0.4 0.5 -sr 0.7

python visualize_developing.py -f generated_benches_u10_p_70_condition_metropolis_subgraph/n_1000/raw_data.csv generated_benches_u10_p_70_condition_metropolis_subgraph/n_3000/raw_data.csv generated_benches_u10_p_70_condition_metropolis_subgraph/n_5000/raw_data.csv generated_benches_u10_p_70_condition_metropolis_subgraph/n_7000/raw_data.csv generated_benches_u10_p_70_condition_metropolis_subgraph/n_9000/raw_data.csv --names n_1000 n_3000 n_5000 n_7000 n_9000 --nodes 1000 3000 5000 7000 9000 --working_dir generated_benches_u10_p_70_condition_metropolis_subgraph/ 

======zhangjianpeng add sampling======================================================
python generate.py -n 1000 --maxk 100 --mu 0.4 --minc 50 --maxc 100 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_1000/
python generate.py -n 5000 --maxk 500 --mu 0.4 --minc 50 --maxc 500 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_5000/
python generate.py -n 10000 --maxk 1000 --mu 0.4 --minc 50 --maxc 1000 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_10000/
python generate.py -n 50000 --maxk 5000 --mu 0.4 --minc 50 --maxc 5000 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_50000/
python generate.py -n 100000 --maxk 10000 --mu 0.4 --minc 50 --maxc 10000 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_100000/
%%%%python generate.py -n 1000000 --maxk 100000 --mu 0.4 --minc 50 --maxc 100000 -s 1 -e 3 -b binary_networks/ -o generated_benches/n_1000000/

python cluster.py -m blondel infomap label_propagation oslom modularity_optimization -sample 0.7 -t 2 -u --gpre generated_benches/n_1000/network_sample_p70_v --gsuf .dat -s 1 -e 3 --lp clustering_programs_5_2/ -o generated_benches/n_1000/
python cluster.py -m blondel infomap label_propagation oslom modularity_optimization -sample 0.7 -t 2 -u --gpre generated_benches/n_5000/network_sample_p70_v --gsuf .dat -s 1 -e 3 --lp clustering_programs_5_2/ -o generated_benches/n_5000/
python cluster.py -m blondel infomap label_propagation oslom modularity_optimization -sample 0.7 -t 2 -u --gpre generated_benches/n_10000/network_sample_p70_v --gsuf .dat -s 1 -e 3 --lp clustering_programs_5_2/ -o generated_benches/n_10000/
python cluster.py -m blondel infomap label_propagation oslom modularity_optimization -sample 0.7 -t 2 -u --gpre generated_benches/n_50000/network_sample_p70_v --gsuf .dat -s 1 -e 3 --lp clustering_programs_5_2/ -o generated_benches/n_50000/
python cluster.py -m blondel infomap label_propagation oslom modularity_optimization -sample 0.7 -t 2 -u --gpre generated_benches/n_100000/network_sample_p70_v --gsuf .dat -s 1 -e 3 --lp clustering_programs_5_2/ -o generated_benches/n_100000/

python measure.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_1000/network_sample_p70_v --gsuf .dat -u --srun --spre generated_benches/n_1000/community_sample_p70_v --ssuf .dat -s 1 -e 3 --cnames blondel infomap label_propagation oslom modularity_optimization --cpre generated_benches/n_1000/blondel_p70_clustering_v generated_benches/n_1000/infomap_p70_clustering_v generated_benches/n_1000/label_propagation_p70_clustering_v generated_benches/n_1000/oslom_p70_clustering_v generated_benches/n_1000/modularity_optimization_p70_clustering_v --csuf .dat --cnum 2 -o generated_benches/n_1000/ -delta 0.4 -sr 0.7
python measure.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_5000/network_sample_p70_v --gsuf .dat -u --srun --spre generated_benches/n_5000/community_sample_p70_v --ssuf .dat -s 1 -e 3 --cnames blondel infomap label_propagation oslom modularity_optimization --cpre generated_benches/n_5000/blondel_p70_clustering_v generated_benches/n_5000/infomap_p70_clustering_v generated_benches/n_5000/label_propagation_p70_clustering_v generated_benches/n_5000/oslom_p70_clustering_v generated_benches/n_5000/modularity_optimization_p70_clustering_v --csuf .dat --cnum 2 -o generated_benches/n_5000/
python measure.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_10000/network_sample_p70_v --gsuf .dat -u --srun --spre generated_benches/n_10000/community_sample_p70_v --ssuf .dat -s 1 -e 3 --cnames blondel infomap label_propagation oslom modularity_optimization --cpre generated_benches/n_10000/blondel_p70_clustering_v generated_benches/n_10000/infomap_p70_clustering_v generated_benches/n_10000/label_propagation_p70_clustering_v generated_benches/n_10000/oslom_p70_clustering_v generated_benches/n_10000/modularity_optimization_p70_clustering_v --csuf .dat --cnum 2 -o generated_benches/n_10000/
python measure.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches/n_50000/network_sample_p70_v --gsuf .dat -u --srun --spre generated_benches/n_50000/community_sample_p70_v --ssuf .dat -s 1 -e 3 --cnames blondel infomap label_propagation oslom modularity_optimization --cpre generated_benches/n_50000/blondel_p70_clustering_v generated_benches/n_50000/infomap_p70_clustering_v generated_benches/n_50000/label_propagation_p70_clustering_v generated_benches/n_50000/oslom_p70_clustering_v generated_benches/n_50000/modularity_optimization_p70_clustering_v --csuf .dat --cnum 2 -o generated_benches/n_50000/

python visualize.py -f generated_benches/n_1000/raw_data.csv --names n_1000 --nodes 1000
python visualize.py -f generated_benches/n_1000/raw_data_s_1_e_3.csv generated_benches/n_5000/raw_data_s_1_e_3.csv generated_benches/n_10000/raw_data_s_1_e_3.csv generated_benches/n_50000/raw_data_s_1_e_3.csv --names n_1000 n_5000 n_10000 n_50000 --nodes 1000 5000 10000 50000

#The real data test will put in this folder, and just change the name of network and commuities.

%Friendster mu=0.6
python combined_developing_real_graph.py -n 65608366--mu 0.6 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.1 -delta 0.8 0.9 1.0  -sac induced_random_edge
python sample.py -n 65608366-s 1 -e 1 -o generated_benches_u60_p_10_condition_induced_random_edge/n_50000/ --sample_percentage 0.1 --sampling_condition induced_random_edge

%DBLP mu=0.5
python combined_developing_real_graph.py -n 317080 --mu 0.5 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.1 -delta 0.8 0.9 1.0  -sac induced_random_edge
python combined_developing_real_graph.py -n 317080 --mu 0.5 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.2 -delta 0.8 0.9 1.0  -sac induced_random_edge
python combined_developing_real_graph.py -n 317080 --mu 0.5 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.3 -delta 0.8 0.9 1.0  -sac induced_random_edge
python combined_developing_real_graph.py -n 317080 --mu 0.5 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.4 -delta 0.8 0.9 1.0  -sac induced_random_edge
python combined_developing_real_graph.py -n 317080 --mu 0.5 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.5 -delta 0.8 0.9 1.0  -sac induced_random_edge

python combined_developing_real_graph.py -n 317080 --mu 0.5 -m measure visualize -s 1 -e 1 -t 1 -sr 0.1 -delta 0.8 0.9 1.0  -sac induced_random_edge

python generate_real_graph.py -n 317080 --maxk 31708 --mu 0.5 --minc 50 --maxc 31708 -s 1 -e 1 -b /home/jzhang4/STHClusterAnalysis_real/Networks_with_ground_truth_communities/ -o generated_benches_u50_p_10_condition_induced_random_edge/n_317080/

python measure_developing.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches_u50_p_10_condition_induced_random_edge/n_317080/network_sample_p10_v --gsuf .dat -u --spre generated_benches_u50_p_10_condition_induced_random_edge/n_317080/community_sample_p10_v --ssuf .dat -s 1 -e 1 --cnames blondel infomap label_propagation oslom mod_opt --cpre generated_benches_u50_p_10_condition_induced_random_edge/n_317080/blondel_p10_clustering_v generated_benches_u50_p_10_condition_induced_random_edge/n_317080/infomap_p10_clustering_v generated_benches_u50_p_10_condition_induced_random_edge/n_317080/label_propagation_p10_clustering_v generated_benches_u50_p_10_condition_induced_random_edge/n_317080/oslom_p10_clustering_v generated_benches_u50_p_10_condition_induced_random_edge/n_317080/mod_opt_p10_clustering_v --csuf .dat --cnum 1 -o generated_benches_u50_p_10_condition_induced_random_edge/n_317080/ -delta 0.8 0.9 1.0 -sr 0.1 --srun




%For mu=0.4 amzon
python combined_developing_real_graph.py -n 317080 --mu 0.4 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.15 -delta 0.8 0.9 1.0  -sac induced_random_edge
python combined_developing_real_graph.py -n 317080 --mu 0.4 -m generate sample cluster measure visualize -s 1 -e 1 -t 1 -sr 0.3 -delta 0.8 0.9 1.0  -sac induced_random_edge

%for mu=0.65 karate
python measure_developing.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches_u65_p_100_condition_induced_random_edge/n_34/network_sample_p100_v --gsuf .dat -u --srun --spre generated_benches_u65_p_100_condition_induced_random_edge/n_34/community_v --ssuf .dat -s 1 -e 1 --cnames blondel infomap label_propagation oslom mod_opt --cpre generated_benches_u65_p_100_condition_induced_random_edge/n_34/blondel_p100_clustering_v generated_benches_u65_p_100_condition_induced_random_edge/n_34/infomap_p100_clustering_v generated_benches_u65_p_100_condition_induced_random_edge/n_34/label_propagation_p100_clustering_v generated_benches_u65_p_100_condition_induced_random_edge/n_34/oslom_p100_clustering_v generated_benches_u65_p_100_condition_induced_random_edge/n_34/mod_opt_p100_clustering_v --csuf .dat --cnum 3 -o generated_benches_u65_p_100_condition_induced_random_edge/n_34/ -delta 0.5 0.6 0.7 0.8 0.9 1.0 -sr 1.0

%for mu=0.3 livejournal
python measure_developing.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/network_sample_p15_v --gsuf .dat -u --srun --spre generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/community_v --ssuf .dat -s 1 -e 1 --cnames blondel infomap label_propagation oslom mod_opt --cpre generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/blondel_p15_clustering_v generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/infomap_p15_clustering_v generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/label_propagation_p15_clustering_v generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/oslom_p15_clustering_v generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/mod_opt_p15_clustering_v --csuf .dat --cnum 1 -o generated_benches_u30_p_15_condition_induced_random_vertex/n_139012/ -delta 0.5 0.6 0.7 0.8 0.9 1.0 -sr 0.15

for mu=0.2 youtube
python measure_developing.py --gmap gmap/ --lnmi mutual3/ --gpre generated_benches_u20_p_15_condition_induced_random_edge/n_72959/network_sample_p15_v --gsuf .dat -u --srun --spre generated_benches_u20_p_15_condition_induced_random_edge/n_72959/community_v --ssuf .dat -s 1 -e 1 --cnames blondel infomap label_propagation oslom mod_opt --cpre generated_benches_u20_p_15_condition_induced_random_edge/n_72959/blondel_p15_clustering_v generated_benches_u20_p_15_condition_induced_random_edge/n_72959/infomap_p15_clustering_v generated_benches_u20_p_15_condition_induced_random_edge/n_72959/label_propagation_p15_clustering_v generated_benches_u20_p_15_condition_induced_random_edge/n_72959/oslom_p15_clustering_v generated_benches_u20_p_15_condition_induced_random_edge/n_72959/mod_opt_p15_clustering_v --csuf .dat --cnum 1 -o generated_benches_u20_p_15_condition_induced_random_edge/n_72959/ -delta 0.5 0.6 0.7 0.8 0.9 1.0 -sr 0.15
