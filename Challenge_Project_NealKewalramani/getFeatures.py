import pandas as pd
from scipy.signal import savgol_filter, argrelextrema, find_peaks
from area_under_peaks_calculations import calc_aup
import numpy as np
from matplotlib import pyplot as plt
import statistics as st
from scipy import stats
import sys
import os
from xlwt import Workbook

def getFilename(string):
    filename = ''
    for i in string:
        if i == '/':
            filename = ''
        else:
            filename += i
    return filename

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

def findBestPeaks(l):
    #print(len(l))
    def mean(l):
        return sum(l)/len(l)

    def filterBest(l):
        def findExtreme(l, bool):
            if bool:
                maxIndex = None
                max = 0
                for i in range(len(l)):
                    if l[i] > max:
                        maxIndex = i
                        max = l[i]
                return maxIndex

            elif not bool:
                minIndex = None
                min = np.inf
                for i in range(len(l)):
                    if l[i] < min:
                        minIndex = i
                        min = l[i]
                return minIndex

        while len(l) > 11:
            #rint(len(l))
            diff = [l[j] - l[j-1] for j in range(1, len(l))]
            meanDiff = mean(diff)

            low, high = 0, 0
            for dist in diff:
                if dist < meanDiff:
                    low += 1
                else:
                    high += 1

            #print(low, high)
            #if low < high:
            index = findExtreme(l, False)
            if index == 0:
                del l[index]
            elif l[index - 1] > meanDiff:
                del l[index+1]
            elif l[index - 1] < meanDiff:
                del l[index]

            #else:
            #    return l
        return l

    if len(l) > 12:
        l = filterBest(l)

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

def classify(filename, directory, remove = True):
    """
    wb = Workbook()
    sheet = wb.add_sheet('Sheet 1')
    sheet.write(0, 0, 'Filename')
    sheet.write(0, 1, 'Ratio of Peaks Found')
    sheet.write(0, 2, 'Ratio of Peaks to Ideal')
    sheet.write(0, 3, 'Ratio of Range')
    sheet.write(0, 4, 'Inverse Standard Deviation')
    """
    #counter = 1

    #for directory in d.keys():
        #for i in range(len(d[directory])):
            #filename = d[directory][i]
    print(filename)
            #sheet.write(counter, 0, filename)

    try:
        df = pd.read_excel(directory+filename)
    except:
        df = pd.read_csv(directory+filename, sep='\t')

    df = df.to_numpy()
    if remove:
        df = removeData(df, 20)

    yhat = savgol_filter(df[:, 1], 31, 6)
            #smoothError = 0

    #1. Peak finding ratio
    peaks, _ = find_peaks(yhat)
    peaks += 20
    diff = []
    if peaks[0] == 1:
        peaks = peaks[1:]

    y = np.concatenate([np.zeros(20), yhat])
    newPeaks = findTruePeaks(peaks, y)
    if len(newPeaks) > 6:
        newPeaks = findBestPeaks(newPeaks)
                #print(newPeaks)

    ratio = len(newPeaks)/len(peaks)
            #sheet.write(counter, 1, ratio)

    #2. Ideal peaks
    ideal = peaksMin(len(newPeaks))
            #sheet.write(counter, 2, ideal)

    #3. Range of peaks
    ran = (newPeaks[-1] - newPeaks[0])/180
    #sheet.write(counter, 3, ran)

    #4. Standard deviation of peaks
    diff = [newPeaks[i] - newPeaks[i - 1] for i in range(1, len(newPeaks))]
    sd = np.std(diff)
            #sheet.write(counter, 4, sd)

    #5, 6, 7. Smooth Error
    area_under_peaks, aup_normed, smoothed_error = calc_aup(directory + filename)

            #counter += 1

    return ratio, ideal, ran, sd, area_under_peaks, aup_normed, smoothed_error

    outputFile1 = 'Train_07192020.xls'
    outputFile2 = 'Train_07192020_1.xls'
    wb.save(outputFile1)

    #6. Area under the curve
    data = pd.read_excel('area_under_peaks_printout (3).xlsx')
    df = pd.read_excel('Book1.xls')
    df['Area Under the Curve'] = pd.Series([1.3 for x in range(df.shape[0])])
    df['Normed Area Under the Curve'] = pd.Series([1.3 for x in range(df.shape[0])])

    for i in range(data.shape[0]):
        filename = getFilename(data.iloc[i, 1])
        for j in range(df.shape[0]):
            if filename == df.iloc[j, 0]:
                df.iloc[j, 6] = data.iloc[i, 2]
                df.iloc[j, 7] = data.iloc[i, 3]
    df.to_excel(outputFile2)








def main():
    d = dict()

    directories = list(sys.argv[1:])
    filenames = []
    for directory in directories:
        d[directory] = []
        for filename in os.listdir(directory):
            if filename.endswith(".xlsx") or filename.endswith(".xls"):
                d[directory].append(filename)

    classify(d)
    sys.exit(1)

if __name__ == "__main__":
    main()
