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

def trigram_similarity(str1, str2):
    trigrams_str1 = set(nltk.ngrams(str1, 3))
    trigrams_str2 = set(nltk.ngrams(str2, 3))
    
    # Calculate Jaccard similarity between trigrams
    intersection = len(trigrams_str1.intersection(trigrams_str2))
    union = len(trigrams_str1.union(trigrams_str2))
    
    return intersection / union if union != 0 else 0

# Function to calculate similarities between blocks in two dictionaries or DataFrames
def calculate_similarities_between_data(dict_or_dataframe_one, dict_or_dataframe_two, measure='jaccard', threshold=0.75, column_name='Title'):
    if isinstance(dict_or_dataframe_one, dict) and isinstance(dict_or_dataframe_two, dict):
        similarities = []
        
        for block_name_one, dataframe_one in dict_or_dataframe_one.items():
            if isinstance(dataframe_one, pd.DataFrame):
                for block_name_two, dataframe_two in dict_or_dataframe_two.items():
                    if isinstance(dataframe_two, pd.DataFrame):
                        for idx1, row1 in dataframe_one.iterrows():
                            for idx2, row2 in dataframe_two.iterrows():
                                if measure == 'jaccard':
                                    sim = jaccard_similarity(tokenize(row1[column_name]), tokenize(row2[column_name]))
                                if measure == 'trigram':
                                    sim = trigram_similarity(row1[column_name], row2[column_name])
                                if sim >= threshold:
                                    similarities.append({'idDBLP': row1['id'], 'idACM': row2['id'], 'Similarity': sim})
                    else:
                        raise ValueError(f"Value for '{block_name_two}' in dict_or_dataframe_two is not a DataFrame.")
            else:
                raise ValueError(f"Value for '{block_name_one}' in dict_or_dataframe_one is not a DataFrame.")
        
        df = pd.DataFrame(similarities)
        df.to_csv(f'./data/Matched_Entities_Blocks{measure}.csv', index=False)
        return df

    elif isinstance(dict_or_dataframe_one, pd.DataFrame) and isinstance(dict_or_dataframe_two, pd.DataFrame):
        similarities = []
        for idx1, row1 in dict_or_dataframe_one.iterrows():
            for idx2, row2 in dict_or_dataframe_two.iterrows():
                if measure == 'jaccard':
                    sim = jaccard_similarity(tokenize(row1[column_name]), tokenize(row2[column_name]))
                if measure == 'trigram':
                    sim = trigram_similarity(row1[column_name], row2[column_name])
                if sim >= threshold:
                    similarities.append({'idDBLP': row1['id'], 'idACM': row2['id'], 'Similarity': sim})

        df = pd.DataFrame(similarities)
        df.to_csv(f'./data/Matched_Entities_DF{measure}.csv', index=False)
        return df

    else:
        raise ValueError("Inputs should be two dictionaries or two DataFrames.")


'''
# Function to calculate similarities between blocks in two dictionaries or DataFrames
def calculate_similarities_between_data(dict_or_dataframe_one, dict_or_dataframe_two, measure='jaccard', threshold=0.75, column_name='Title'):
    if isinstance(dict_or_dataframe_one, dict) and isinstance(dict_or_dataframe_two, dict):
        similarities = []
        
        for block_name_one, dataframe_one in dict_or_dataframe_one.items():
            if isinstance(dataframe_one, pd.DataFrame):
                for block_name_two, dataframe_two in dict_or_dataframe_two.items():
                    if isinstance(dataframe_two, pd.DataFrame):
                        for idx1, row1 in dataframe_one.iterrows():
                            for idx2, row2 in dataframe_two.iterrows():
                                if measure == 'jaccard':
                                    sim = jaccard_similarity(tokenize(row1[column_name]), tokenize(row2[column_name]))
                                if measure == 'trigram':
                                    sim = trigram_similarity(row1[column_name], row2[column_name])
                                if sim >= threshold:
                                    similarities.append({'DBLP_Entry': row1.to_dict(), 'ACM_Entry': row2.to_dict(), 'Similarity': sim})
                    else:
                        raise ValueError(f"Value for '{block_name_two}' in dict_or_dataframe_two is not a DataFrame.")
            else:
                raise ValueError(f"Value for '{block_name_one}' in dict_or_dataframe_one is not a DataFrame.")
        
        df = pd.DataFrame(similarities)
        df.to_csv(f'./data/Matched_Entities_Blocks{measure}.csv', index=False)
        return df

    elif isinstance(dict_or_dataframe_one, pd.DataFrame) and isinstance(dict_or_dataframe_two, pd.DataFrame):
        similarities = []
        for idx1, row1 in dict_or_dataframe_one.iterrows():
            for idx2, row2 in dict_or_dataframe_two.iterrows():
                if measure == 'jaccard':
                    sim = jaccard_similarity(tokenize(row1[column_name]), tokenize(row2[column_name]))
                if measure == 'trigram':
                    sim = trigram_similarity(row1[column_name], row2[column_name])
                if sim >= threshold:
                    similarities.append({'DBLP_Entry': row1.to_dict(), 'ACM_Entry': row2.to_dict(), 'Similarity': sim})

        df = pd.DataFrame(similarities)
        df.to_csv(f'./data/Matched_Entities_DF{measure}.csv', index=False)
        return df

    else:
        raise ValueError("Inputs should be two dictionaries or two DataFrames.")
'''

