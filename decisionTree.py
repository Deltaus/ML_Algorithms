# -*- coding: utf-8 -*-
"""
Created on Wed Nov 08 20:44:45 2017

@author: Deltau
"""
from math import log
import operator


#Calculate Shannon Entropy
def calShannonEnt(dataSet):
    numOfEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]    #currentLabel = Yes/No
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numOfEntries #num of Yes/No divided by total number
        shannonEnt -= prob * log(prob,2)
    return shannonEnt


#Split data by feature on specific axis , those whose value = value remain
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])   #These 2 lines delete value on the specific axis
            retDataSet.append(reducedFeatVec)
    return retDataSet  

#Choose the best feature to divide the dataset
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calShannonEnt(dataSet)
    bestInfoGain = 0.0;bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)  #get the set of features(no repeat element)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

#Return the most frequently present feature
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

#Build a Decision Tree
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList): #if all the elements share the same class with the 1st element
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet) #bestfeat - index of a feature label(an int)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

    
    
    
    
    
    
    
    
    
    
    
    