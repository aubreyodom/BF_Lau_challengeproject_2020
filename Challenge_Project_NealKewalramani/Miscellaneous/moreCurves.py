import pandas as pd
import numpy as np
import sys
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter

def normalize(filename):
    def removeData(data, thresh):
        x, y = data.shape
        for i in range(x):
            if int(data[i, 0]) >= thresh:
                filter = i
                break
        data = data[filter:398, :]
        return data

    try:
        df = pd.read_excel(filename)
    except:
        df = pd.read_csv(filename, sep='\t')

    df = df.to_numpy()
    df = removeData(df, 20)
    df[:, 1] = np.divide(np.subtract(df[:, 1], np.mean(df[:, 1])), np.std(df[:, 1]))
    return df

def gaussianNoise(filename, axs):
    #allGaus = [0.10, 0.20, 0.30]
    #fig, axs = plt.subplots(4, 2)
    #axs = axs.flatten()

    df = normalize(filename)
    #for sigma in allGaus:
    randVals = np.random.normal(0, .15, (df.shape[0], 1))
    temp = randVals + df[:, [1]]
    axs[0].plot(df[:, 0], temp)
    #plt.show()

def smooth(filename, axs):
    #filters = [4, 5, 6]
    #for filter in filters:
    df = normalize(filename)
    yhat = savgol_filter(df[:, 1], 9, 6)
    axs[1].plot(df[:, 0], yhat)

def graph(filename, axs):
    df = normalize(filename)
    axs[2].plot(df[:, 0], df[:, 1])

def main():
    '''
    directory = sys.argv[1]
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            filenames.append(filename)
    '''
    filename = sys.argv[1]
    fig, axs = plt.subplots(3, 1)
    axs = axs.flatten()
    gaussianNoise(filename, axs)
    smooth(filename, axs)
    graph(filename, axs)
    plt.show()
    sys.exit(1)

if __name__ == "__main__":
    main()
