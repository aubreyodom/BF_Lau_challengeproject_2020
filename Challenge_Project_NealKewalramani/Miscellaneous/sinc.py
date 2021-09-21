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
    print(array)
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
    for i in x:
        y.append((ans[0])*sinc(alpha * i)  + ans[1] * i**2 + ans[2]*i + ans[3])# + (i**2)*sinc(alpha*i))
        #y.append((ans[0]*i)*sinc(alpha * i) + (ans[1])*sinc(alpha * i) + ans[2] * i**2 + ans[3]*i + ans[4])# + (i**2)*sinc(alpha*i))
        #y.append(ans[0] + ans[1]*i + ans[2]*(i**2) + ans[3]*(i**3) + ans[4]*(i**4) + ans[5]*(i**5) + ans[6]*(i**6) + ans[7]*(i**7) + ans[8]*(i**8) + ans[9]*(i**9) + ans[10]*(i**10))
    #print(ans[4])
    plt.plot(df[:,0], df[:,1], c='b')
    plt.plot(x, y, c = 'r')
    #plt.show()
    #print(error)
    return error

def multiFit(filename):
    def points(x, funcs):
        ans = [0]

        try:
            num = len(x) % funcs
            iterator = int(len(x)/funcs)
            for _ in range(num):
                ans.append(ans[-1] + iterator)
            while ans[-1] + iterator < len(allx) - 1:
                ans.append(ans[-1] + iterator - 1)

            '''
            iterator = len(x) // (funcs)
            while ans[-1] + iterator < len(allx) - 1:
                ans.append(ans[-1] + iterator)
            '''
        except ZeroDivisionError:
            pass

        ans.append(len(x) - 1)
        if ans[-1] - ans[-2] < 4:
            del ans[-2]
        return ans

    df = pd.read_excel(filename)
    #df.insert(2, 'N/A', 0)
    df = df.to_numpy()
    df = removeData(df, 20)

    x, y = df.shape
    funcs = [i for i in range(1, x//2 + 1)]
    funcs = funcs[:36]
    allx = [i for i in range(x)]
    #print(allx)
    #print(len(allx))
    #print(points(allx, len(allx)-90) == points(allx, len(allx)))
    allScores = []
    prev = []
    #print(funcs[0:2])
    for i in funcs:
        positions = points(allx, i)
        print(positions)
        #print(positions)
        if positions == prev:
            allScores.append(allScores[-1])
            continue
        prev = positions[:]
        #print(positions)
        #print('New:')
        score = fit(df[positions[0]:positions[1], :], 1/50)
        #print(positions[0], positions[1])
        for j in range(1, len(positions) - 1):
            score += fit(df[(positions[j] - 1):positions[j+1], :], 0.20)
        #    print(positions[j] - 1, positions[j+1])
        #print(score, i)
        plt.show()
        allScores.append(score)
    #print(allScores)
    plt.plot(funcs, allScores)
    plt.show()

def graph(filename):
    df = pd.read_excel(filename)
    df.insert(2, 'N/A', 0)
    df = df.to_numpy()
    df = removeData(df, 20)
    plt.plot(df[:,0], df[:,1], c='b')
    plt.title('AeAlbo Ovary')
    plt.xlabel('Nucleotide Position')
    plt.ylabel('Frequency')
    plt.show()

filename1 = 'AeAlbo_Ovary_OA.24_35.trim.fastq.uq.polyn.5to5_SPECIES.xls.xlsx'
filename2 = 'AeAeg_Ovary_TC.24_35.trim.fastq.uq.polyn.5to5_SPECIES.xls.xlsx'
filename3 = 'CuQuin_Fcarc_NL.24_35.trim.fastq.uq.polyn.5to5_SPECIES.xlsx'
filename4 = 'aeg_fc_scaled.csv'
x = 200
y = -200
dic = {'t1': (x, y), 'r1': np.pi/2, 't2': (-x, -y)}
#adjustData(filename, dic)
#fit(filename, 0.12)
multiFit(filename1)
#graph(filename2)
