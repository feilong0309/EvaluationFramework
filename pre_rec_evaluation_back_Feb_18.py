'''
Created on 25 Nov 2015

@author: Administrator
'''
'''
Created on 24 Nov 2015

@author: Administrator
'''
import numpy as np
from sklearn.metrics.cluster import normalized_mutual_info_score
import copy
import time

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

def DeltaCoverage(s1, s2, threshold, sample):
#    delta = len(s1 & s2) * 1.0 / len(s2 | s1)
#    print("intersection of two set is %d" % (len(s1 & s2)))
#    print("union of two set is %d" % (len(s1 | s2)))

    delta = len(s1 & s2) * 1.0 / len(s2)
    delta2 = len(s1 & s2) * 1.0 / (len(s1) * sample)
     
#    if delta>= threshold and delta<= 2-threshold:
#        return True
#    elif delta2>= threshold and delta2<= 2-threshold:
#        return True        
#    else:
#        return False
        
#    if delta>= threshold and delta<= 2-threshold and delta2>= threshold and delta2<= 2-threshold:
#    if delta>= threshold and delta2>= threshold:
    if delta>= threshold and delta2>= 0.5:
        
#        print("\n\n\nnew original set:delta=%0.2f, delta2=%0.2f\n"%(delta, delta2))
#        print(list(s1))
#        print("sample set \n")
#        print(list(s2))   
#        time.sleep(5)
        return True

    else:
        return False
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
                if len(v2)>3: 
                    if Coverage(v1, v2):
                        res1.add(k1)
                    if DeltaCoverage(v1, v2, float(delta), sample):
                        res2.add(k1)
                        c1.pop(k1)
#                        c2.pop(k2)

        delta_precison = len(res2) * 1.0 / sample_block_num
        delta_recall = len(res2) * 1.0 / original_block_num
        delta_composite = 2.0*delta_precison*delta_recall* 1.0 / (delta_precison+delta_recall)
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
        
def Compare3(s1, s2, deltas, sample):
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
                if len(v2)>3: 
                    if Coverage(v1, v2):
                        res1.add(k1)
                    if DeltaCoverage(v1, v2, float(delta), sample):
                        res2.add(k1)
                        c1.pop(k1)
#                        c2.pop(k2)

        delta_precison = len(res2) * 1.0 / sample_block_num
        delta_recall = len(res2) * 1.0 / original_block_num
#        delta_composite = 2.0*delta_precison*delta_recall* 1.0 / (delta_precison+delta_recall)
        print (len(res1), len(res2))
        print ('---------------------------------')
        print ('Delta Precision with delta (' + str(delta) + '): ' + str(delta_precison))
        print ('Delta Recall with delta (' + str(delta) + '): ' + str(delta_recall))
#        print ('Delta F-measure with delta (' + str(delta) + '): ' + str(delta_composite))      
        result_lines.append([str(delta)+'_precison', 'Entire Graph', delta_precison])
        result_lines.append([str(delta)+'_recall', 'Entire Graph', delta_recall])
#        result_lines.append([str(delta)+'_composite', 'Entire Graph', delta_composite])
    
    precision = len(res1) * 1.0 / sample_block_num
    recall = len(res1) * 1.0 / original_block_num
    print ('Precision: ' + str(precision))
    print ('Recall: ' + str(recall))
    result_lines.append(['Precison', 'Entire Graph', precision])
    result_lines.append(['Recall', 'Entire Graph', recall])
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

    Compare(ground, partition)
    
   
    
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
#     
    
    
    