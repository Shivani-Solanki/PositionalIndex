'''
Created on Mar 7, 2019

@author: solan
'''
from os import listdir
from os.path import isfile, join
from collections import defaultdict, Counter, OrderedDict
import re
import json
def querysearch(text): 
    try:
        global PosInvInd
        with open('positionalindex.txt') as jsonfile:
            PosInvInd= json.load(jsonfile) 
            global queryT  
            match= {}
            temp = {} 
            queryT=list(text.split())  
            for word in queryT:
                if word == 'AND':
                    andInd= queryT.index(word)
                elif word == 'OR':
                    orInd= queryT.index(word)
                else:
                    continue
                    
            if queryT.__contains__("AND") and queryT.__contains__("OR"):
                if (andInd>orInd):
                    match= AND_TermsFromDictionary(queryT[andInd-1].lower(),queryT[andInd+1].lower())
                    temp= OR_TermsFromDictionary(queryT[orInd-1].lower())
                    match.update(temp)
                    return(match)
                else:
                    match= AND_TermsFromDictionary(queryT[andInd-1].lower(),queryT[andInd+1].lower())
                    temp= OR_TermsFromDictionary(queryT[orInd+1].lower())
                    match.update(temp)
                    return(match)
                
            elif queryT.__contains__("AND"):
                match= AND_TermsFromDictionary(queryT[andInd-1].lower(),queryT[andInd+1].lower()) 
                return(match)
            
            elif queryT.__contains__("OR"):
                match= temp= OR_TermsFromDictionary(queryT[orInd-1].lower(),queryT[orInd+1].lower()) 
                return(match)
    except KeyError as error:
        print('Invalid query: reasons: incorrect spellings; chars,symbols,numbers,stopwords are not included in the index, hence not accepted in the query. Pl. follow the format specified.')      
     
def OR_TermsFromDictionary(*args):
    dicDoc={}
    for word in args:
        for element,v in PosInvInd.items():
            for k in PosInvInd[element]:
                if(word==element):
                    dicDoc.update({word:PosInvInd[word][k]})
    return dicDoc

def AND_TermsFromDictionary(t1,t2):
    INV={}              
    a= PosInvInd[t1]
    b= PosInvInd[t2]
    d=list(a.values())[0]
    e=list(b.values())[0]
    for key1 in d.keys():
        for key2 in e.keys():
            if key1==key2:
                INV.setdefault(t1,{}).update({key1:d[key1]})
                INV.setdefault(t2,{}).update({key2:e[key2]})
    return INV
               
query= input('Enter the query in form: word1 OR word2, word1 AND word2, word1 OR word2 AND word3, word1 AND word2 OR word3 :')
result= querysearch(query)
print(result)
