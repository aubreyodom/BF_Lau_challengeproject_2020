import pandas as pd
from scipy.signal import savgol_filter, argrelextrema, find_peaks
import numpy as np
from matplotlib import pyplot as plt
import statistics as st
from scipy import stats
import sys
import os
from xlwt import Workbook

def removeData(data, thresh):
    x, y = data.shape
    for i in range(x):
        if int(data[i, 0]) >= thresh:
            filter = i
            break
    data = data[filter:, :]
    return data

def findTruePeaks(x, y):
    vals = [1 for i in range(len(x))]
    realy = []
    for i in x:
        realy.append(y[i])

    for i in range(1, len(x)):
        for j in range(len(realy[0:i]) - 1, -1, -1):
            if realy[i] > realy[j]:
                vals[j] = 0

    newPeaks = []
    for i in range(len(vals)):
        if vals[i] == 1:
            newPeaks.append(x[i])
    return newPeaks

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
    return n, m

def returnTitle(filename):
    for i in range(len(filename)):
        if filename[i] == '.':
            return filename[0:i]

def findBestPeaks(l):
    #print(l)
    l = [l]
    while True:
        newL = []
        for j in l:
            for i in range(len(j)):
                newL.append(j[0:i] + j[i+1:])
        l = newL[:]
        if len(l[0]) == 6:
            break

    low = np.inf
    lowL = []
    for i in l:
        diff = [i[j] - i[j-1] for j in range(1, len(i))]
        diffStd = np.std(diff)
        if diffStd < low:
            low = diffStd
            lowL = i[:]
    #print(lowL)
    return lowL

def peaksMin(num):
    a = 6/num
    b = num/6
    if a < b:
        return a
    else:
        return b

def classify(filenames, directory):
    def mean(l):
        return sum(l)/len(l)
    if directory[-1] != '/':
        directory += '/'

    '''
    wb = Workbook()
    sheet = wb.add_sheet('Sheet 1')
    sheet.write(0, 0, 'Filename')
    sheet.write(0, 1, 'Ratio of Peaks Found')
    sheet.write(0, 2, 'Ratio of Peaks to Ideal')
    sheet.write(0, 3, 'Ratio of Range')
    sheet.write(0, 4, 'Inverse Standard Deviation')
    '''
    n, m = dimensions(len(filenames))
    fig, axs = plt.subplots(n, m)
    axs = axs.flatten()
    fig.tight_layout(pad=1.5)

    allScores = []
    #allPeaks = []
    allNewPeaks = []
    for i, filename in zip(range(len(filenames)), filenames):
        print(filename)
        #sheet.write(i+1, 0, filename)

        try:
            df = pd.read_excel(directory+filename)
        except:
            df = pd.read_csv(directory+filename, sep='\t')
            #print(df)
        #print(df)
        df = df.to_numpy()
        df = removeData(df, 20)
        #df = df[0:198, :]

        yhat = savgol_filter(df[:, 1], 31, 6)
        smoothError = 0
        for j in range(len(yhat)):
            smoothError += abs(yhat[i] - df[j, 1])
        smoothError /= len(yhat)
        smoothError = smoothError**-1
        #yhat = df[:, 1]
        #yhat = savgol_filter(df[:, 1], 21, 6)
        #yhat = savgol_filter(yhat, 21, 6)

        peaks, _ = find_peaks(yhat)
        #peaks, _ = find_peaks(df[:, 1])
        #print(peaks)
        peaks += 20
        diff = []
        if peaks[0] == 1:
            peaks = peaks[1:]
        #allPeaks.append(peaks)

        y = np.concatenate([np.zeros(20), yhat])
        newPeaks = findTruePeaks(peaks, y)
        if len(newPeaks) > 6:
            newPeaks = findBestPeaks(newPeaks)
        #newPeaks = newPeaks[0:6]
        allNewPeaks.append(newPeaks)
        diff = [newPeaks[i] - newPeaks[i - 1] for i in range(1, len(newPeaks))]

        '''
        sheet.write(i+1, 1, len(newPeaks)/len(peaks))
        sheet.write(i+1, 2, len(newPeaks)/6)
        sheet.write(i+1, 3, ((newPeaks[-1] - newPeaks[0])/180))
        sheet.write(i+1, 4, (1/np.std(diff)))
        wb.save('Correlation.xls')
        '''
        #p, q, r, s, t = 997/997, 925/997, 538/997, 697/997, 500/997
        #p, q, r, s = 1, 1, 1, 1
        p, q, r, s, t = 909/945, 945/945, 416/945, 889/945, 500/997
        if peaksMin(len(newPeaks)) < 0.5 or ((newPeaks[-1] - newPeaks[0])/180) < 0.85 or (1/np.std(diff)) < 0.981 or (len(newPeaks)/len(peaks)) < 0.462:
            score = -1
        else:
            #score = (len(newPeaks)/len(peaks))**p * (peaksMin(len(newPeaks))**q) * (((newPeaks[-1] - newPeaks[0])/180)**r) * (1/np.std(diff))**s #* smoothError**t
            #score = round(score, 4)
            score = 1

        if score == np.inf:
            score = round(0, 4)

        allScores.append(score)

    order = [str(i) for i in range(len(filenames))]
    allScores, order = (list(t) for t in zip(*sorted(zip(allScores, order))))

    filenames = [filenames[int(i)] for i in order]
    allNewPeaks = [allNewPeaks[int(i)] for i in order]

    filenames = filenames[::-1]
    allScores = allScores[::-1]
    allNewPeaks = allNewPeaks[::-1]

    for filename, row, score, newPeaks in zip(filenames, axs, allScores, allNewPeaks):
        try:
            df = pd.read_excel(directory+filename)
        except:
            df = pd.read_csv(directory+filename, sep='\t')
        df = df.to_numpy()
        df = removeData(df, 20)
        df = df[0:180, :]

        yhat = savgol_filter(df[:, 1], 31, 6)
        #yhat = savgol_filter(yhat, 21, 6)
        y = np.concatenate([np.zeros(20), yhat])

        row.plot(df[:, 0], df[:, 1], c = 'b')
        #row.plot(df[:, 0], yhat, c = 'r')
        #row.plot(newPeaks, [y[i] for i in newPeaks], 'x', c = 'g')
        row.text(1 - 0.0278*len(returnTitle(filename)), 0.75, returnTitle(filename), transform = row.transAxes, fontsize=8)#returnTitle(filename)+ ': ' + str(score))
        #print(filename)
        row.axis('off')
        row.text(0.875, 0.375, str(score), transform=row.transAxes, fontsize = 8)
        #row.text(0.75, 0.65, '-------', transform=row.transAxes)
        #row.set_title(returnTitle(filename))
        row.set_xticks([])
        row.set_yticks([])
    plt.show()
    return filenames, allScores


def write(filenames, scores, output):
    def changeName(filename):
        for i in range(len(filename) - 1, -1, -1):
            if filename[i] == '.':
                return filename[0:i]

    if output[-4:] != '.xls' and output[-5:] != '.xlsx':
        output += '.xls'

    wb = Workbook()
    sheet = wb.add_sheet('Sheet1')
    sheet.write(0, 0, 'Filenames')
    sheet.write(0, 1, 'Scores')

    for i in range(len(filenames)):
        sheet.write(i+1, 0, changeName(filenames[i]))
        sheet.write(i+1, 1, scores[i])

    wb.save(output)

def main():
    directory = sys.argv[1]
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            filenames.append(filename)

    filenames, scores = classify(filenames, directory)
    try:
        output = sys.argv[2]
    except IndexError:
        sys.exit(1)

    write(filenames, scores, output)
    sys.exit(1)

if __name__ == "__main__":
    main()
