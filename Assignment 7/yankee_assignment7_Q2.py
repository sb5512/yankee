import collections
import numpy as np
import ast
import bisect
import random
import matplotlib.pyplot as plt 
from threading import Thread

counterAllCharInEnglish = 0
THREADS = 30

#Parses the file. Helper function for countCharactersSpaces()
def getEachLinesFromFile(filename):
    with open(filename , encoding="utf8") as fp:
        try:
            content = fp.read()
        except:
            content = ""
    return content
 
def writeTextToFile(filename , text):
    with open(filename , 'w+' , encoding="utf8") as fp:
        try:
            content = fp.write(text)
        except:
            content = ""
    return content

    
# Get the total characters in Simple English file
def getCharactersInSimpleEnglish(filename):
    getSimpleEnglishText = getEachLinesFromFile(simpleEnglishFilename)
    return len(getSimpleEnglishText)


#Returns probabilities in the file as dictionaries. Each dictionaries are 
#elements of list. Note we here only have Zipf and uniform probabilities.   
def readProbabilitiesFromFileToDict(filename):    
    with open(filename, 'r') as f:
        s = f.read() 
    
    # ------------------------ First part for Zipf   --------------------------
    if s.find('{') < 0:
        return None        
    s = s[s.find('{'):]

    if s.find('}') < 0:
        return None        
    zipf_probabilities = s[:s.find('}') + 1]
    
    # ------------------------Second part for Uniform--------------------------
    # Getting the remaining probabilities after deducing Zipf
    remainingProbabilities = s[s.find('}') + 1:]  
    
    # Now we strip the remaningProb to get uniform probabilities
    if remainingProbabilities.find('{') < 0:
        return None        
    remainingProbabilities = remainingProbabilities\
                                            [remainingProbabilities.find('{'):]

    if remainingProbabilities.find('}') < 0:
        return None
    uniformProbabilities = remainingProbabilities\
                                        [:remainingProbabilities.find('}') + 1]
        
    zipf_probabilitiesDict = ast.literal_eval(zipf_probabilities)
    uniformProbabilitiesDict = ast.literal_eval(uniformProbabilities)
    return [zipf_probabilitiesDict , uniformProbabilitiesDict]

#------------------------------------------------------------------------------    
# Section RandomTextGenerate STARTS 
#------------------------------------------------------------------------------

# This section is for generating random text when the characters to be used are
# sent with its associated CDF
# Note we create 30 threads

def threadToGetRandomText(allKeys , associatedCDF , result , indexer):
    characters = []
    for x in range(0, counterAllCharInEnglish // THREADS):        
        randomValue = random.random()
        index = bisect.bisect(associatedCDF, randomValue) 
        characters.append(allKeys[index])
    text = "".join(characters) 
    result[indexer] = text
    return text

def getRandomTextAsPerProbabilityDist(allKeys , associatedCDF):
    threads = [None] * THREADS
    results = {}
    i = 0;
    for i in range(0, len(threads)):
        threads[i] = Thread(target=threadToGetRandomText, \
                                    args=(allKeys , associatedCDF, results, i))
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()
        
    return ''.join(list(results.values()))

#------------------------------------------------------------------------------
# Section RandomTextGenerate ENDS      
#------------------------------------------------------------------------------


def getWordWithItsProbabilities(text):
    frequencyEachWord_S = collections.Counter(text.split()).most_common()    
    #Here we get probabilities for each character
    sumOfTotalCharOccurrence = sum([frequency for (key,frequency) in \
                                                    frequencyEachWord_S])
    probabilityForEachWordDict = {}    
    for (key , frequency) in frequencyEachWord_S:
        probabilityForEachWordDict[key] = frequency / \
                                                    sumOfTotalCharOccurrence 
    print ("totalSum Word" ,sumOfTotalCharOccurrence )
    return probabilityForEachWordDict 

def cdfCalculation(probDictForCDFCalc):
    arrayForCDFCalc = list(probDictForCDFCalc.values())
    a = np.array(arrayForCDFCalc) #Gets us CDF 
    cdfEvalDict = np.cumsum(a)
    return (list(probDictForCDFCalc.keys()) , cdfEvalDict)        


def performKolmogorovSmirnovTest(cdfsMain , cdfsToCompare):
     maxPointwiseDistance = max([abs(cdf_S - cdf_Zipf) \
                                 for (cdf_S , cdf_Zipf) in \
                                                zip(cdfsMain , cdfsToCompare)])
     return maxPointwiseDistance

#------------------------------------------------------------------------------    
# Section Plots STARTS 
#------------------------------------------------------------------------------

# This section is for plotting rank frequency diagram 
    
def drawPlot(listElements_S , listElements_Z , listElements_U , xLabel , yLabel):
    x_S = [x for x in range(1, len(listElements_S)+1)]
    y_S = np.array(listElements_S)
    x_Z = [x for x in range(1, len(listElements_Z)+1)]
    y_Z = np.array(listElements_Z)
    x_U = [x for x in range(1, len(listElements_U)+1)]
    y_U = np.array(listElements_U)
    plt.figure(figsize=(12,9))
    plt.plot(x_S, y_S , 'r', label = "Simple English")
    plt.plot(x_Z, y_Z , 'b', label = "Zips Distribution Words")
    plt.plot(x_U, y_U , 'g', label = "Uniform Distribution Words")
    
    plt.xlabel(xLabel)
    plt.ylabel(yLabel) 
    plt.yscale('log')
    plt.xscale('log')
    plt.legend(loc='upper right')  
    plt.grid()
    plt.show() 
    
def drawCDFPlot(listElements_S , listElements_Z , listElements_U , xLabel , yLabel):
    x_S = [x for x in range(1, len(listElements_S)+1)]
    y_S = np.array(listElements_S)
    x_Z = [x for x in range(1, len(listElements_Z)+1)]
    y_Z = np.array(listElements_Z)
    x_U = [x for x in range(1, len(listElements_U)+1)]
    y_U = np.array(listElements_U)
    plt.figure(figsize=(12,9))
    plt.plot(x_S, y_S , 'r', label = "Simple English")
    plt.plot(x_Z, y_Z , 'b' , label = "Zips Distribution Words")
    plt.plot(x_U, y_U , 'g' , label = "Uniform Distribution Words")
    
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(0, 1.2)
    plt.legend(loc='bottom right')  
    plt.grid()
    plt.show() 

#------------------------------------------------------------------------------
# Section Plots ENDS      
#------------------------------------------------------------------------------

 

def mainFunction(simpleEnglishFilename , probabilitiesFilename):
    # This one is for simple english wikipedia. 
    # Here we get the probability for each character in a dictionary format. 
    # Then we get CDF for each words in tuple format
    getSimpleEnglishText = getEachLinesFromFile(simpleEnglishFilename)
    probabilityForEachWordDict = getWordWithItsProbabilities(getSimpleEnglishText)    
    (allKeys_S, associatedCDF_S ) = cdfCalculation(probabilityForEachWordDict)
        
        
    # This one is for probabilistic distribution given in file. 
    # i.e. probability distribution and uniform distribution
    probabilityDistFromFile =  readProbabilitiesFromFileToDict(\
                                                         probabilitiesFilename)
    (allKeys_Zipf, associatedCDF_Zipf ) = cdfCalculation(\
                                                    probabilityDistFromFile[0])
    (allKeys_Unif, associatedCDF_Unif ) = cdfCalculation(\
                                                    probabilityDistFromFile[1])
    
    #following gives the text for the Zipf and uniform distribution
    text_Zipf = getRandomTextAsPerProbabilityDist(allKeys_Zipf , \
                                                  associatedCDF_Zipf)
    text_Unif = getRandomTextAsPerProbabilityDist(allKeys_Unif , \
                                                  associatedCDF_Unif)
    
    
    probabilityForEachWordDict_Zipf = getWordWithItsProbabilities(text_Zipf)    
    (allKeys_NewZipf, associatedCDF_NewZipf ) = cdfCalculation(\
                                            probabilityForEachWordDict_Zipf)
    
    probabilityForEachWordDict_Unif = getWordWithItsProbabilities(text_Unif)    
    (allKeys_NewUnif, associatedCDF_NewUnif ) = cdfCalculation(\
                                            probabilityForEachWordDict_Unif)
    
    
    #To put both obtained text into a file
    #print('Zipf text' ,text_Zipf )
    #print('\nUnif text' ,text_Zipf)
    
    writeTextToFile("ZipfCreatedText.txt",text_Zipf)
    writeTextToFile("UnifCreatedText.txt",text_Unif)
    
    #--------------------------------------------------------------------------
    # Plots for Rank Frequency STARTS
    #--------------------------------------------------------------------------
    #Note: _S is for simple English 
    frequencyEachWord_S = collections.Counter(getSimpleEnglishText.split())\
                                                                .most_common()
    listForRankFrequencyDiag_S = [frequency for (word , frequency) \
                                                  in frequencyEachWord_S] 
    
    #Note _Z is for Zipf 
    frequencyEachWord_Z = collections.Counter(text_Zipf.split()).most_common()
    listForRankFrequencyDiag_Z = [frequency for (word , frequency) \
                                                  in frequencyEachWord_Z]  
    
    #Note_U is for Uniform
    frequencyEachWord_U = collections.Counter(text_Unif.split()).most_common()
    listForRankFrequencyDiag_U = [frequency for (word , frequency) \
                                                  in frequencyEachWord_U]
    
    drawPlot(listForRankFrequencyDiag_S , listForRankFrequencyDiag_Z, \
             listForRankFrequencyDiag_U, "x = Rank" , "y = Number of occurences") 
    #--------------------------------------------------------------------------
    # Plots for Rank Frequency ENDS
    #--------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------
    # Plots for Rank and CDF STARTS
    #--------------------------------------------------------------------------
     
    drawCDFPlot(associatedCDF_S , associatedCDF_NewZipf, associatedCDF_NewUnif,\
                                        "x = Rank" , "y = Cumulative Frequency") 
   
    #--------------------------------------------------------------------------
    # Plots for Rank and CDF ENDS
    #--------------------------------------------------------------------------
    
    # Now we perform Kolmogorov Smirnov test  by calculating the maximum 
    # pointwise distance of CDFs
    maxPointWiseD_S_Zipf = performKolmogorovSmirnovTest(associatedCDF_S , \
                                                        associatedCDF_NewZipf)
    maxPointWiseD_S_Unif = performKolmogorovSmirnovTest(associatedCDF_S , \
                                                        associatedCDF_NewUnif)
    print ("Obtained Maximum Pointwise Distance between simple English \
                                       and Zipf is : " , maxPointWiseD_S_Zipf)
    print ("Obtained Maximum Pointwise Distance between simple English \
                                       and Unif is : " , maxPointWiseD_S_Unif)

if __name__ == "__main__":
    simpleEnglishFilename = "simple-20160801-1-article-per-line"
    probabilitiesFilename = "probabilities.py.txt"
    # Here we calculate the total characters in Simple English and 
    # assign global variable 
    counterAllCharInEnglish = getCharactersInSimpleEnglish(simpleEnglishFilename)
    print ("TotalChracters: " ,counterAllCharInEnglish)
    mainFunction(simpleEnglishFilename ,probabilitiesFilename ) 
    
    
 