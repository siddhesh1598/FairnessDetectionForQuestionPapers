import pickle
from nltk import word_tokenize
import nltk
import re

from util.config import *


class BloomsTaxonomy:

    def __init__(self, question_paper_df):
        self.question_paper_df = question_paper_df


    def getBloomTagged(self):
        
        bloom_tagged = []
        with open(BLOOM_TAGS_PATH, 'rb') as handle:
            bloom_tags = pickle.load(handle)
        
        
        default_tagger = nltk.DefaultTagger('out')
        tagger = nltk.tag.UnigramTagger(model=bloom_tags, 
            backoff=default_tagger)
        
        for s in self.question_paper_df['Question']:
            #Remove punctuations
            s = re.sub('[^a-zA-Z]', ' ', s)

            #Convert to lowercase
            s = s.lower()

            #remove tags
            s=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",s)

            # remove special characters and digits
            s=re.sub("(\\d|\\W)+"," ",s)
            tokenized = word_tokenize(s) 

            tagged = tagger.tag(tokenized)

            final = []
            for ele in tagged:
                if not ele[1] == 'out':
                    final.append(ele)
            bloom_tagged.append(final)
            
        self.question_paper_df['Bloom\'s Verbs'] = bloom_tagged
        
        return self.question_paper_df


    def calculateBloomScore(self): 

        bloom_tagged = self.question_paper_df['Bloom\'s Verbs']
        new = []
        final_score = []
        
        for i in bloom_tagged:
            l = []
            if len(i):
                for j in i:
                    l.append(j[1])
            
            new.append(l)
            
        for x in new:
            score = 0
            if len(x):
                for level in x:
                    if level == 'remember':
                        score += 1/21
                    if level == 'understand':
                        score += 2/21
                    if level == 'apply':
                        score += 3/21
                    if level == 'analyze':
                        score += 4/21
                    if level == 'evaluate':
                        score += 5/21
                    if level == 'create':
                        score += 6/21
            else:
                score += 1/21
                
            final_score.append(score)
            
        self.question_paper_df["Bloom's Score"] = final_score

        return round(self.question_paper_df['Bloom\'s Score'].sum()/len(self.question_paper_df) *100, 2)


    def getQuestionPaper(self):
        return self.question_paper_df
