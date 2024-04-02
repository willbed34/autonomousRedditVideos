import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def extract_keywords_from_title(title):
    # Remove variants of "ELI5"
    title = re.sub(r'\b(eli5|ELI5|explain\s+like\s+i\'?m\s+5)\b', '', title)

    # Tokenize the modified title into words
    words = word_tokenize(title)

    # Filter out stopwords (common words like 'the', 'is', 'and', etc.)
    filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]

    # Perform part-of-speech tagging to identify nouns, adjectives, etc.
    pos_tags = nltk.pos_tag(filtered_words)

    # Extract nouns and adjectives as keywords
    keywords = [word for word, pos in pos_tags if pos.startswith('NN') or pos.startswith('JJ')]

    # Join the keywords into a single string
    keyword_string = ' '.join(keywords)

    return keyword_string