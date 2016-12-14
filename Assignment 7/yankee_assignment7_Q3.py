import random
import numpy as np
import matplotlib.pyplot as plt
import collections

ROLLDICESIDES = 6
# roll two dice and get sum
def rollDiceGetSum():
    return random.randint(1, ROLLDICESIDES) + random.randint(1, ROLLDICESIDES)

def rollDiceAndGetListOfSums(n):
    return np.sort([rollDiceGetSum() for i in range(n)])

# draw a CDF plot for a given list of normalised data.
def drawCDFPlot(listElements , xLabel , yLabel):
    x_1 = [x for x in range(1, len(listElements)+1)]
    y_1 = np.array(listElements)
   
    plt.figure(figsize=(10,6))
    plt.plot(x_1, y_1 , drawstyle='steps-post' , color = 'b' , label = 'CDF')
    
    plt.xlabel(xLabel)
    plt.ylabel(yLabel) 
    plt.ylim(0, 1.2)
    plt.title('cumulative step')
    
    plt.xlim(xmin=1)    
    plt.axvline(np.median(x_1), color='r', linestyle='dashed', linewidth=2 , \
                                    label = "median = " + str(np.median(x_1)))
    
    print(x_1)
    plt.axhline(y_1[8], color='g', linestyle='dashed', linewidth=2 , \
                        label = "probability dice sum <= 9 : " + str(y_1[8]))
     
    plt.legend(loc='upper right')  
    plt.grid()
    plt.show() 

def drawCDFPlotTwo(listElements1 , listElements2 , xLabel , yLabel):
    x_1 = [x for x in range(1, len(listElements1)+1)]
    y_1 = np.array(listElements1)
    
    x_2 = [x for x in range(1, len(listElements2)+1)]
    y_2 = np.array(listElements2)
   
    plt.figure(figsize=(10,6))
    plt.plot(x_1, y_1 , drawstyle='steps-post' , color = 'b' , label = 'CDF1st')
    plt.plot(x_2, y_2 , drawstyle='steps-post' , \
                                             color = 'gray' , label = 'CDF2nd')
    
    plt.xlabel(xLabel)
    plt.ylabel(yLabel) 
    plt.ylim(0, 1.2)
    plt.title('cumulative step')
    plt.xlim(xmin=1)
    
    plt.axvline(np.median(x_1), color='r', linestyle='dashed', linewidth=2 , \
                             label = "median for 1st = " + str(np.median(x_1)))
    
    plt.axvline(np.median(x_2), color='black', linestyle='dashed', linewidth=2,\
                              label = "median for 2nd= " + str(np.median(x_2)))
    
    plt.axhline(y_1[8], color='g', linestyle='dashed', linewidth=2 , \
                   label = "1st probability dice sum <= 9 is : " + str(y_1[8]))
    plt.axhline(y_2[8], color='brown', linestyle='dashed', linewidth=2 , \
                   label = "2nd probability dice sum <= 9 is : " + str(y_2[8]))
     
    plt.legend(loc='bottom right')  
    plt.grid()
    plt.show() 
    
def drawHistogram(listElements , xLabel , yLabel, interval):
    print (listElements)
    x_1 = np.array(listElements)
    plt.figure(figsize=(10,5))
    plt.hist(x_1 , bins= range(0, 12, interval) , color='c' )
    plt.xlabel(xLabel)
    plt.ylabel(yLabel) 
    plt.xlim(xmin=2)
    plt.axvline(np.median(x_1), color='r', linestyle='dashed', linewidth=2 , \
                                    label = "median = " + str(np.median(x_1)))
    
    plt.legend(loc='upper right')  
    plt.show()

    
def calculateCDF(result):
    frequencyNum = collections.Counter(result).most_common()
    total = sum([frequency for (key, frequency) in frequencyNum])
    probabilityForEachNumDict = {}
    for (key, frequency) in frequencyNum:
        probabilityForEachNumDict[key] = frequency / \
                                          total

    arrayForCDFCalc = list(probabilityForEachNumDict.values())
    a = np.array(arrayForCDFCalc)
    cdfEvalDict = np.cumsum(a)
    return (list(probabilityForEachNumDict.keys()), cdfEvalDict)

def performKolmogorovSmirnovTest(cdfsMain , cdfsToCompare):
     maxPointwiseDistance = max([abs(cdf_S - cdf_Zipf) \
                                 for (cdf_S , cdf_Zipf) in \
                                                zip(cdfsMain , cdfsToCompare)])
     return maxPointwiseDistance

     
if __name__ == "__main__":    
    drawHistogram(rollDiceAndGetListOfSums(100) ,"Sum Results" ,"Frequencies", 1)
    (eachNumbers , associatedCDFs) = calculateCDF(rollDiceAndGetListOfSums(100))
    (eachNumbers , secondAssociatedCDFs) = calculateCDF(\
                                                rollDiceAndGetListOfSums(100))
    drawCDFPlot(associatedCDFs , "Dice Sum Rank", "Cumulative Frequency %" )
    drawCDFPlotTwo(associatedCDFs , secondAssociatedCDFs, "Dice Sum Rank" , \
                                                      "Cumulative Frequency %")    
    #Computing the maximum pointwise distance for both CDF's
    print ("Maximum PointWise Distance of both CDF's when ran 100 is : " , \
           performKolmogorovSmirnovTest(associatedCDFs , secondAssociatedCDFs))
    
    
    (eachNumbers1000 , associatedCDFs1000) = calculateCDF(\
                                                rollDiceAndGetListOfSums(1000))
    (eachNumbers1000 , secondAssociatedCDFs1000) = \
                                   calculateCDF(rollDiceAndGetListOfSums(1000))
    drawCDFPlotTwo(associatedCDFs1000 , secondAssociatedCDFs1000, \
                                   "Dice Sum Rank" , "Cumulative Frequency %")    
    #Computing the maximum pointwise distance for both CDF's
    print ("Maximum PointWise Distance of both CDF's when ran 1000 is : ",\
      performKolmogorovSmirnovTest(associatedCDFs1000 , secondAssociatedCDFs1000))