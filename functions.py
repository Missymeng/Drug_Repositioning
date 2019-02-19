import csv
import os

def initMatrix(row, col):
    mat = []
    for i in range(0, row):
        row = []
        for j in range(0, col):
            row.append(0)
        mat.append(row)
    return mat

def csv_writer(lists,name):
    basedir = './dataset/weight_metapath'
    filename = os.path.join(basedir,name+'.csv')
    with open(filename, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(lists)
    print 'Done:', name

def csv_reader(name):
    basedir = './dataset/weight_metapath'
    filename = os.path.join(basedir,name+'.csv')
    with open(filename,'rb') as f:
        reader = csv.reader(f)
        resultList = list(reader)
    return resultList

def lift(diseases, drugs, dSize, rSize, supportD, supportR, totalThread, lines, outputFile):
    # initialize matrix
    output = initMatrix(dSize, rSize)
    # calculate count(d & r)
    for i in range(0, dSize):
        for j in range(0, rSize):
            for line in lines:
                if diseases[i] in line and drugs[j] in line:
                    output[i][j] += 1
    for i in range(0, dSize):
        for j in range(0, rSize):
            if output[i][j] == 0: continue
            deno = float(totalThread * supportD[i] * supportR[j])
            if deno == 0: continue
            output[i][j] = float(output[i][j])/deno

    outputFile = './dataset/weight_lift/' + outputFile + '.csv'
    with open(outputFile, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(output)
    print "Done: " + outputFile


def lift1(diseases, dSize, supportD, totalThread, lines, outputFile):
    output = initMatrix(dSize, dSize)
    # calculate count(d & r)
    for i in range(0, dSize):
        for j in range(0, dSize):
            if j == i:
                continue
            for line in lines:
                if diseases[i] in line and diseases[j] in line:
                    output[i][j] += 1
    for i in range(0, dSize):
        for j in range(0, dSize):
            if j == i: continue
            if output[i][j] == 0: continue
            deno = float(totalThread * supportD[i] * supportD[j])
            if deno == 0: continue
            output[i][j] = float(output[i][j])/deno

    outputFile = './dataset/weight_lift/' + outputFile + '.csv'
    with open(outputFile, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(output)
    print "Done: " + outputFile
