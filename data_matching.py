import nltk
import pandas as pd
from multiprocessing import Pool

nltk.download('punkt')

def create_year_blocks(dataframe, year_ranges):
    # Sort the DataFrame by the 'Year' column
    dataframe = dataframe.sort_values(by='year')
    
    blocks = {}
    for i, (start, end) in enumerate(year_ranges):
        block_name = f'Block_{i+1}'
        blocks[block_name] = dataframe[(dataframe['year'] >= start) & (dataframe['year'] <= end)]
    
    return blocks

# Tokenization function
def tokenize(text):
    if isinstance(text, str):  
        return set(nltk.word_tokenize(text.upper()))
    else:
        return set()

def jaccard_similarity(list1, list2):
    s1 = set(map(str.upper, list1))
    s2 = set(map(str.upper, list2))
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

def trigram_similarity(str1, str2):
    trigrams_str1 = set(nltk.ngrams(str1, 3))
    trigrams_str2 = set(nltk.ngrams(str2, 3))
    
    # Calculate Jaccard similarity between trigrams
    intersection = len(trigrams_str1.intersection(trigrams_str2))
    union = len(trigrams_str1.union(trigrams_str2))
    
    return intersection / union if union != 0 else 0

def compare_blocks(df_one, df_two, measure, threshold, column_name):
    similarities = []
    for idx1, row1 in df_one.iterrows():
        for idx2, row2 in df_two.iterrows():
            if measure == 'jaccard':
                sim = jaccard_similarity(row1[column_name], row2[column_name])
            elif measure == 'trigram':
                sim = trigram_similarity(tokenize(row1[column_name]), tokenize(row2[column_name]))
            if sim >= threshold:
                similarities.append({'idDBLP': row1['id'], 'idACM': row2['id'], 'Similarity': sim})
    return similarities