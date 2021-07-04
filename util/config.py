# import
import os


# path to subject data
SUBJECT_DIR = "metadata"

# additional stop words
additional_words = [
    'operations', 'perform', 'implement', 
    'advantages', 'program', 'finding',
    'notation', 'complexity', 'analysis',
    'derive', 'find', 'define', 'prove',
    'concept', 'draw', 'apply', 'elements', 
    'computing', 'time', 'procedure', 'approach', 
    'different', 'solving', 'algorithms', 
    'strategy', 'programming', 'understand', 
    'note', 'detailed', 'solve', 'difference', 
    'determine', 'following', 'problem', 'in',
    'used', 'method', 'solution', 'algorithm',
    "write", "example", "obtain", "using", 
    "show", "result", "large", "also", "iv", 
    "one", "two", "new", "previously", "shown", 
    "explain","detail","compare","techniques"
]

# bloom tags path
BLOOM_TAGS_PATH = "metadata/bloom_tags.pickle"

# previous questions path
PREV_QUESTIONS_PATH = "metadata/aoa_prev_questions.txt"
