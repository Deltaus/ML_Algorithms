# -*- coding: utf-8 -*-
"""
Created on Sun Nov 05 19:01:59 2017

@author: Deltau
"""

import numpy as np
import operator

def classifier(inData, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]    # row number of dataset
    diffMat = np.tile(inData, (dataSetSize,1))  #repeat inData dataSetSize times in row, 1 time in col
    diffMat = diffMat - dataSet  #difference
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1) #calculate sum in direction of axis 1
    distances = sqDistances**0.5
    sortedDistanceIndicies = distances.argsort() #return an array of index of sorted distances
    classCount = {}  #dictionary of classes and their times of appearance
    for i in range(k):
        voteLabel = labels[sortedDistanceIndicies[i]]
        classCount[voteLabel] = classCount.get(voteLabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]  #return the class counted most

def file2matrix(filename,col):
    infile = open(filename)
    arrayOfLines = infile.readlines() #read the entire file in form of lines
    numberOfLines = len(arrayOfLines)
    returnMat = zeros((numberOfLines,col)) #create a numberOfLine x 3 matrix
    classLabelVector = []
    index = 0
    for line in arrayOfLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:col]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector

def autonorm(dataSet):
    minVals = dataSet.min(0) #return min values of each column;  a row array
    maxVals = dataSet.max(0) #return max values of each column;  a row array
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet)) #create a matrix of the same size as dataSet
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet, ranges, minVals

def classify(testData, trainingData, trainingLabels, k):
    m = testData.shape[0]
    resultLabel = []
    #error = 0
    for i in range(m):
        classifierResult = classifier(testData[i,:], trainingData, trainingLabels, k)
        #classNumStr = labelTest[i]
        resultLabel.append(classifierResult)
        #if classifierResult != classNumStr:
            #error += 1
    #print "\nAccuracy: %f"%(1.0 - error/float(m))
    return resultLabel

#load data
tmpTraining = np.loadtxt("train.csv",dtype=np.str,delimiter=',')
dataTraining = tmpTraining[1:,1:].astype(np.float)
labelTraining = tmpTraining[1:,0].astype(np.float)

tmpTest = np.loadtxt("test.csv",dtype=np.str,delimiter=',')
dataTest = tmpTest[1:,0:].astype(np.float)
#labelTest = tmpTest[1:,0].astype(np.float)



'''
#set training and test data 3:2
num = data.shape[0]
numTraining = int(num*0.6)
dataTraining = data[0:numTraining,:]
labelTraining = label[0:numTraining]

dataTest = data[(numTraining+1):,:]
labelTest = label[(numTraining+1):]
'''
result = classify(dataTest,dataTraining,labelTraining,3)
result_arr = np.array(result)
seq = np.arange(dataTest.shape[0]) + 1
tp = [seq,result_arr]
final = np.array(tp).transpose()
