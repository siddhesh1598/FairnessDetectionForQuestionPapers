# import
import os

from src.question_paper_dataframe import *
from src.knowledge_graph import *
from src.blooms_taxonomy import *
from src.sentence_similarity import *
from util.config import *


# get paths to question paper and syllabus
subject = input('Select subject name (aoa,ds,mcc,chemtech,testing): ')

question_paper = os.path.sep.join([SUBJECT_DIR, subject + ".txt"])
syllabus = os.path.sep.join([SUBJECT_DIR, subject + ".txt"])


"""### Call question paper related functions
Output will be Question Paper DataFrame with Extracted Keywords
"""

total_marks, question_paper_df = createQuestionPaperDF(question_paper, subject)


"""### Give syllabus csv and Create Graph"""
syllabusKG = SyllabusKG(syllabus, subject, total_marks)
try:
    syllabus_graph = syllabusKG.importGraph()
except:
    syllabus_graph = syllabusKG.buildKnowledgeGraph()

"""### Parse Qestion paper dataframe through graph and identify syllabus nodes
Output will be DataFrame with identified nodes
"""

question_paper_df = syllabusKG.parse(question_paper_df)

"""## Extraction of Bloom verbs from questions
Output will be dataframe containing extracted Bloom's verbs
"""

bloomstaxonomy = BloomsTaxonomy(question_paper_df)
bloomstaxonomy.getBloomTagged()

"""## Calculate Syllabus Fairness Score and Bloom's Taxanomy Score based on identified nodes and extracted bloom's verbs"""

print("Syllabus Fairness Score: " + str(syllabusKG.getResult()))
print("Bloom's Taxonomy Score: " + str(bloomstaxonomy.calculateBloomScore()))
print("Similarity Score: " + str(getSimilarityScore(question_paper_df)))

"""### Bloom's Score per question on 0 to 1 scale"""

question_paper_df = bloomstaxonomy.getQuestionPaper()
question_paper_df
