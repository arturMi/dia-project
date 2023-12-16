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


# Function to calculate similarities between blocks in two dictionaries
def calculate_similarities_between_data(dict_or_dataframe_one, dict_or_dataframe_one_two, threshold=0.9, column_name='Title'):
    if isinstance(dict_or_dataframe_one, dict) and isinstance(dict_or_dataframe_one_two, dict):
        similarities = []
        
        for block_name_one, dataframe_one in dict_or_dataframe_one.items():
            if isinstance(dataframe_one, pd.DataFrame):
                for block_name_two, dataframe_two in dict_or_dataframe_one_two.items():
                    if isinstance(dataframe_two, pd.DataFrame):
                        for idx1, row1 in dataframe_one.iterrows():
                            for idx2, row2 in dataframe_two.iterrows():
                                sim = jaccard_similarity(tokenize(row1[column_name]), tokenize(row2[column_name]))
                                if sim >= threshold:
                                    similarities.append({'Block1': block_name_one, 'Block2': block_name_two, 'Similarity': sim})
                    else:
                        raise ValueError(f"Value for '{block_name_two}' in dict_two is not a DataFrame.")
            else:
                raise ValueError(f"Value for '{block_name_one}' in dict_one is not a DataFrame.")
            
    elif isinstance(dict_or_dataframe_one, pd.DataFrame) and isinstance(dict_or_dataframe_one_two, pd.DataFrame):
        # If both arguments are DataFrames, proceed with similarity calculations
        similarities = []
        for idx1, row1 in dataframe_one.iterrows():
            for idx2, row2 in dataframe_two.iterrows():
                sim = jaccard_similarity(tokenize(row1[column_name]), tokenize(row2[column_name]))
                if sim >= threshold:
                    similarities.append({'ACM_Entry': idx1, 'DBLP_Entry': idx2, 'Similarity': sim})

        df = pd.DataFrame(similarities)

        return df.to_csv(f'./data/Matched_Entities_DF.csv', index=False)
    else:
        # Handle cases where inputs are not dictionaries or DataFrames
        raise ValueError("Inputs should be two dataframes dictionaries of blocks.")

