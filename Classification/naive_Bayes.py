# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 19:09:47 2017

@author: Deltau
"""

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)  #create union of words
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
       # else:
       #     print "the word: %s is not in my Vocabulary!" %word
    return returnVec    

def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Den = 2.0
    p1Den = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Den += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Den += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Den)        #use log function to prevent underflow
    p0Vect = log(p0Num/p0Den)
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1 - pClass1)
    if p1>p0:
        return 1
    else:
        return 0
 
####################Test samples
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec
#################################
   
def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))
    testEntry = ['love','my','dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList,testEntry))
    print testEntry,'classified as: ', classifyNB(thisDoc, p0V,p1V,pAb)
    testEntry = ['stupid','garbage']
    thisDoc = array(setOfWords2Vec(myVocabList,testEntry))
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V,p1V,pAb)
    
def bagOfWords2VectMN(vocabList, inputSet):
    returnVect = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVect[vocabList.index(word)] += 1
    return returreturnVect

def txtParse(totalString):
    import re
    listOfTokens = re.split(r'\W*',totalString)
    return [tok.lower() for tok in listOfTokens if len(tok)>2]

def spamTest():
    docList = []
    classList = []
    fullTxt = []
    for i in range(1,26):
        wordList = txtParse(open('file1.txt').read())
        docList.append(wordList)
        fullTxt.append(wordList)
        classList.append(1)
        wordList = txtParse(open('file2.txt').read())
        docList.append(wordList)
        fullTxt.append(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50)
    testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainingMat = []
    trainingClasses = []
    for docIndex in trainingSet:
        trainingMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainingClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainingMat),array(trainingClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
        print 'the error rate is: ', float(errorCount)/len(testSet)
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        