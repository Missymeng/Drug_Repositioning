import csv
import pandas as pd
from collections import Counter

def initMatrix(row, col):
    mat = []
    for i in range(0, row):
        row = []
        for j in range(0, col):
            row.append(0)
        mat.append(row)
    return mat

def writeCSV(fileName,matrix):
    with open(fileName,'w') as f:
        writer = csv.writer(f)
        writer.writerows(matrix)
    print("Done: writing files")


with open('./data/relation/d_r_PharmGKB1.csv','r') as f:
    reader = csv.reader(f)
    d_r = list(reader)

with open('./data/relation/r_adr.csv','r') as f:
    reader = csv.reader(f)
    r_adr = list(reader)

drugs_1 = set()
for row in d_r:
    for item in row[1:]:
        if item:
            drugs_1.add(item)
print("len of drugs in D-R: ",len(drugs_1))

drugs_2 = [i[0] for i in r_adr[1:]]
print("len of drugs in R-ADR: ",len(drugs_2))

drugs_missing = set()
drugs_existing = set()
for drug in drugs_1:
    if drug in drugs_2:
        drugs_existing.add(drug)
    elif drug not in drugs_2:
        drugs_missing.add(drug)
print("len of drugs in D-R but not in R-ADR: ",len(drugs_missing))
print("len of drugs in D-R and in R-ADR: ",len(drugs_existing))

with open('./data/relation/list_adrs_expanded.csv','r') as f:
    reader = csv.reader(f)
    adrs = list(reader)
adrs_id = [i[0] for i in adrs[1:]]
adrs_name = [i[1] for i in adrs[1:]]
print("len of ADRs expanded: ",len(adrs_id))


data_file = './data/medhelp/medhelp_disease_all_raw.txt'
with open(data_file) as f:
    lines = f.readlines()
print("num of threads: ",len(lines))

r_adr_1 = []
r_adr_1.append(r_adr[0])
for row in r_adr[1:]:
    if row[0] in drugs_1:
        r_adr_1.append(row)
writeCSV('./data/relation/r_adr_1.csv',r_adr_1)

r_adr_2 = initMatrix(len(drugs_missing),len(adrs_id[23:]))
for i,drug in enumerate(drugs_missing):
    print(drug)
    for j,adr in enumerate(adrs_id[23:]):
        if r_adr_2[i][j] > 100:
            continue
        for line in lines:
            if drug in line and adr in line:
                r_adr_2[i][j] += 1
writeCSV('./data/relation/r_adr_2.csv',r_adr_2)

r_adr_3 = initMatrix(len(drugs_existing),len(adrs_name[:23]))
print("size of new r_adr matrix: ",len(r_adr_3),len(r_adr_3[0]))
for i,drug in enumerate(drugs_existing):
    print(i,drug)
    for j,adr in enumerate(adrs_name[:23]):
        if r_adr_3[i][j] > 100:
            continue
        for line in lines:
            if drug in line and adr in line:
                r_adr_3[i][j] += 1
writeCSV('./data/relation/r_adr_3.csv',r_adr_3)

r_adr_4 = initMatrix(len(drugs_missing),len(adrs_name[:23]))
print("size of new r_adr matrix: ",len(r_adr_4),len(r_adr_4[0]))
for i,drug in enumerate(drugs_missing):
    print(i,drug)
    for j,adr in enumerate(adrs_name[:23]):
        if r_adr_4[i][j] > 100:
            continue
        for line in lines:
            if drug in line and adr in line:
                r_adr_4[i][j] += 1
writeCSV('./data/relation/r_adr_4.csv',r_adr_4)

with open('./data/relation/r_adr_expanded.csv','r') as f:
    reader = csv.reader(f)
    r_adr = list(reader)
print("size of new r_adr matrix: ",len(r_adr),len(r_adr[0]))

with open('./data/relation/list_r.csv','r') as f:
    reader = csv.reader(f)
    drugs = list(reader)
drugs = [drug[0] for drug in drugs]
print("len of drugs: ",len(drugs))

with open('./data/relation/list_adr_expanded.csv','r') as f:
    reader = csv.reader(f)
    adrs = list(reader)
adrs_name = [i[1] for i in adrs[1:]]
print("len of ADRs: ",len(adrs_name))

for row in r_adr[:2]:
    for item in row:
        try:
            item = float(item)
        except ValueError:
            item = 0

drug_adr = []
for i,row in enumerate(r_adr):
    row_float = []
    for item in row:
        try:
            row_float.append(float(item))
        except ValueError:
            row_float.append(0)

    drug_adr_line = []
    drug_adr_line.append(drugs[i])
    for pair in sorted(enumerate(row_float),key=lambda x:x[1],reverse=True):
        # pair[0]: index of element, pair[1]: value of element
        if pair[1] != 0:
            drug_adr_line.append(adrs_name[pair[0]])
            # print(pair[0])
    drug_adr.append(drug_adr_line)
print("size of new r_adr matrix: ",len(drug_adr))
writeCSV('./data/drug_adr_sorted.csv',drug_adr)

count = 0
adr_drug = []
for j in range(len(r_adr[0])):
    col_float = []
    for i in range(len(r_adr)):
        try:
            col_float.append(float(r_adr[i][j]))
        except ValueError:
            col_float.append(0)

    adr_drug_line = []
    adr_drug_line.append(adrs_name[j])
    for pair in sorted(enumerate(col_float),key=lambda x:x[1],reverse=True):
        if pair[1] != 0:
            adr_drug_line.append(drugs[pair[0]])
    adr_drug.append(adr_drug_line)
writeCSV('./data/adr_drug_sorted.csv',adr_drug)
print("size of new r_adr matrix: ",len(adr_drug))

with open('./data/relation/d_r_PharmGKB1.csv','r') as f:
    reader = csv.reader(f)
    d_r = list(reader)

with open('./data/relation/adr_drug_sorted.csv','r') as f:
    reader = csv.reader(f)
    adr_drug = list(reader)
adrs = [i[0] for i in adr_drug]

with open('./data/relation/drug_adr_sorted.csv','r') as f:
    reader = csv.reader(f)
    drug_adr = list(reader)
drugs = [i[0] for i in drug_adr]

### find out significant d-adr associations ###
d_adr = []
for line in d_r:
    d_adr_line = []
    d_adr_line.append(line[0])
    adr_count = Counter()
    for drug in line[1:]:
        if drug:
            if 'alfacalcidol' in drug:
                idx = 0
            else:
                idx = drugs.index(drug)  # get index of drug
            adr_line = drug_adr[idx]    # find the line in drug_adr
            for adr in adr_line[1:]:    # count num of occurring of ADR in drugs indicated for a disease
                if adr:
                    adr_count[adr] += 1
    for adr,count in adr_count.most_common(15):  # get the most common 8 ADRs for a disease
        d_adr_line.append(adr)
    d_adr.append(d_adr_line)
writeCSV('./data/relation/d_adr_sig.csv',d_adr)


with open('./data/relation/d_adr_sig.csv','r') as f:
    reader = csv.reader(f)
    d_adr = list(reader)

### find d and repositioningDrugs via intermediate ADR ###
d_reposR = []
for line in d_adr:
    drug_count = Counter()
    d_reposR_line = []
    d_reposR_line.append(line[0])
    for adr in line[1:11]:
        idx = adrs.index(adr)
        drug_line = adr_drug[idx]
        for drug in drug_line[1:]:
            if drug:
                drug_count[drug] += 1
    for drug,count in drug_count.most_common():
        d_reposR_line.append(drug)
    d_reposR.append(d_reposR_line)

# filter out drugs already indicated for that disease
d_reposition = []
for i,line in enumerate(d_reposR):
    d_repos_line = []
    d_repos_line.append(d_reposR[i][0])
    for drug in line:
        if drug and drug not in d_r[i]:
            d_repos_line.append(drug)
    print(len(d_repos_line))
    d_reposition.append(d_repos_line)
writeCSV('./data/relation/d_reposition.csv',d_reposition)



