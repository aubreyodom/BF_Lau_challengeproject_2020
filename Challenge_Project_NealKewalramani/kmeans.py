import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import sys
from kneed import KneeLocator
from xlwt import Workbook


def removeData(data, thresh):
    x, y = data.shape
    for i in range(1, x):
        if int(data[i, 0]) >= thresh:
            return data[i:398, :]

def dimensions(num):
    n, m = 1, 1

    while n * m != num:
        if n * m < num:
            n += 1
            m += 1
        elif n * m > num:
            m -= 1

    if (n == 1 or m == 1) and num > 4:
        num += 1
        return dimensions(num)

    if (n == 2 or m ==2) and num > 8:
        num += 1
        return dimensions(num)
    return n, m

def get_directory(filename):
    for i in range(len(filename)):
        if filename[i] == '_':
            if filename[0:i] == 'AaAeg':
                return 'AeAeg2/'
            else:
                return filename[0:i] +  '2/'

def round_all(array):
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            array[i, j] = round(array[i, j], 2)
    return array

def graphCluster(numClusters, d, data):
    colors = ['red', 'blue', 'orange', 'green', 'black']
    colorCounter = 0
    colorDict = dict()
    #data = pd.read_excel(file)
    d = round_all(d)
    for j in range(numClusters):
        df = pd.read_excel('Clusters.xls')
        df = df.iloc[:, j]
        df = df.dropna()

        n, m = dimensions(df.shape[0])

        fig, axs = plt.subplots(n, m)
        fig.suptitle(d[j, :])
        axs = axs.flatten()
        print("Cluster" + str(j))
        for i, ax in zip(range(df.shape[0]), axs):
            filename = df.iloc[i]
            directory = get_directory(filename)
            if directory not in colorDict.keys():
                colorDict[directory] = colors[colorCounter]
                colorCounter += 1
            print(str(i) + ": " + filename)

            try:
                graph = pd.read_excel(directory+filename)
            except:
                graph = pd.read_csv(directory+filename, sep='\t')

            graph = graph.to_numpy()
            graph = removeData(graph, 20)

            ax.plot(graph[:, 0], graph[:, 1])#, color = colorDict[directory])
            ax.axis('off')
            ax.set_xticks([])
            ax.set_yticks([])
            """
            for k in range(data.shape[0]):
                if data.loc[k, 'Filename'] == filename:
                    dataString = ''
                    for l in range(1, data.shape[1]):
                        dataString += str(round(data.iloc[k, l], 2)) + ', '
                    dataString = dataString[:-2]
                    break
            ax.text(0, 1, dataString, transform=ax.transAxes, fontsize = 6)
            """
            #ax.text(0.875, 0.375, round(d[j][i], 3), transform=ax.transAxes, fontsize = 8)
        plt.show(block=False)

    for key in colorDict.keys():
        print(key, colorDict[key])
    x = input()

def distance(one, two):
    dist = 0
    for i in range(len(one)):
        dist += (two[i] - one[i])**2
    return dist**(1/2)

def k_means(filename, num):
    df = pd.read_excel(filename)
    df.iloc[:, 1:] = (df.iloc[:, 1:]-df.iloc[:, 1:].mean())/df.iloc[:, 1:].std()
    #print(df)
    #for i in range(1, df.shape[1]):
    #    df.iloc[:, i] = (df.iloc[:, 1] - df.iloc[:, i].mean())/df.iloc[:, i].std()

    #for i in range(1, df.shape[1]):
    #    print(i, df.iloc[:, i].mean(), df.iloc[:, i].std(ddof=0))
    errors = []
    max = 31
    target = 5
    for cluster in range(1, max):
        kMeans = KMeans(init='random', n_clusters = cluster, n_init = 30, max_iter = 500000)
        kMeans.fit(df.iloc[:, 1:])
        errors.append(kMeans.inertia_)
        #print('Finished ' + str(cluster))


    k1 = KneeLocator(range(1, max), errors, curve='convex', direction='decreasing')
    print(k1.elbow)

    #plt.scatter([i for i in range(1, max)], errors)
    #plt.xlabel('Number of Clusters')
    #plt.ylabel('SSE')
    #plt.show()
    kMeans = KMeans(init='random', n_clusters = num, n_init = 30, max_iter = 5000000)
    #print(df)
    kMeans.fit(df.iloc[:, 1:])
    #print(kMeans.cluster_centers_)
    allClusters = dict()
    d = dict()
    distDict = dict()
    for k in range(kMeans.cluster_centers_.shape[0]):
        #allClusters = kMeans.cluster_centers_[k, :]
        d[k] = []
        distDict[k] = []

    for i in range(df.shape[0]):
        dist = np.inf
        cluster = None

        for j in range(kMeans.cluster_centers_.shape[0]):
            currentDist = distance(df.iloc[i, 1:], kMeans.cluster_centers_[j, :])
            if currentDist < dist:
                dist = currentDist
                cluster = j

        d[cluster].append(df.iloc[i, 0])
        distDict[cluster].append(dist)

    wb = Workbook()
    sheet = wb.add_sheet('Sheet 1')

    clusterLowest = None
    lowest = np.inf

    colCounter = 0
    for key in d.keys():
        if len(d[key]) < lowest:
            lowest = len(d[key])
            clusterLowest = key

        print(len(d[key]))
        rowCounter = 1
        sheet.write(0, colCounter, colCounter)
        for filename in d[key]:
            sheet.write(rowCounter, colCounter, filename)
            rowCounter += 1
        colCounter += 1

    wb.save('Clusters.xls')
    np.savetxt('NewClusterValues.txt', kMeans.cluster_centers_)
    return kMeans.cluster_centers_, df


    #plt.xlabel('Number of Clusters')
    #plt.ylabel('SSE')
    #plt.show()


def main():
    numCluster = 8
    filename = sys.argv[1]
    k, data = k_means(filename, numCluster)
    graphCluster(numCluster, k, data)
    sys.exit(1)

if __name__ == "__main__":
    main()
