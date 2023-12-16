import pandas as pd
import nltk
nltk.download('punkt')

# Tokenization function
def tokenize(text):
    return set(nltk.word_tokenize(text.lower()))

# Calculate Jaccard similarity
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# Function to calculate similarities
def calculate_similarities(dataframe_one, dataframe_two, threshold=0.9, column_name='Title'):
    similarities = []
    for idx1, row1 in dataframe_one.iterrows():
        for idx2, row2 in dataframe_two.iterrows():
            sim = jaccard_similarity(tokenize(row1[column_name]), tokenize(row2[column_name]))
            if sim >= threshold:
                similarities.append({'ACM_Entry': idx1, 'DBLP_Entry': idx2, 'Similarity': sim})

    df = pd.DataFrame(similarities)

    return df.to_csv(f'./data/Matched Entities.csv', index=False)
