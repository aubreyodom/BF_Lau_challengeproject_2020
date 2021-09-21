import pandas as pd
from xlwt import Workbook
from matplotlib import pyplot as plt
import os
import sys
import numpy as np

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
    if not excelName.endswith(".xlsx") and not excelName.endswith(".xls"):
        excelName += '.xls'

    wb = Workbook()
    sheet = wb.add_sheet('Sheet 1')
    for i in range(201):
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

def main():
    excelFile = sys.argv[1]
    directories = list(sys.argv[2:])
    d = dict()

    for directory in directories:
        d[directory] = []
        for filename in os.listdir(directory):
            if filename.endswith(".xlsx") or filename.endswith(".xls"):
                d[directory].append(filename)

    condenseCurves(d, excelFile)
    sys.exit(1)

if __name__ == "__main__":
    main()
