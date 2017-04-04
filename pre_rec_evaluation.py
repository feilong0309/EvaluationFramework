from __future__ import division
'''
Created on 25 Nov 2015

@author: Administrator
'''
'''
Created on 24 Nov 2015

@author: Administrator
'''
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.cluster import normalized_mutual_info_score
import copy
import time
import networkx as nx
import matplotlib.pyplot as plt
import os
import time

def DeltaCoverage_sep(s1, s2, threshold, sample):
#    delta = len(s1 & s2) * 1.0 / len(s2 | s1)
#    print("intersection of two set is %d" % (len(s1 & s2)))
#    print("union of two set is %d" % (len(s1 | s2)))

    delta = len(s1 & s2) * 1.0 / len(s2)
    delta2 = len(s1 & s2) * 1.0 / (len(s1) * sample)
#    delta3 = len(s1 & s2)
#    if delta>= threshold and delta3>= 5:#threshold:       
    if delta>= threshold and delta2>= threshold:#threshold:    
        print("\n\n\nnew original set:delta=%0.2f, delta2=%0.2f\n"%(delta, delta2))
#        print(list(s1))
#        print("sample set \n")
#        print(list(s2))   
#        time.sleep(5)
        return 1
        
#    if delta>= threshold or delta2>= 0.5:#threshold:
#        return True 
    elif delta>= threshold:
        return 2
    
    else:
        return 3
        
def Compare3_backup(s1, s2, deltas, sample):
    result_lines = []
    precision = 0.0
    recall = 0.0

    sample_block_num= 0
    original_block_num = 0
    block_size=[]
    block_size_median=0
    
    for kk1, vv1 in s1.items():
        if len(vv1)>2:
            original_block_num=original_block_num+1
            
    
    for kk2, vv2 in s2.items():
        if len(vv2)>2:
            sample_block_num=sample_block_num+1
            block_size.append(len(vv2))
    block_size_median = np.median(block_size)

    for delta in deltas:
        res1 = set()       
        res2 = set()
        res3 = set()
        res2.clear()
        res1.clear()
        c1={}
        c2={}
        c1=copy.deepcopy(s1)
        c2=copy.deepcopy(s2)
#        print('c1 length is %d\n' %len(c1))
#        print('c2 length is %d\n' %len(c2))
#        time.sleep(5)
       
        for k2, v2 in c2.items():
            for k1, v1 in c1.items():
                if len(v2)>2 and len(v1)>2: 
                    if Coverage(v1, v2):
                        res1.add(k1)
#                    if DeltaCoverage(v1, v2, float(delta), sample):
#                        res2.add(k1)
#                        res3.add(k2)
                        #c1.pop(k1)
                    if DeltaCoverage_sep(v1, v2, float(delta), sample)==1:
                        res2.add(k1)
                        res3.add(k2)
                    elif DeltaCoverage_sep(v1, v2, float(delta), sample)==2:
                        res3.add(k2)
                    else:
                        continue

        delta_precison = len(res3) * 1.0 / sample_block_num
        delta_recall = len(res2) * 1.0 / original_block_num
        
        if delta_precison+delta_recall !=0:
            delta_composite = 2.0*delta_precison*delta_recall* 1.0 / (delta_precison+delta_recall)
        else:
            delta_composite = 0
        
        print (len(res1), len(res2))
        print ('---------------------------------')
        print ('Delta F-measure with delta (' + str(delta) + '): ' + str(delta_composite))   
        print ('Delta Precision with delta (' + str(delta) + '): ' + str(delta_precison))
        print ('Delta Recall with delta (' + str(delta) + '): ' + str(delta_recall))    
        result_lines.append([str(delta)+'_precison', 'Entire Graph', delta_precison])
        result_lines.append([str(delta)+'_recall', 'Entire Graph', delta_recall])
        result_lines.append([str(delta)+'_composite', 'Entire Graph', delta_composite])
    
#    precision = len(res1) * 1.0 / sample_block_num
#    recall = len(res1) * 1.0 / original_block_num
#    print ('Precision: ' + str(precision))
#    print ('Recall: ' + str(recall))
#    result_lines.append(['Precison', 'Entire Graph', precision])
#    result_lines.append(['Recall', 'Entire Graph', recall])

    print ('block_size_median: ' + str(block_size_median))
    print ('sample_block_num: ' + str(sample_block_num))
    print ('original_block_num: ' + str(original_block_num))
    result_lines.append(['Block_size_median', 'Entire Graph', block_size_median])
    result_lines.append(['Sample_block_num', 'Entire Graph', sample_block_num])
    result_lines.append(['Original_block_num', 'Entire Graph', original_block_num])
    return result_lines

def purity_score(clusters, classes):
    """
    Calculate the purity score for the given cluster assignments and ground truth classes
    
    :param clusters: the cluster assignments array
    :type clusters: numpy.array
    
    :param classes: the ground truth classes
    :type classes: numpy.array
    
    :returns: the purity score
    :rtype: float
    """
    
    A = np.c_[(clusters,classes)]
    
    n_accurate = 0.

    for j in np.unique(A[:,0]):
        z = A[A[:,0] == j, 1]
        x = np.argmax(np.bincount(z))
        n_accurate += len(z[z == x])

    return n_accurate / A.shape[0]

def ReadInData(filename):
    clusters = {}
    fin = open(filename, 'r')
    for line in fin.readlines():
        res = line.strip().split()
        if clusters.has_key(int(res[1])):
            ids = clusters.get(int(res[1]))
            ids.add(int(res[0]))
            clusters[int(res[1])] = ids
        else:
            ids = set()
            ids.add(int(res[0]))
            clusters[int(res[1])] = ids
    fin.close()
    return clusters

def Coverage(s1, s2):
    if s1.issuperset(s2) and len(s2)>3:
        return True
    else:
        return False


def Compare(c1, c2):
    result_lines = []
    precision = 0.0
    recall = 0.0
    delta = 0.7
    sample = 0.7
    res1 = set()
    res2 = set()
    for k2, v2 in c2.items():
        for k1, v1 in c1.items():
            if len(c2)>3: 
                if Coverage(v1, v2):
                   res1.add(k1)
                if DeltaCoverage(v1, v2, delta, sample):
                   res2.add(k1)
                   c1.pop(k1)
#                   c2.pop(k2)
        
    precision = len(res1) * 1.0 / len(c2)
    recall = len(res1) * 1.0 / len(c1)
    delta_precison = len(res2) * 1.0 / len(c2)
    delta_recall = len(res2) * 1.0 / len(c1)
    print (len(res1), len(res2))
    print ('Precision: ' + str(len(res1) * 1.0 / len(c2)))
    print ('Recall: ' + str(len(res1) * 1.0 / len(c1)))
    print ('---------------------------------')
    print ('Delta Precision with delta (' + str(delta) + '): ' + str(len(res2) * 1.0 / len(c2)))
    print ('Delta Recall with delta (' + str(delta) + '): ' + str(len(res2) * 1.0 / len(c1)))
    result_lines.append(['Precison', 'Entire Graph', precision])
    result_lines.append(['Recall', 'Entire Graph', recall])    
    result_lines.append(['delta_precison', 'Entire Graph', delta_precison])
    result_lines.append(['delta_recall', 'Entire Graph', delta_recall])
    return result_lines

def Compare2(c1, c2, delta, sample):
    result_lines = []
    precision = 0.0
    recall = 0.0
 #   delta = 0.7
 #   sample = 0.7
    res1 = set()
    res2 = set()
    for k2, v2 in c2.items():
        for k1, v1 in c1.items():
            if len(c2)>3: 
                if Coverage(v1, v2):
                   res1.add(k1)
                if DeltaCoverage(v1, v2, delta, sample):
                   res2.add(k1)
                   c1.pop(k1)
                   c2.pop(k2)
    precision = len(res1) * 1.0 / len(c2)
    recall = len(res1) * 1.0 / len(c1)
    delta_precison = len(res2) * 1.0 / len(c2)
    delta_recall = len(res2) * 1.0 / len(c1)
    print (len(res1), len(res2))
    print ('Precision: ' + str(len(res1) * 1.0 / len(c2)))
    print ('Recall: ' + str(len(res1) * 1.0 / len(c1)))
    print ('---------------------------------')
    print ('Delta Precision with delta (' + str(delta) + '): ' + str(len(res2) * 1.0 / len(c2)))
    print ('Delta Recall with delta (' + str(delta) + '): ' + str(len(res2) * 1.0 / len(c1)))
    result_lines.append(['Precison', 'Entire Graph', precision])
    result_lines.append(['Recall', 'Entire Graph', recall])    
    result_lines.append(['delta_precison', 'Entire Graph', delta_precison])
    result_lines.append(['delta_recall', 'Entire Graph', delta_recall])
    return result_lines
    
def Compare4(s1, s2, deltas, sample):
    result_lines = []
    precision = 0.0
    recall = 0.0

    sample_block_num= len(s2)
    original_block_num = len(s1)

    for delta in deltas:
        res1 = set()       
        res2 = set()
        res2.clear()
        res1.clear()
        c1={}
        c2={}
        c1=copy.deepcopy(s1)
        c2=copy.deepcopy(s2)
#        print('c1 length is %d\n' %len(c1))
#        print('c2 length is %d\n' %len(c2))
#        time.sleep(5)
        
        for k2, v2 in c2.items():
            for k1, v1 in c1.items():
                if len(v2)>2: 
                    if Coverage(v1, v2):
                        res1.add(k1)
                    if DeltaCoverage(v1, v2, float(delta), sample):
                        res2.add(k1)
                        c1.pop(k1)
#                        c2.pop(k2)

        delta_precison = len(res2) * 1.0 / sample_block_num
        delta_recall = len(res2) * 1.0 / original_block_num
        if delta_precison+delta_recall !=0:
            delta_composite = 2.0*delta_precison*delta_recall* 1.0 / (delta_precison+delta_recall)
        else:
            delta_composite=0
            
        print (len(res1), len(res2))
        print ('---------------------------------')
        print ('Delta Precision with delta (' + str(delta) + '): ' + str(delta_precison))
        print ('Delta Recall with delta (' + str(delta) + '): ' + str(delta_recall))
        print ('Delta F-measure with delta (' + str(delta) + '): ' + str(delta_composite))      
        result_lines.append([str(delta)+'_precison', 'Entire Graph', delta_precison])
        result_lines.append([str(delta)+'_recall', 'Entire Graph', delta_recall])
        result_lines.append([str(delta)+'_composite', 'Entire Graph', delta_composite])
    
    precision = len(res1) * 1.0 / sample_block_num
    recall = len(res1) * 1.0 / original_block_num
    print ('Precision: ' + str(precision))
    print ('Recall: ' + str(recall))
    result_lines.append(['Precison', 'Entire Graph', precision])
    result_lines.append(['Recall', 'Entire Graph', recall])
    return result_lines

def DeltaCoverage(s1, s2, threshold, sample):
#    delta = len(s1 & s2) * 1.0 / len(s2 | s1)
#    print("intersection of two set is %d" % (len(s1 & s2)))
#    print("union of two set is %d" % (len(s1 | s2)))

    delta = len(s1 & s2) * 1.0 / len(s2)
    delta2 = len(s1 & s2) * 1.0 / (len(s1) * sample)
    delta3 = len(s1 & s2)
    if delta>= threshold and delta3>= 3:#threshold:       
#    if delta>= threshold and delta2>= 0.5:#threshold:    
        print("\n\n\nnew original set:delta=%0.2f, delta2=%0.2f\n"%(delta, delta2))
#        print(list(s1))
#        print("sample set \n")
#        print(list(s2))   
#        time.sleep(5)
        return True
        
#    if delta>= threshold or delta2>= 0.5:#threshold:
#        return True 
    else:
        return False
        
def DeltaCoverage_weighted(s1, s2, threshold, sample):
#    delta = len(s1 & s2) * 1.0 / len(s2 | s1)
#    print("intersection of two set is %d" % (len(s1 & s2)))
#    print("union of two set is %d" % (len(s1 | s2)))

#    delta = len(s1 & s2) * 1.0 / len(s2)
    delta = len(s1 & s2) * 1.0 / min(len(s2),len(s1))
    delta2 = len(s1 & s2) * 1.0 / (len(s1) * sample)
    delta3 = len(s1 & s2)
    if delta>= threshold and delta3>= 2:#threshold:       
#    if delta>= threshold and delta2>= 0.5:#threshold:    
#        print("\n\n\nnew original set:delta=%0.2f, delta2=%0.2f\n"%(delta, delta2))
#        print(list(s1))
#        print("sample set \n")
#        print(list(s2))   
#        time.sleep(5)
        return True
        
#    if delta>= threshold or delta2>= 0.5:#threshold:
#        return True 
    else:
        return False

def delta_rank_match_plot(block_match_ratio,clustering_current):
    
    block_match_ratio_sequence=sorted(block_match_ratio,reverse=True) # degree sequence
    #print "Degree sequence", degree_sequence
    dmax=max(block_match_ratio_sequence)
    
    num_of_block=len(block_match_ratio_sequence)
    
#    fig, ax= plt.figure() #size of the whole graph
    fig = plt.figure()
    ax = fig.add_subplot(111)
#    fig, ax= plt.figure(figsize=(16, 20)) #size of the whole graph
#    fig.subplots_adjust(wspace=0.5, hspace=0.5, top=0.90, bottom=0.05)
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(18)

#    plt.loglog(degree_sequence,'b-',marker='o')
    x=[(i+1)/float(num_of_block) for i in range(num_of_block)]
    plt.plot(x, block_match_ratio_sequence,'b-',marker='o', markersize=8)
#    plt.bar(block_match_ratio_sequence)
    plt.title("Block match ratio plot", fontsize=18)
    plt.ylabel("value")
    plt.xlabel("rank")
    plt.ylim([0,1.1])
    plt.xlim([1/float(num_of_block) ,1.0])
    
    

    output_file = clustering_current.split('.')[0]+"_rank_match_plot.pdf"
    plt.savefig(output_file, format='pdf', dpi=1200)
#    plt.show()
    
def match_ratio(c1,c2):
    res_match=[]
    for k1, v1 in c1.items():
        max_match_sample= 0#for each sample block, initiate the max_mathch=0
        match_sample_block=set()
        for k2, v2 in c2.items():
            if len(v2)>2 and len(v1)>2:                  
                intection_set_len = len(v1 & v2)                        
                if intection_set_len > max_match_sample:
                    max_match_sample = intection_set_len
                    match_sample_block=v2
                else:
#                   print('no lager match')
                    continue                                                                              
        res_match.append((len(match_sample_block & v1) * 1.0)/len(v1))#original
    return res_match
def Compare3(s1, s2, deltas, sample, clustering_current):
    result_lines = []
    precision = 0.0
    recall = 0.0

    sample_block_num= 0
    original_block_num = 0
    block_size=[]
    block_size_median=0
    
    for kk1, vv1 in s1.items():
        if len(vv1)>2:
            original_block_num=original_block_num+1
            
    
    for kk2, vv2 in s2.items():
        if len(vv2)>2:
            sample_block_num=sample_block_num+1
            block_size.append(len(vv2))
    block_size_median = np.median(block_size)

    for delta in deltas:
        res1 = set()       
        res2 = set()
        res3 = set()
        res_orig=list()
        res_samp=list()
        res2.clear()
        res1.clear()
        c1={}
        c2={}
        c1=copy.deepcopy(s1)
        c2=copy.deepcopy(s2)
#        print('c1 length is %d\n' %len(c1))
#        print('c2 length is %d\n' %len(c2))
#        time.sleep(5)

#        delta-coverage(pi(S)) for precision       
        for k2, v2 in c2.items():
            max_match_orig= 0#for each sample block, initiate the max_mathch=0
            match_orig_block=set()
            for k1, v1 in c1.items():
                if len(v2)>2 and len(v1)>2: 
#                    if Coverage(v1, v2):
#                        res1.add(k1)
#                    if DeltaCoverage(v1, v2, float(delta), sample):
#                        res2.add(k1)
#                        res3.add(k2)
                        #c1.pop(k1)
#                    if DeltaCoverage_sep(v1, v2, float(delta), sample)==1:
#                        res2.add(k1)# original, because of sampling, mapbe it is too low.
#                        res3.add(k2)# sampling 
#                    elif DeltaCoverage_sep(v1, v2, float(delta), sample)==2:
#                        res3.add(k2)
#                    else:
#                        continue                    
                    if DeltaCoverage_weighted(v1, v2, float(delta), sample):
                        intection_set_len = len(v1 & v2)                        
                        if intection_set_len > max_match_orig:
                            max_match_orig = intection_set_len
                            match_orig_block=v1
                        else:
                        
#                            print('no lager match')
#                            print(intection_set_len)
                            continue
                else:
#                    print('less than 3 clusters.')
#                    print("sample set")
#                    print(list(v2))
                    continue                                                                                
            res_samp.append((len(match_orig_block & v2) * 1.0)/len(v2))#sample
            
#        delta-coverage(pi(G)) for recall.  
        for k1, v1 in c1.items():
            max_match_sample= 0#for each sample block, initiate the max_mathch=0
            match_sample_block=set()
            for k2, v2 in c2.items():
                if len(v2)>2 and len(v1)>2:                  
                    if DeltaCoverage_weighted(v1, v2, float(delta), sample):
                        intection_set_len = len(v1 & v2)                        
                        if intection_set_len > max_match_sample:
                            max_match_sample = intection_set_len
                            match_sample_block=v2
                        else:
#                            print('no lager match')
                            continue
                else:
#                    print('less than 3 clusters.')
                    continue                                                                                
            res_orig.append((len(match_sample_block & v1) * 1.0)/len(v1))#original
        
        sum_weight_coverage_S = sum(res_samp)
        sum_weight_coverage_G = sum(res_orig)
        delta_precison = sum_weight_coverage_S * 1.0 / sample_block_num
        delta_recall = sum_weight_coverage_G * 1.0 / original_block_num        
#        delta_precison = len(res3) * 1.0 / sample_block_num
#        delta_recall = len(res2) * 1.0 / original_block_num
        
        if delta_precison+delta_recall !=0:
            delta_composite = 2.0*delta_precison*delta_recall* 1.0 / (delta_precison+delta_recall)
        else:
            delta_composite = 0
        
        print (len(res2), len(res3))
        print ('---------------------------------')
  
        print ('Delta Precision with delta (' + str(delta) + '): ' + str(delta_precison))
        print ('Delta Recall with delta (' + str(delta) + '): ' + str(delta_recall)) 
        print ('Delta F-measure with delta (' + str(delta) + '): ' + str(delta_composite)) 
        result_lines.append([str(delta)+'_precison', 'Entire Graph', delta_precison])
        result_lines.append([str(delta)+'_recall', 'Entire Graph', delta_recall])
#        result_lines.append([str(delta)+'_composite', 'Entire Graph', delta_composite])
    
    if 1:
        match_block_ratio=match_ratio(s1,s2)
        sample_list = [1]*len(match_block_ratio)
        block_match_ave=np.array(match_block_ratio)-np.asarray(sample_list)*sample          
        abs_difference = np.array(map(abs, list(block_match_ave)))
        sum_all=0
        for i in range(len(block_match_ave)-1):
            if block_match_ave[i]<0:
                sum_all = sum_all+abs_difference[i]/sample;
            else:
                sum_all = sum_all+abs_difference[i]/match_block_ratio[i];
        NLS=1-sum_all/len(match_block_ratio) 
        print("NLS:",NLS)
        result_lines.append(['NLS', 'Entire Graph', NLS])  
        if 0:
            delta_rank_match_plot(match_block_ratio,clustering_current) 

#calculate NLS divied by p                  
#        aver_difference=abs_difference/sample
#        NLS=1-aver_difference.sum()/len(match_block_ratio)
#        print("NLS:",NLS)
            
#calculate ASE            
#        block_match_sum=np.square(block_match_ave)
#        ase= block_match_sum.sum()/len(match_block_ratio)
#        print("ASE:",ase)
            
#calculate real precision recall               
#    precision = len(res1) * 1.0 / sample_block_num
#    recall = len(res1) * 1.0 / original_block_num
#    print ('Precision: ' + str(precision))
#    print ('Recall: ' + str(recall))
#    result_lines.append(['Precison', 'Entire Graph', precision])
#    result_lines.append(['Recall', 'Entire Graph', recall])          

    print ('block_size_median: ' + str(block_size_median))
    result_lines.append(['Block_size_median', 'Entire Graph', block_size_median])
    result_lines.append(['Sample_block_num', 'Entire Graph', sample_block_num])
    result_lines.append(['Original_block_num', 'Entire Graph', original_block_num])
    
#    print('difference is:'+ str(abs(original_block_num-sample_block_num)))
#    print('max is:'+ str(max(original_block_num-sample_block_num)))
    print ('sample_block_num: ' + str(sample_block_num))
    print ('original_block_num: ' + str(original_block_num))
    ANC=1.0-(abs(original_block_num-sample_block_num)*1.0/max(original_block_num,sample_block_num))
    print ('ANC: ' + str(ANC))
    result_lines.append(['ANC', 'Entire Graph', ANC])   
 
    return result_lines
    
def Compare3_no_nls(s1, s2, deltas, sample, clustering_current):
    result_lines = []
    precision = 0.0
    recall = 0.0

    sample_block_num= 0
    original_block_num = 0
    block_size=[]
    block_size_median=0
    
    for kk1, vv1 in s1.items():
        if len(vv1)>2:
            original_block_num=original_block_num+1
            
    
    for kk2, vv2 in s2.items():
        if len(vv2)>2:
            sample_block_num=sample_block_num+1
            block_size.append(len(vv2))
    block_size_median = np.median(block_size)

    for delta in deltas:
        res1 = set()       
        res2 = set()
        res3 = set()
        res_orig=list()
        res_samp=list()
        res2.clear()
        res1.clear()
        c1={}
        c2={}
        c1=copy.deepcopy(s1)
        c2=copy.deepcopy(s2)
#        print('c1 length is %d\n' %len(c1))
#        print('c2 length is %d\n' %len(c2))
#        time.sleep(5)

#        delta-coverage(pi(S)) for precision       
        for k2, v2 in c2.items():
            max_match_orig= 0#for each sample block, initiate the max_mathch=0
            match_orig_block=set()
            for k1, v1 in c1.items():
                if len(v2)>2 and len(v1)>2: 
#                    if Coverage(v1, v2):
#                        res1.add(k1)
#                    if DeltaCoverage(v1, v2, float(delta), sample):
#                        res2.add(k1)
#                        res3.add(k2)
                        #c1.pop(k1)
#                    if DeltaCoverage_sep(v1, v2, float(delta), sample)==1:
#                        res2.add(k1)# original, because of sampling, mapbe it is too low.
#                        res3.add(k2)# sampling 
#                    elif DeltaCoverage_sep(v1, v2, float(delta), sample)==2:
#                        res3.add(k2)
#                    else:
#                        continue                    
                    if DeltaCoverage_weighted(v1, v2, float(delta), sample):
                        intection_set_len = len(v1 & v2)                        
                        if intection_set_len > max_match_orig:
                            max_match_orig = intection_set_len
                            match_orig_block=v1
                        else:
                        
#                            print('no lager match')
#                            print(intection_set_len)
                            continue
                else:
#                    print('less than 3 clusters.')
#                    print("sample set")
#                    print(list(v2))
                    continue                                                                                
            res_samp.append((len(match_orig_block & v2) * 1.0)/len(v2))#sample
            
#        delta-coverage(pi(G)) for recall.  
        for k1, v1 in c1.items():
            max_match_sample= 0#for each sample block, initiate the max_mathch=0
            match_sample_block=set()
            for k2, v2 in c2.items():
                if len(v2)>2 and len(v1)>2:                  
                    if DeltaCoverage_weighted(v1, v2, float(delta), sample):
                        intection_set_len = len(v1 & v2)                        
                        if intection_set_len > max_match_sample:
                            max_match_sample = intection_set_len
                            match_sample_block=v2
                        else:
#                            print('no lager match')
                            continue
                else:
#                    print('less than 3 clusters.')
                    continue                                                                                
            res_orig.append((len(match_sample_block & v1) * 1.0)/len(v1))#original

#        np.array(res_samp).mean()
        if delta == deltas[-1]:
            match_block_ratio=match_ratio(c1,c2)
            delta_rank_match_plot(match_block_ratio,clustering_current)
        
        sum_weight_coverage_S = sum(res_samp)
        sum_weight_coverage_G = sum(res_orig)
        delta_precison = sum_weight_coverage_S * 1.0 / sample_block_num
        delta_recall = sum_weight_coverage_G * 1.0 / original_block_num        
#        delta_precison = len(res3) * 1.0 / sample_block_num
#        delta_recall = len(res2) * 1.0 / original_block_num
        
        if delta_precison+delta_recall !=0:
            delta_composite = 2.0*delta_precison*delta_recall* 1.0 / (delta_precison+delta_recall)
        else:
            delta_composite = 0
        
        print (len(res2), len(res3))
        print ('---------------------------------')
  
        print ('Delta Precision with delta (' + str(delta) + '): ' + str(delta_precison))
        print ('Delta Recall with delta (' + str(delta) + '): ' + str(delta_recall)) 
        print ('Delta F-measure with delta (' + str(delta) + '): ' + str(delta_composite)) 
        result_lines.append([str(delta)+'_precison', 'Entire Graph', delta_precison])
        result_lines.append([str(delta)+'_recall', 'Entire Graph', delta_recall])
        result_lines.append([str(delta)+'_composite', 'Entire Graph', delta_composite])
    
#    precision = len(res1) * 1.0 / sample_block_num
#    recall = len(res1) * 1.0 / original_block_num
#    print ('Precision: ' + str(precision))
#    print ('Recall: ' + str(recall))
#    result_lines.append(['Precison', 'Entire Graph', precision])
#    result_lines.append(['Recall', 'Entire Graph', recall])
    
    ANC=1.0-(abs(original_block_num-sample_block_num)/max(original_block_num,sample_block_num))
    print ('ANC: ' + str(ANC))
    result_lines.append(['ANC', 'Entire Graph', ANC])  

    print ('block_size_median: ' + str(block_size_median))
    print ('sample_block_num: ' + str(sample_block_num))
    print ('original_block_num: ' + str(original_block_num))
    result_lines.append(['Block_size_median', 'Entire Graph', block_size_median])
    result_lines.append(['Sample_block_num', 'Entire Graph', sample_block_num])
    result_lines.append(['Original_block_num', 'Entire Graph', original_block_num])
    return result_lines
    
def sort(a):
    for k in range(len(a)):
        (a[k][0],a[k][1]) = (a[k][1],a[k][0])
    a.sort()
    for k in range(len(a)):
        (a[k][0],a[k][1]) = (a[k][1],a[k][0]) 


if __name__ == '__main__':
    ground = ReadInData('community.dat')
    partition = ReadInData('network_metisResult')
    #partition = ReadInData('network500/network_StructuralSamplerResult')
    print(len(ground), len(partition))
    deltas=[0.5,0.6,0.7,0.8,0.9,1.0]
    sample=1.0;
    current_dir=os.getcwd()
#    Compare3(ground, partition,deltas,sample, current_dir)
    
   
'''    
#     a = [[1,2,4],[6,5,6],[2,5,9]]
#     sort(a)
#     print(a)
    
#     x = np.array([[1,2,4],[6,5,6],[2,5,9]])
#    x[np.argsort(x)]
#    print x
    comm = np.loadtxt('community.dat',dtype='int32') 
    myresult = np.loadtxt('network_metisResult',dtype='int32')
    myresult_sorted= np.array( sorted(myresult, key=lambda myresult : myresult[0]))
    myresult_sampled= np.array(myresult_sorted[:,0])
    myresult_label= np.array(myresult_sorted[:,1])
    print (len(myresult))
#comm_sorted =np.array( sorted(comm, key=lambda comm : comm[0]))
    
    comm_sorted =np.array( sorted(comm, key=lambda myresult_sorted : myresult_sorted[0]))
    a= myresult[:,0]
    b=comm_sorted[myresult[:,0],:]
    
    comm_selected= np.array(comm_sorted[myresult[:,0],:])
    
    truelabel_whole= np.array(comm_sorted[:,0])

    truelabel= np.array(comm_selected[:,1])
    print (len(truelabel))
    print (purity_score(myresult_label, truelabel))
    
    print (normalized_mutual_info_score([0, 0, 0, 0], [0, 1, 2, 3]))
    

    print ("resut is ",normalized_mutual_info_score(truelabel.tolist(), myresult_label.tolist()))
# 
#     
#     clus = np.array([1, 4, 4, 4, 4, 4, 3, 3, 2, 2, 3, 1, 1])
#     clas = np.array([5, 1, 2, 2, 2, 3, 3, 3, 1, 1, 1, 5, 2])
#     print purity_score(clus, clas)
    '''     
    
    
    