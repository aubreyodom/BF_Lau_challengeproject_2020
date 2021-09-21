import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import sys
import os
from xlwt import Workbook

def update_name(excelFile):
    for i in range(len(excelFile)):
        if excelFile[i] == '.':
            return excelFile[:i] + "Ranked_Curves.xls"

    return excelFile + "Ranked_Curves.xls"

def normalize(filename):
    def removeData(data, thresh):
        x, y = data.shape
        for i in range(1, x):
            #print(data[i, 0])
            #print(filename)
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

def condenseCurves(dictionary, excelName):
    wb = Workbook()
    sheet = wb.add_sheet('Sheet 1')
    for i in range(178):
        sheet.write(i+1, 0, i)
    sheet.write(0, 0, 'X Position')

    counter = 1
    for d in dictionary.keys():
        for filename in dictionary[d]:
            sheet.write(0, counter, filename)
            df = normalize(d+filename)
            for i in range(df.shape[0]):
                sheet.write(i+1, counter, df[i, 1])
            counter += 1

    wb.save(excelName)

def update_plot(allLines, groupNum, y):
    #for i in range(0, len(allLines) - 1):
        #print(i)
    #    newy = allLines[i+1][groupNum-1].get_ydata()
    #    print(i+1, groupNum - 1)
    #    print(newy)
    #    allLines[i][groupNum-1].set_ydata(newy)

    allLines[groupNum-1].set_ydata(y)

def ezRank(filename):
    newExcel = update_name(filename)
    wb = Workbook()
    sheet = wb.add_sheet('Sheet 1')
    for i in range(178):
        sheet.write(i+1, 0, i)
    sheet.write(0, 0, 'X Position')

    fig1, ax1 = plt.subplots(4, 2)
    x = [i for i in range(178)]
    y = [0 for _ in range(178)]

    #temp = [0 for i in range(1)]
    allLines = [0 for _ in range(8)]
    #print(allLines)

    ax1 = ax1.flatten()
    #for j in range(ax1.shape[1]):
    for i in range(ax1.shape[0]):
        ax1[i].set_xticks([])
        ax1[i].set_yticks([])
        ax1[i].axis('off')
        if i < 8:
            ax1[i].set_title('Group ' + str(i+1))
        ax1[i].set_xlim([0, 178])
        ax1[i].set_ylim([-4, 4])
        line1, = ax1[i].plot(x, y)
        allLines[i] = line1
    #print(allLines[0])
    try:
        df = pd.read_excel(filename)
    except:
        df = pd.read_csv(filename, sep='\t')
    dfNames = list(df.columns)
    #plt.show(block=False)

    #fig2, ax2 = plt.subplots()
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)

    x = df.iloc[:, 0]
    line2, = ax2.plot(x, df.iloc[:, 1])
    ax2.set_ylim([-4, 4])
    #print(type(line2))
    for col in range(1, df.shape[1] - 1):
        sheet.write(0, col, dfNames[col])
        plt.show(block=False)
        while True:
            try:
                groupNum = int(input("Enter a group number for this curve: "))
            except:
                print('Invalid input')
                continue
            if groupNum > 0 and groupNum < 9:
                break
            print('Invalid input')

        line2.set_ydata(df.iloc[:, col+1])
        fig2.canvas.draw()
        #plt.close()

        update_plot(allLines, groupNum, df.iloc[:, col])
        fig1.canvas.draw()

        for i in range(df.shape[0]):
            #print(i, col)
            sheet.write(i+1, col, df.iloc[i, col])
        sheet.write(179, col, groupNum)
        #plt.show(block=False)
    wb.save(newExcel)
    #for col in range(df.shape[1]):

def main():
    excelFile = sys.argv[1]
    if not excelFile.endswith(".xlsx") and not excelFile.endswith(".xls"):
        excelFile += '.xls'

    directories = list(sys.argv[2:])
    d = dict()

    for directory in directories:
        d[directory] = []
        for filename in os.listdir(directory):
            if filename.endswith(".xlsx") or filename.endswith(".xls"):
                d[directory].append(filename)

    condenseCurves(d, excelFile)
    ezRank(excelFile)

    sys.exit(1)

if __name__ == "__main__":
    main()
