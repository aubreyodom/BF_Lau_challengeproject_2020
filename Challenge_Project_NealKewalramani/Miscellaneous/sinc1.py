import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def transform(dic):
    def translate(tup):
        array = np.identity(3)
        array[0, 2] = tup[0]
        array[1, 2] = tup[1]
        return array

    def rotate(rad):
        array = np.identity(3)
        array[0, 0] = np.cos(rad)
        array[1, 1] = -np.cos(rad)
        array[0, 1] = -np.sin(rad)
        array[1, 0] = np.sin(rad)
        return array

    result = np.identity(3)
    for key in dic.keys():
        if key[0] == 't':
            result = np.matmul(result, translate(dic[key]))
        elif key[0] == 'r':
            result = np.matmul(result, rotate(dic[key]))
    return result

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

def adjustData(filename, dic):
    array = transform(dic)
    #print(array)
    #print(array)
    df = pd.read_excel(filename)
    df.insert(2, 'N/A', 0)
    df = df.to_numpy()
    df = removeData(df, 20)
    #print(df[0, :])

    x, y = df.shape
    #plt.plot(df[:, 0], df[:, 1])
    #plt.show()
    for i in range(x):
        temp = np.ones((3, 1))
        for j in range(2):
            temp[j, 0] = df[i, j]
        result = np.matmul(array, temp)
        #print(result)
        for j in range(3):
            df[i, j] = result[j, 0]
    #print(df[0, :])
    plt.plot(df[:, 0], df[:, 1])
    plt.show()

def sinc(x):
    if x == 0:
        return 1
    else:
        return np.sin(x)/(x**2)

def normalize(df):
    df = np.subtract(df, np.mean(df))
    df = np.divide(df, np.std(df))
    return df

def fit(df, alpha):
    x1, y = df.shape
    array = np.zeros((x1, 4))

    x, y = array.shape
    for i in range(x):
        #array[i, 0] = df[i, 0] * sinc(alpha * df[i, 0])
        array[i, 0] = sinc(alpha * df[i, 0])
        array[i, 1] = df[i, 0]**2
        array[i, 2] = df[i, 0]
        array[i, 3] = 1
    b = df[:, 1]
    #print(np.linalg.det(np.matmul(np.transpose(array), array)))
    ans = np.linalg.inv(np.matmul(np.transpose(array), array))
    ans = np.matmul(ans, np.transpose(array))
    ans = np.matmul(ans, b)
    #print(ans)
    error = np.linalg.norm(np.matmul(array, ans) - b)

    x = np.linspace(df[0, 0], df[x1-1, 0], 1000)
    y = []
    val = abs(ans[0]/(ans[1]+ans[2]))
    for i in x:
        y.append(ans[0]*sinc(alpha*i) + ans[1]*(i**2) + ans[2]*i + ans[3])# + (i**2)*sinc(alpha*i))
    return error, val

def returnTitle(string):
    for i in range(len(string)):
        if string[i] == '.':
            return string[0:i]

def multiFit(filenames, titles):
    def points(x, funcs):
        ans = [0]

        try:
            num = len(x) % funcs
            iterator = int(len(x)/funcs)
            for _ in range(num):
                ans.append(ans[-1] + iterator)
            while ans[-1] + iterator < len(allx) - 1:
                ans.append(ans[-1] + iterator - 1)
        except ZeroDivisionError:
            pass

        ans.append(len(x) - 1)
        if ans[-1] - ans[-2] < 2:
            del ans[-2]
        return ans
    def mean(l):
        return sum(l)/len(l)

    fig, axes = plt.subplots(2, 2)
    axes = axes.ravel()
    for filename, ax, title in zip(filenames, axes, titles):
        df = pd.read_excel(filename)
        df = df.to_numpy()
        df = removeData(df, 20)
        df[:, 1] = normalize(df[:, 1])

        x, y = df.shape
        funcs = [i for i in range(1, x)]
        funcs = funcs[:35]
        allx = [i for i in range(x)]
        allScores = []
        prev = []
        allVals = []

        for i in funcs:
            meanVal = []
            #print('Started ' + str(i))
            positions = points(allx, i)
            if positions == prev:
                allScores.append(allScores[-1])
                continue
            prev = positions[:]
            score, val = fit(df[positions[0]:positions[1], :], 1/30)
            meanVal.append(val)

            for j in range(1, len(positions) - 1):
                score1, val = fit(df[(positions[j] - 1):positions[j+1], :], 1/30)
                meanVal.append(val)
                score += score1

            allVals.append(mean(meanVal))
            allScores.append(score)
        ax.plot(funcs, allScores)
        ax.set_title(title, fontsize = 12)
        ax.set_xlabel('Number of Partitions', fontsize =8)
        ax.set_ylabel('Error', fontsize = 8)
    plt.subplots_adjust(hspace = 0.75)
    plt.savefig('FourErrors.pdf')
    plt.show()

def graph(filenames, titles):
    fig, axes = plt.subplots(2, 2)
    axes = axes.ravel()
    for filename, ax, title in zip(filenames, axes, titles):
        df = pd.read_excel(filename)
        df.insert(2, 'N/A', 0)
        df = df.to_numpy()
        df = removeData(df, 20)
        df = df[0:180, :]
        f = plt.figure(1)
        ax.plot(df[:,0], df[:,1], c='b')
        ax.set_title(title, fontsize = 16)
        ax.set_xlabel('Nucleotide Position', fontsize = 12)
        #ax.set_ylabel('Frequency', fontsize = 12)
        ax.set_yticks([])
    #plt.tick_params(axis='y', which='both', top=False, left='off')
    plt.subplots_adjust(hspace = 0.5, vspace = 0.5)
    plt.savefig('FourCurves.pdf')
    plt.show()

def graph2(filename):
    df = pd.read_excel(filename)
    df.insert(2, 'N/A', 0)
    df = df.to_numpy()
    #df = removeData(df, 20)
    df = df[20:380, :]
    plt.plot(df[:,0], df[:,1], c='b')
    plt.title(filename)
    plt.xlabel('Nucleotide Position')
    plt.ylim(0, 1500000)
    #plt.subplots_adjust(hspace = 5)
    #plt.ylabel('Frequency')
    plt.title('Aedes Albopictus Ovary')
    plt.yticks([])
    plt.savefig('FullCurve.JPG')
    plt.show()


filename1 = 'AeAeg_Ovary_TC.24_35.trim.fastq.uq.polyn.5to5_SPECIES.xls.xlsx'
filename2 = 'AeAlbo_Ovary_OA.24_35.trim.fastq.uq.polyn.5to5_SPECIES.xls'
filename3 = 'AnGam_Mos55-JRcells_BetaE.24_35.trim.fastq.uq.polyn.5to5_SPECIES.xls'
filename4 = 'CuQuin_Mcarc_NL.24_35.trim.fastq.uq.polyn.5to5_SPECIES.xls'
titles = ['Aedes albopictus', 'Aedes aegypti', 'Culex quinquefasciatus', 'Anopheles gambiae']
filenames = [filename2, filename1, filename4, filename3]
#multiFit(filenames, titles)
graph2(filename2)
#graph(filenames, titles)
