
import csv
import pandas as pd
from functions import lift, lift1

data = pd.read_csv("./dataset/list_disease.csv")
diseases = data['disease_emb'].values

data = pd.read_csv("./dataset/list_drug.csv")
drugs = data['drug_emb'].values

data = pd.read_csv("./dataset/list_adr.csv")
adrs = data['adr'].values

dSize = len(diseases)
rSize = len(drugs)
adrSize = len(adrs)

fileName = './dataset/medhelp_disease_all.txt'
f = open(fileName, 'r+')
lines = f.readlines()
totalThread = len(lines)

supportD = []
for disease in diseases:
    count = 0
    for line in lines:
        if disease in line:
            count += 1
    supportD.append(float(count)/totalThread)

supportR = []
for drug in drugs:
    count = 0
    for line in lines:
        if drug in line:
            count += 1
    supportR.append(float(count)/totalThread)

supportADR = []
for adr in adrs:
    count = 0
    for line in lines:
        if adr in line:
            count += 1
    supportADR.append(float(count)/totalThread)

print "Done: calculate supports"

# calculate lift-2_item: d-r d-d d-adr r-r r-adr adr-adr
lift(diseases, drugs, dSize, rSize, supportD, supportR, totalThread, lines, 'd_r')
lift1(diseases, dSize, supportD, totalThread, lines, 'd_d')
lift(diseases, adrs, dSize, adrSize, supportD, supportADR, totalThread, lines, 'd_adr')
lift1(drugs, rSize, supportR, totalThread, lines, 'r_r')
lift(drugs, adrs, rSize, adrSize, supportR, supportADR, totalThread, lines, 'r_adr')
lift1(adrs, adrSize, supportADR, totalThread, lines, 'adr_adr')

f.close()
