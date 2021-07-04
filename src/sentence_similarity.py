# import
import scipy

from sentence_transformers import SentenceTransformer
from util.config import *


def getPrevQuestionsEmbeddings(model):
    
    # Extract question from the text file.
    prev_questions = []

    with open(PREV_QUESTIONS_PATH, "r", encoding='utf-8-sig') as questions:
        for question in questions:
            if question[0] != "#":
                prev_questions.append(question.strip("\n"))
    
    # Each sentence is encoded as a 1-D vector with 768 columns
    prev_questions_embeddings = model.encode(prev_questions) 

    return prev_questions_embeddings


def getSimilarityScore(question_paper_df, num_matches):
    model = SentenceTransformer('bert-base-nli-stsb-mean-tokens')
    prev_questions_embeddings = getPrevQuestionsEmbeddings(model)

    questions = question_paper_df['Question']

    # Each sentence is encoded as a 1-D vector with 768 columns
    questions_embeddings = model.encode(questions)

    similarity_score = 0

    for query, query_embedding in zip(questions, prev_questions_embeddings):
        distances = scipy.spatial.distance.cdist([questions_embeddings], 
            prev_questions_embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])

        print("\n\n======================\n\n")
        print("Query:", query)
        print("\nTop {} most similar sentences in corpus:".format(num_matches))

        indiv_score = 0
        for idx, distance in results[0:num_matches]:
            indiv_score += 1 - distance
            # print("[Cosine Score: {:.4f}]".format(1-distance), questions[idx].strip())

        similarity_score += round(indiv_score / num_matches, 2)
    
    return round(similarity_score / len(question_paper_df), 2)