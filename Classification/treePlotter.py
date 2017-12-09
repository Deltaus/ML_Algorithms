# -*- coding: utf-8 -*-
"""
Created on Wed Nov 08 22:36:48 2017

@author: Deltau
"""

import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth",fc="0.8")
leafNode = dict(boxstyle="round4",fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords="axes fraction",xytext=centerPt,textcoords="axes fraction",va="center",ha="center",bbox=nodeType,arrowprops=arrow_args)

def getNumOfLeaves(myTree):
    numOfLeaves = 0
    firstItem = myTree.keys()[0]  #get 1st feature label
    secondDict = myTree[firstItem]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numOfLeaves += getNumOfLeaves(secondDict[key])
        else:
            numOfLeaves += 1
    return numOfLeaves

def getTreeDepth(myTree):
    maxDepth = 0
    firstItem = myTree.keys()[0]
    secondDict = myTree[firstItem]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth

def plotMidText(curPt, parentPt, txtStr):
    xTxt = (parentPt[0] - curPt[0])/2 + curPt[0]
    yTxt = (parentPt[1] - curPt[1])/2 + curPt[1]
    createPlot.ax1.text(xTxt,yTxt,txtStr)
    
def plotTree(myTree, parentPt, nodeTxt):
    numLeaves = getNumOfLeaves(myTree)
    depth = getTreeDepth(myTree)
    firstItem = myTree.keys()[0]
    curPt = (plotTree.xOff + (1.0 + float(numLeaves))/2.0/plotTree.totalW,plotTree.yOff)
    plotMidText(curPt, parentPt, nodeTxt)
    plotNode(firstItem,curPt,parentPt,decisionNode)
    secondDict = myTree[firstItem]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],curPt,str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),curPt,leafNode)
            plotMidText((plotTree.xOff,plotTree.yOff),curPt,str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD
    
def createPlot(inTree):
    fig = plt.figure(1,facecolor='white')
    fig.clf()
    axprops = dict(xticks=[],yticks=[])
    createPlot.ax1 = plt.subplot(111,frameon=False,**axprops)
    plotTree.totalW = float(getNumOfLeaves(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree,(0.5,1.0),'')
    plt.show()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        