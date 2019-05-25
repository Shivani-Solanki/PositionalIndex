'''
Created on Mar 1, 2019

@author: solan
'''
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import re
import json

def PosInd(Dir):
    #direc= input('Please enter the Directory path:')
    #C:\\Users\\solan\\Downloads\\assuns
    #print('Hi',direc)
    filenames = [f for f in listdir(Dir) if isfile(join(Dir, f))]
    
    index=defaultdict(lambda: defaultdict(list))
    DF = defaultdict(int) 
    positionalIndex=defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    docno = defaultdict(list)
    
    def openingfile(direc,filename):
        with open(direc+'/'+ filename, 'r') as text:
            words = (re.sub(r"[^a-zA-Z]+", ' ', text.read())).lower()     
            splitWords = ((words.lower().split()))
            pos=enumerate(splitWords,start=1)          
        return splitWords,pos
    
    for file in filenames:
        docid=file
        text,posn= openingfile(Dir, file)
        for pos, word in posn:
            index[word][docid].append(pos)
            if (word) in docno.keys():
                    if docid not in docno[word]:
                        docno[word].append(docid)                    
            else:
                docno[word].append(docid)
        for word in set(text):
            DF[word] += 1
    index=dict(index)
    DF=dict(DF)
    
    for key in index.keys():
        if key in DF.keys():
            positionalIndex[key][DF[key]].update(index[key])
                
    for key in list(positionalIndex):
        if key in ('and', 'but', 'is', 'the', 'to'):
            positionalIndex.pop(key)
    positionalIndex=dict(positionalIndex)     
    return positionalIndex

def writedisk(positionalIndex):
    with open('positionalindex.txt', 'w') as outfile:
        json.dump(positionalIndex, outfile)



Dir= input('Enter the directory path from where the input .txt files are to be read, in form C:\\Users\\solan\\Document\\Assignment2:')
data=PosInd(Dir)
writedisk(data)
print ('The inverted index has been created and loaded into a file positionalindex.txt and is ready to use.')


    