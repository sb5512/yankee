#Code for implementing Sentiment observation in all articles 
#Also note you will have to download nltk packages online

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd

sentimentsEachArticles = []
neutralSentimentList = []
positiveSentimentList = []
negativeSentimentList = []

def getSentimentOptimal(textToFindSentimentOf):
    #initialise the SentimentAnalyszer
    sid = SentimentIntensityAnalyzer()    
    ss = sid.polarity_scores(textToFindSentimentOf)
    
    # maximum value of all obtained sentiments
    maxValueKey =  max(ss.keys(), key=(lambda key: ss[key]))
    if ss[maxValueKey] <= 0.0 :
        return None
    return maxValueKey

# We give a sentence and get the noun or verb or adjective from the sentence
def getRelevantWordForSentimentEvaluation(sentence):
    perSentenceWords = nltk.word_tokenize(sentence)
    # Here we get the grammarType for each words we splitted from the sentence.
    getGrammarTypeOfEachWord = nltk.pos_tag(perSentenceWords)
    print (getGrammarTypeOfEachWord)
    
    #Here we convert to dictionary inorder to obtain the appropriate word for 
    #testing.
    grammarTypeReversed = [(b,a) for (a,b) in getGrammarTypeOfEachWord] 
    grammarTypeReversed = dict(grammarTypeReversed)  
      
    try:
        try: 
            try: 
                try: 
                    try:
                        try: 
                            try:
                                try:
                                    try:
                                        value = grammarTypeReversed['NNS']
                                    except:
                                        value = grammarTypeReversed['NNPS']
                                except:
                                    value = grammarTypeReversed['NN']
                            except:
                                value = grammarTypeReversed['NNP']
                        except:
                            value = grammarTypeReversed['NNS']
                    except:
                        value = grammarTypeReversed['RB']
                except:
                    value = grammarTypeReversed['RBR']
            except:
                value = grammarTypeReversed['RBS']
        except:
            value = grammarTypeReversed['RP']
    except:
        try:
            value = next (iter (dict.values(grammarTypeReversed)))
        except:
            value = None
    return value



def drawHistogram(listElements , xLabel , yLabel, interval):
    x_1 = np.array(listElements)
    plt.figure(figsize=(12,9))
    plt.hist(x_1 , bins= range(0, 100 + interval, interval) , color='c' )
    plt.xlabel(xLabel)
    plt.ylabel(yLabel) 
    plt.yscale('log')
    plt.axvline(x_1.mean(), color='b', linestyle='dashed', linewidth=2 , \
                                        label="mean = " + str(np.mean(x_1)))
    plt.axvline(np.median(x_1), color='r', linestyle='dashed', linewidth=2 , \
                                    label = "median = " + str(np.median(x_1)))
     
    plt.legend(loc='upper right')  
    plt.show()
    

def drawCDF(listElements , xLabel , yLabel, interval):
    x_1 = np.array(listElements)
    plt.figure(figsize=(12,9))
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)	
    plt.axvline(x_1.mean(), color='black', linestyle='dashed', linewidth=2 ,\
                                        label="mean = " + str(np.mean(x_1)))
    plt.axvline(np.median(x_1), color='r', linestyle='dashed', linewidth=2 ,\
                                    label = "median = " + str(np.median(x_1)))
    
    n, bins, patches = plt.hist(x_1, bins= range(0, 90, interval), normed=1,
                            histtype='step', cumulative=True)
       
    plt.ylim(0, 1.2)
    plt.title('cumulative step')
    plt.legend(loc='upper top')
    
    plt.show()
    
#Parses the file
def getEachLinesFromFile(filename):
    #fname = "simple-20160801-1-article-per-line1.txt"
    with open(filename , encoding="utf8") as fp:
        try:
            content = fp.readlines()
        except:
            content = ""
    return content
    

#Takes filename and starts the process for sentiment observation in that file
def mainFunction(filename):   
    # Here we load tokenizers from nltk and obtain sentences.
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    content = getEachLinesFromFile(filename)
    
    #Obtain each articles i.e. each line 
    listOfSentencesFromArticles = [tokenizer.tokenize(eachArticle) for \
                                   eachArticle in content]
    
    for sentencesForSentiment in listOfSentencesFromArticles:
        neutralSentiments = 0
        negativeSentiments = 0
        positiveSentiments = 0
        for eachSentence in sentencesForSentiment:
            demoKolagi = eachSentence
            
            #get Sentiment calculated for eachSentence
            sentiment = getSentimentOptimal(demoKolagi)
            if sentiment is not None:
                if sentiment.lower() == "neu":
                    neutralSentiments = neutralSentiments + 1
                if sentiment.lower() == "neg":
                    negativeSentiments = negativeSentiments + 1
                if sentiment.lower() == "pos":
                    positiveSentiments = positiveSentiments + 1
                if sentiment.lower() == "compound":
                    positiveSentiments = positiveSentiments + 1
        
        neutralSentimentList.append(neutralSentiments)
        negativeSentimentList.append(negativeSentiments)
        positiveSentimentList.append(positiveSentiments)
        
        articleSentimentsDict = {}
        articleSentimentsDict["Neutral"] = neutralSentiments
        articleSentimentsDict["Positive"] = positiveSentiments
        articleSentimentsDict["Negative"] = negativeSentiments
        sentimentsEachArticles.append(articleSentimentsDict)
    
    
    
if __name__ == "__main__":
    filename = "simple-20160801-1-article-per-line2.txt"
    mainFunction(filename)   
    print("\n Each articles has : " , sentimentsEachArticles) 
    print ("\n Each articles has This neutral : " , neutralSentimentList)
    
    print ("\n Each articles has This positive : " , positiveSentimentList)
    
    print ("\n Each articles has This negative : " , negativeSentimentList)
    sumNegativePositiveSentimentList = [x + y for x, y in zip(\
                                positiveSentimentList, negativeSentimentList)]
    
    drawHistogram(neutralSentimentList , "Number of Neutral sentiment sentences\
                      per article" , "Number of articles - Frequencies" , 10) 
    drawCDF(neutralSentimentList , "Number of Neutral sentiment sentences per \
                                                        article" , "CDF " , 5) 
   
    drawHistogram(sumNegativePositiveSentimentList , "Number of Positive plus \
                                    Negative sentiment sentences per article" ,\
                                    "Number of articles - Frequencies" , 5) 
    drawCDF(sumNegativePositiveSentimentList , "Number of Positive plus \
                        Negative sentiment sentences per article" , "CDF " , 1) 
  














df1 = pd.DataFrame(index=range(len(neutralSentimentList)), columns=["No. of Neutral Sentiment Sentences" , \
                                       "No. of Negative Sentiment Sentences",\
                                       "No. of Positive Sentiment Sentences Articles"])
df1["No. of Neutral Sentiment Sentences"] = neutralSentimentList
df1["No. of Negative Sentiment Sentences"] = negativeSentimentList
df1["No. of Positive Sentiment Sentences Articles"] = positiveSentimentList
print(df1)





  

