from scipy.fft import fft, ifft
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

def FourierTransform(filename):
    def removeData(data, thresh):
        x, y = data.shape
        for i in range(x):
            #print(data[i, 0])
            if int(data[i, 0]) >= thresh:
                #print('hello')
                filter = i
                break
        data = data[filter:, :]
        return data

    def findMax(x, y):
        max = 0
        for i in range(x.shape[0]):
            if y[i] > max:
                max = y[i]
                xMax = x[i]
        return 1/xMax

    df = pd.read_excel(filename)
    df = df.to_numpy()
    df = removeData(df, 20)

    x = df[:, 0]
    y = df[:, 1]
    N = len(x)
    yfft = fft(y)
    #plt.plot(x, np.abs(yfft))
    plt.plot(x[0:N//2], (2.0/N)*np.abs(yfft[0:N//2]))
    plt.show()
    return findMax(x[0:N//2], (2.0/N)*np.abs(yfft[0:N//2]))

filename1 = 'AeAlbo_Ovary_OA.24_35.trim.fastq.uq.polyn.5to5_SPECIES.xls.xlsx'
print(FourierTransform(filename1))
