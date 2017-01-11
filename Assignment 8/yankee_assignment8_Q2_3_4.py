# NOTE Please run the yankee_assignment8_Q1.py to get the necessary files
# before running this file else Error in loading file will occur.

import pickle
import numpy as np
import random
from collections import Counter
import operator
import math
import pandas as pd
import matplotlib.pyplot as plt

from_file_articles_with_totalwords = {}
from_file_articles_list_ofwords = {}
from_file_tf_idf_article_eachterm = {}
from_file_articles_list_ofoutlinks = {}

def calculateCosineSimilarity(article1, article2):
    try:
        tf_idf_article1 = from_file_tf_idf_article_eachterm[article1]
        tf_idf_article2 = from_file_tf_idf_article_eachterm[article2]

        scalar_product_article1_article2 = 0
        for each_term_article1 in tf_idf_article1:
            if each_term_article1 in tf_idf_article2.keys():
                scalar_product_article1_article2 = \
                                scalar_product_article1_article2 +  \
                                (tf_idf_article1[each_term_article1] * \
                                          tf_idf_article2[each_term_article1])
    
        euc_dist_tfIdfDict1 = np.sum(np.square(list(tf_idf_article1.values())))
        euc_dist_tfIdfDict2 = np.sum(np.square(list(tf_idf_article2.values())))
        
        cosineSimilarity = scalar_product_article1_article2 / \
                                    (euc_dist_tfIdfDict1 * euc_dist_tfIdfDict2)
        
    except Exception as e:
        print("ERROR: Failed to get article for calculating Cosine")
        import sys
        sys.exit(1)
    return cosineSimilarity   

def calcJaccardSimilarity(article1, article2):
    wordset1 = from_file_articles_list_ofwords[article1]
    wordset2 = from_file_articles_list_ofwords[article2]
    wordset1=set(wordset1)
    wordset2=set(wordset2)
    inter=wordset1.intersection(wordset2)
    union=wordset1.union(wordset2)
    if (len(union) > 0 ):
        jc=(len(inter)/len(union))
    else:
        jc = 1
    return jc
   
def calcJaccardGraphSimilarity(article1, article2):
    wordset1 = from_file_articles_list_ofoutlinks[article1]["out_links"]
    wordset2 = from_file_articles_list_ofoutlinks[article2]["out_links"]
    wordset1=set(wordset1)
    wordset2=set(wordset2)
    inter=wordset1.intersection(wordset2)
    union=wordset1.union(wordset2)
    if (len(union) > 0 ):
        jc=(len(inter)/len(union))
    else:
        jc = 1
    return jc

    

def initialise_loading():
    global from_file_articles_with_totalwords
    global from_file_articles_list_ofwords
    global from_file_tf_idf_article_eachterm
    global from_file_articles_list_ofoutlinks 
    
    # Lets load all necessary already calculated values
    try:    
        
        from_file_articles_with_totalwords = pickle.load(open\
                                          ( "articles_with_totalwords.p","rb"))
        from_file_tf_idf_article_eachterm = pickle.load(open\
                                        ( "tf_idf_article_eachterm.p","rb"))
        from_file_articles_list_ofwords = pickle.load(open\
                                             ( "articles_list_ofwords.p","rb"))
        from_file_articles_list_ofoutlinks = pickle.load(open\
                                          ( "articles_list_ofoutlinks.p","rb"))
    except Exception as e:
        print("ERROR: Failed to load from file")
        import sys
        sys.exit(1)    
    
  
    
    
    
#------------------------------------------------------------------------------
# Begins Experiment for 1.3 and 1.4
#------------------------------------------------------------------------------

def longest_article(how_many):
    article_in_order = Counter(from_file_articles_with_totalwords).most_common()
    if (len(article_in_order) <= how_many):
        return [article for (article , numberofwords) in article_in_order]
    allarticles = [article for (article , numberofwords) in article_in_order]
    return allarticles[:how_many]

def random_articles(how_many):
    if (len(from_file_articles_with_totalwords) <= how_many):
        return random.sample(from_file_articles_with_totalwords.keys(),len(\
                                          from_file_articles_with_totalwords))
    return random.sample(from_file_articles_with_totalwords.keys(),how_many)    

def giverankto_tuplelist(tuple_list):    
    i = 1
    ranking_tuple = {}
    for (key , val) in tuple_list:
        ranking_tuple[key] = i
        i = i + 1
    return ranking_tuple
    

def calculate_statistical_significance(ranked_column):
    C = [sum(i > val for i in ranked_column[idx + 1:]) for idx, val in \
                                                     enumerate(ranked_column)]
    try:
        C.pop()
    except:
        print("No elements to get the Statistic measure\n")
    
        
    D = [sum(i < val for i in ranked_column[idx + 1:]) for idx, val in \
                                                      enumerate(ranked_column)]
    try:
        D.pop()
    except:
        print("No elements to get the Statistic measure\n")    
    
    kendalls_tau = (sum(C) - sum(D)) / (sum(C) + sum(D)) 
    
    n = len(ranked_column)
    statistical_significance_Z = (3 * kendalls_tau * math.sqrt(n * (n - 1))) / \
                                                         math.sqrt(2 * (2*n+5)) 
    
    #Note Any Z value greater than 1.96 is going to statistically significant. 
    return statistical_significance_Z

    
# Cosine vs Jacakard
def get_statistical_significance_cosine_jacakard(firstArticle , \
                                                      remainingArticles_list):
    col1_from_cosine_firstcompared_toothers = {remainingArticles_list[i]: \
           calculateCosineSimilarity(firstArticle , remainingArticles_list[i])\
                                                        for i in range (0,100)}    
    sorted_cosine = sorted(col1_from_cosine_firstcompared_toothers.items(), \
                           key=operator.itemgetter(1) , reverse=True) 
    ranked_cosine_dict = giverankto_tuplelist(sorted_cosine)
    
    
    col2_from_jackard_firstcompared_toothers = {remainingArticles_list[i]: \
           calcJaccardSimilarity(firstArticle , remainingArticles_list[i]) \
                                                        for i in range (0,100)}
    sorted_jacard = sorted(col2_from_jackard_firstcompared_toothers.items(), \
                           key=operator.itemgetter(1) , reverse=True)
    ranked_jacard_column = [ranked_cosine_dict[term] for (term , value) \
                                                              in sorted_jacard]
    return calculate_statistical_significance(ranked_jacard_column)

#Cosine vs Jackard with outlinks - Graphs
def get_statistical_significance_cosine_jacakardGraph(firstArticle , \
                                                      remainingArticles_list):
    col1_from_cosine_firstcompared_toothers = {remainingArticles_list[i]: \
        calculateCosineSimilarity(firstArticle , remainingArticles_list[i]) \
                                                       for i in range (0,100)}    
    sorted_cosine = sorted(col1_from_cosine_firstcompared_toothers.items(), \
                                     key=operator.itemgetter(1) , reverse=True) 
    ranked_cosine_dict = giverankto_tuplelist(sorted_cosine)
    
    
    col2_from_jackardGraph_firstcompared_toothers = {remainingArticles_list[i]:\
        calcJaccardGraphSimilarity(firstArticle , remainingArticles_list[i]) \
                                                        for i in range (0,100)}
    sorted_jacard = sorted(col2_from_jackardGraph_firstcompared_toothers.items(),\
                                     key=operator.itemgetter(1) , reverse=True)
    ranked_jacard_column = [ranked_cosine_dict[term] for (term , value) in \
                                                                sorted_jacard]
    return calculate_statistical_significance(ranked_jacard_column)

    
# Jackard vs Jackard with outlinks - Graphs
def get_statistical_significance_jacakard_jacakardGraph(firstArticle , \
                                                        remainingArticles_list):
    col1_from_cosine_firstcompared_toothers = {remainingArticles_list[i]: \
               calcJaccardSimilarity(firstArticle , remainingArticles_list[i])\
                                                        for i in range (0,100)}    
    sorted_cosine = sorted(col1_from_cosine_firstcompared_toothers.items(), \
                                     key=operator.itemgetter(1) , reverse=True) 
    ranked_cosine_dict = giverankto_tuplelist(sorted_cosine)
    
    
    col2_from_jackardGraph_firstcompared_toothers = {remainingArticles_list[i]:\
           calcJaccardGraphSimilarity(firstArticle , remainingArticles_list[i])\
                                                        for i in range (0,100)}
    sorted_jacard = sorted(col2_from_jackardGraph_firstcompared_toothers.items(),\
                                     key=operator.itemgetter(1) , reverse=True)
    ranked_jacard_column = [ranked_cosine_dict[term] for (term , value) in \
                                                                 sorted_jacard]
    return calculate_statistical_significance(ranked_jacard_column)

    
# We will evaluate each pair and do the plot by measuring whish was more 
# significant compared to each other via frequency plot
def performStatistical_significance_and_plot(type_of_article_random_or_longest):
    cosine_jackard_dict = {}
    cosine_jackard_graph_dict = {}
    jackard_jackard_graph_dict = {}
    for article in type_of_article_random_or_longest:
        temp = type_of_article_random_or_longest[:]
        temp.remove(article)
        cosine_jackard_dict[article] =  \
                   get_statistical_significance_cosine_jacakard(article , temp) 
        cosine_jackard_graph_dict[article] =  \
              get_statistical_significance_cosine_jacakardGraph(article , temp)
        jackard_jackard_graph_dict[article] =  \
            get_statistical_significance_jacakard_jacakardGraph(article , temp)
        
        
    # -----------------------------------------------------------------------------
    # Counting the total significance for each pair and plotting    
    Cosine_JackardDict = (list(cosine_jackard_dict.values()))
    Cosine_JackardGraphDict = (list(cosine_jackard_graph_dict.values()))                           
    Jackard_JackardGraphDict = (list(jackard_jackard_graph_dict.values()))
    
    df = pd.DataFrame(
        {'Cosine_Jackard': Cosine_JackardDict,
         'Cosine_JackardGraph': Cosine_JackardGraphDict,
         'Jackard_JackardGraph': Jackard_JackardGraphDict
        })
    df_seperated = pd.DataFrame({'Insignificant' : df[df<= 1.96].count(),
         'Significant' : df[df > 1.96].count()})
    df_seperated.plot(kind='bar')
    plt.ylabel("Frequency")
    plt.show()

       
if __name__ == "__main__":     
    
    initialise_loading()     
    print("\n Jaccard Similarity between two articles Germany and Europe is: \n"\
                                 , calcJaccardSimilarity("Germany" , "Europe" ))
    print("\n Cosine Similarity between two articles Germany and Europe is: \n"\
                            , calculateCosineSimilarity("Germany" , "Europe" ))
    print("\n Jacard with Graph Similarity between two articles Germany and " + \
             "Europe is: \n" , calcJaccardGraphSimilarity("Germany" , "Europe"))
    
    #--------------------------------------------------------------------------
    # Answer 1.4 Performing Experiment and testing with plots
    #--------------------------------------------------------------------------
    
    # Here I will have to get hundred Longest and random Article comparisons
    hundredlongestArticle = longest_article(101)
    randomarticles = random_articles(101)
    
    performStatistical_significance_and_plot(hundredlongestArticle)
    performStatistical_significance_and_plot(randomarticles)
    
    
    #time calculations
    print ("Total documents in our dataset : " , \
                         len(from_file_articles_with_totalwords.keys()))
    
    import timeit
    
    def _template_func(setup, func):
        """Create a timer function. Used if the "statement" is a callable."""
        def inner(_it, _timer, _func=func):
            setup()
            _t0 = _timer()
            for _i in _it:
                retval = _func()
            _t1 = _timer()
            return _t1 - _t0, retval
        return inner
    
    timeit._template_func = _template_func
    
    def foo():
        return calculateCosineSimilarity("Germany" , "Europe")
    
    t = timeit.Timer(foo)
    print("Time in seconds for evaluating Cosine Similarity : " \
                                                   , t.timeit(number=1))
    

    