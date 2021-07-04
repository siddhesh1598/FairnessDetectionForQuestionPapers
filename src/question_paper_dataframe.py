import re
import nltk
# nltk.download()
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd

from util.config import *


def createQuestionPaperDF(question_paper, subject):

    # calculate total marks
    question_paper_df = pd.read_csv(question_paper, header=None)    
    question_paper_df.rename(columns={0:'Num', 1:'Question', 2:'Marks'}, inplace=True)
    
    total_marks = int(question_paper_df['Marks'].sum())
    
    # set stop words
    stop_words = set(stopwords.words("english")).union(additional_words)
    
    keywords = []
    
    for i in range(len(question_paper_df)):
        
        # remove punctuations
        text = re.sub('[^a-zA-Z0-9]', ' ', question_paper_df['Question'][i])
        
        # convert to lowercase
        text = text.lower()
        
        #remove tags
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
        
        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)
        
        # Lemmatizer
        text = text.split()
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in stop_words]
        text = ' '.join(text)
        
        keywords.append(text)
       
    # removing repeated words
    final_keywords = []
    
    for i in keywords:
        l = i.split()
        k = [] 
        for x in l:   
            if i.count(x) > 1 and (x not in k) or i.count(x) == 1: 
                k.append(x) 
        t = ' '.join(k)
        final_keywords.append(t)
        
    question_paper_df['Extracted Keywords'] = final_keywords
    
    return total_marks, question_paper_df