
import csv
import glob
import pandas as pd
from nltk import tokenize, re
import data_prep.py

def sentence2word(inputFile,outputFile):

    with open(inputFile) as dataFile:
        sentences = dataFile.read().splitlines()

    rows = []
    for sentence in sentences:
        row = []
        row.append(sentence); row.append('Sentence'); rows.append(row)
        row = []
        row.append('BOS'); row.append('BOS'); rows.append(row)

        # split sentence into words and punctuations
        words = re.findall(r"[\w']+|[().,!?;]", sentence)
        for word in words:
            row = []
            row.append(word)
            row.append('O')
            rows.append(row)
        row = []
        row.append('EOS'); row.append('EOS'); rows.append(row)

    with open(outputFile,'w') as w:
        writer = csv.writer(w)
        writer.writerows(rows)
    print('Done: sentence text to word+\'O\' csv')
    
# write each thread into a line, and merge all files into one file
path = './data/medhelp_disease/*.txt'
files = glob.glob(path)
resultList = []
for fileName in files:
    with open(fileName) as data:
        sentences = data.read().splitlines()

    tempStr = ""
    for i in range(0, len(sentences)-1):
        if "Content:" in sentences[i]:
            tempStr += sentences[i]
        if "User0:" in sentences[i+1]:
            resultList.append(tempStr)
            tempStr = ""
    resultList.append(tempStr)

f = open('./data/medhelp_disease_all.txt', 'w')
f.writelines(["%s\n" % result for result in resultList])
print("Done")

# ## split text into sentence by sentence, using NLTK
# open input file, read all columns, address unexpected letters
fp = open("./data/medhelp_disease_all.txt")
data = fp.read()
# data = unicode(data, errors='ignore')

# tokenize text into sentences, using nltk
sentences = tokenize.sent_tokenize(data)
print(len(sentences))

# write generated list of strings into txt file
file = open('./data/medhelp_disease_sentence.txt', 'w')
file.writelines(["%s\n" % sentence for sentence in sentences])
print('Done')

if __name__ == "__main__":
    # inputFile = './data/all.txt'
    sentenceFile = './data/all_sentence.txt'

    # text2sentence(inputFile,sentenceFile)
    # word2id(sentenceFile)

    wordFile = './data/all_word.csv'
    # sentence2word(sentenceFile,wordFile)

    with open('./data/label_file_1.csv','w') as f:
        writer = csv.writer(f)
        writer.writerows(bioLists)
