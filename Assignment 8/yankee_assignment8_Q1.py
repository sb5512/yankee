#NOTE: This python file creates necessary files with calculated 
# values required for cosine and jackard and statistical measure 
# calculation. These files saved heryby will be loaded in next .py file.

import pandas as pd
import itertools
from collections import Counter
import math
import pickle

articles_with_totalwords = {}
articles_list_ofwords = {}
articles_list_ofoutlinks = {}
tf_idf_article_eachterm = {}


# tf_dict has id as article and value = dictionary of each term with associated 
# term frequency in that document. 
def tf_idf_cal(tf_dict , df_dict):  
    global  tf_idf_article_eachterm
    tf_idf_article_eachterm = {}    
    total_document_length = len(tf_dict.keys())
    for each_article in tf_dict:
        tf_idf = {}
        for each_term in tf_dict[each_article]:
            tf_idf[each_term]= tf_dict[each_article][each_term] * \
                        math.log(total_document_length / df_dict[each_term],10)
        tf_idf_article_eachterm[each_article] = tf_idf
          
        
# returns the dictionary of term frequency  
def count_term_frequency_each_article(dict_df1):
   global articles_with_totalwords
   global articles_list_ofwords
   df1_withtermfrequency_eacharticle = {}
   for article_name in dict_df1.keys():
       list_words = dict_df1[article_name][0].split()
       articles_list_ofwords[article_name] = list_words
       articles_with_totalwords[article_name] = len(list_words)
       df1_withtermfrequency_eacharticle[article_name] = \
                 dict(Counter(dict_df1[article_name][0].split()).most_common())
   return df1_withtermfrequency_eacharticle
   

# updates the unique_term_dict value which contains the all unique terms 
# by document frequency for given terms and dataframe
def count_document_frequency_for_eachterm(df1 ,unique_terms_dict ):   
   document_frequency_for_eachterm_dic = {}
   copyDF = df1.copy()
   copyDF['wordset']= copyDF.text.map(lambda x: set(x.lower().split()))
   for eacharticleterms in copyDF['wordset']:
        for eachterm in eacharticleterms:
            if eachterm in document_frequency_for_eachterm_dic:
                num=document_frequency_for_eachterm_dic[eachterm]+1
            else:
                num=1
            document_frequency_for_eachterm_dic[eachterm] = num
   return document_frequency_for_eachterm_dic

# Responsible for reading articles from file and evaluating tfIDF , creating 
# dictionary of list of words per article and dictionry of article and len words
def read_articles_from_file_evaluate_tfidf(filename):
   global all_terms_basevector_dict
   global articles_list_ofoutlinks
   store = pd.HDFStore(filename)#read .h5 file 
   df1=store['df1']
   df2=store['df2']
   df1["text"] = df1.text.str.lower()    
   
   # Dictionary of article names and its associated article text in list form
   dict_df1 = df1.set_index('name').T.to_dict('list')
   dict_df2 = df2.set_index('name').T.to_dict()
   articles_list_ofoutlinks = dict_df2
   
   # get the term frequency for each article given the dictionary of datas
   articles_with_termfrequency_dict = count_term_frequency_each_article(dict_df1)
   
   # now we get document frequency . first get all terms and put in the set
   all_terms = list(itertools.chain.from_iterable([list(\
                    term_frequency_dict.keys()) for term_frequency_dict \
                                in articles_with_termfrequency_dict.values()]))
   unique_terms_dict = {each_term : 0 for each_term in all_terms}

   document_frequency_for_eachterm_diction = \
                  count_document_frequency_for_eachterm(df1, unique_terms_dict) 
  
   # Evaluate tfidf for each term in articles. Stored in dictionary
   tf_idf_cal(articles_with_termfrequency_dict , \
                                       document_frequency_for_eachterm_diction)
   
  
if __name__ == "__main__":    
    # Here we read articles from file, create base vectors, calculate tfidf, 
    # calculate document vectors and store all in global variable    
    read_articles_from_file_evaluate_tfidf("store.h5")
    
    # Save  ariticletotalwords, tfidfforeachterm , articles with outlinks
    # and articles with its words into a pickle file.
    try:    
        pickle.dump( articles_with_totalwords, open( \
                                            "articles_with_totalwords.p","wb"))
        pickle.dump( tf_idf_article_eachterm, open( \
                                             "tf_idf_article_eachterm.p","wb"))
        pickle.dump( articles_list_ofwords, open( \
                                               "articles_list_ofwords.p","wb"))
        pickle.dump( articles_list_ofoutlinks, open( \
                    "articles_list_ofoutlinks.p","wb"))
    except Exception as e:
        print("ERROR: Failed to save to a file")
        import sys
        sys.exit(1)    
    



