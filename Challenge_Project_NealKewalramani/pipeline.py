import pandas as pd
import os
import shutil
import getFeatures as gf
import numpy as np
from sklearn import metrics
import scipy
from matplotlib import pyplot as plt
from xlwt import Workbook
import sys

def get_all_files(directories):
    filenames = []
    for directory in directories:
        for filename in os.listdir(directory):
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                filenames.append(directory+filename)
    return filenames

def get_stats(featureFile):
    df = pd.read_excel(featureFile)
    return df.mean(axis = 0), df.std(axis = 0)

def file_2_rank(excelName):
    file2rank = dict()
    try:
        df = pd.read_excel(excelName)
    except:
        df = pd.read_csv(excelName, sep='\t')

    for i in range(df.shape[0]):
        file2rank[df.loc[i, 'Filename']] = df.loc[i, 'Rank']

    return file2rank

def file_2_feature_train(filenames, file2rank):
    file2feature = dict()
    for filename in filenames:
        assert filename in file2rank.keys(), filename + ' not in ranking excel file'

        l = list(gf.classify(filename, ''))
        l.append(file2rank[filename])
        file2feature[filename] = l

    return file2feature

def file_2_feature_test(filenames):
    file2feature = dict()
    for filename in filenames:
        l = list(gf.classify(filename, ''))
        file2feature[filename] = l

    return file2feature

def distance(sample, cluster):
    dist = 0
    for i in range(len(sample)):
        dist += (cluster[i] - sample[i])**2
    return dist**(1/2)

def find_closest_cluster(df, clusters):
    file2cluster = dict()

    def find_min(vals):
        minIndex = None
        minVal = np.inf
        for i in range(len(vals)):
            #print(val[i])
            if vals[i] < minVal:
                minIndex = i
                minVal = vals[i]
        return minIndex+1

    for i in range(df.shape[0]):
        allDist = []
        for j in range(clusters.shape[0]):
            dist = distance(df.iloc[i, :], clusters[j, :])
            allDist.append(dist)

        file2cluster[list(df.index)[i]] = find_min(allDist)
    return file2cluster

def rank(directories, clusterFilename, cluster2group):
    allFilenames = get_all_files(directories)
    means, stds = get_stats('Train_07192020.xls')
    file2features = file_2_feature_test(allFilenames)
    #df = pd.read_excel(featureFile)
    clusters = np.loadtxt(clusterFilename)

    columns = ['Ratio of Peaks Found', 'Ratio of Peaks to Ideal', 'Ratio of Range', 'Inverse Standard Deviation', 'Area Under the Curve', 'Normed Area Under the Curve', 'Smoothing Error']

    df = pd.DataFrame(list(file2features.values()), columns = columns, index = file2features.keys())
    for column in columns:
        df.loc[:, column] = (df.loc[:, column] - means[column])/stds[column]
    #print(df)
    file2cluster = find_closest_cluster(df, clusters)
    file2group = dict()
    for filename in file2cluster.keys():
        for key in cluster2group.keys():
            if file2cluster[filename] in key:
                file2group[filename] = cluster2group[key]
                break

    return file2group

def get_wilcoxon(testRanks, realRanks):
    def remove_directory(filename):
        for i in range(len(filename)):
            if filename[i] == '/':
                return filename[i+1:]

    df = pd.read_excel('TrainRanked.xls')
    rankedDict = dict()
    for i in range(df.shape[0]):
        rankedDict[df.loc[i, 'name']] = df.loc[i, 'rank']

    for key in rankedDict.keys():
        for pair in realRanks.keys():
            if rankedDict[key] >= pair[0] and rankedDict[key] <= pair[1]:
                rankedDict[key] = realRanks[pair]
                break

    testList = []
    realList = []
    for f1 in testRanks.keys():
        testList.append(testRanks[f1])
        realList.append(rankedDict[remove_directory(f1)])

    print(testList)
    print(realList)
    return scipy.stats.wilcoxon(testList, realList)

def main():
    cluster2group = dict()
    cluster2group[(6, 7)] = 1
    cluster2group[(4, 1)] = 4
    cluster2group[(2, 8)] = 3
    cluster2group[(3, 5)] = 2

    directories = sys.argv[1:-1]
    test = rank(directories, 'ClusterValues.txt', cluster2group)
    wb = Workbook()
    sheet = wb.add_sheet('Sheet 1')
    sheet.write(0, 0, 'Filenames')
    sheet.write(0, 1, 'Rank')
    counter = 1
    for filename in test.keys():
        sheet.write(counter, 0, filename)
        sheet.write(counter, 1, test[filename])
        counter += 1
    wb.save(sys.argv[-1])

    sys.exit(1)

if __name__ == "__main__":
    main()
