import nltk
import pandas as pd
import string

nltk.download('punkt')

def create_year_blocks(dataframe, year_ranges):
    # Sort the DataFrame by the 'Year' column
    dataframe = dataframe.sort_values(by='year')
    
    blocks = {}
    for i, (start, end) in enumerate(year_ranges):
        block_name = f'Block_{i+1}'
        blocks[block_name] = dataframe[(dataframe['year'] >= start) & (dataframe['year'] <= end)]
    
    return blocks

def tokenize(text):
    if isinstance(text, str):
        text = text.translate(str.maketrans("", "", string.punctuation))
        
        return set(nltk.word_tokenize(text.upper()))
    else:
        return set()

def jaccard_similarity(list1, list2):
    s1 = tokenize(list1)
    s2 = tokenize(list2)
    
    intersection_size = len(s1.intersection(s2))
    union_size = len(s1.union(s2))
    
    if union_size != 0:
        return float(intersection_size / union_size)
    else:
        return 0.0


def trigram_similarity(str1, str2):
    def get_trigrams(text):
        trigrams = set()
        # add 2 empty fields in the end and beginning, pretty hard coded
        text = "  " + str(text) + "  "
        for i in range(len(text) - 2):
            trigram = text[i:i+3]
            trigrams.add(trigram)
        return trigrams
    
    trigrams1 = get_trigrams(str1)
    trigrams2 = get_trigrams(str2)

    intersection = len(trigrams1.intersection(trigrams2))
    union = len(trigrams1) + len(trigrams2)

    if union == 0:
        return 0.0
    else:
        return 2 * intersection / union

def find_matches(df1, df2, output_csv_path):
    matched_pairs = pd.DataFrame(columns=['DBLP', 'ACM'])

    for idx1, row1 in df1.iterrows():
        for idx2, row2 in df2.iterrows():
            
            if row1['title'] == row2['title'] and row1['year'] == row2['year']:
                print('same title found')
                sim_auth = jaccard_similarity(row1['authors'], row2['authors'])
                if sim_auth >= 0.1:
                    print(df1.iloc[[idx1]])
                    print(df2.iloc[[idx2]])
                    sim_venue = jaccard_similarity(row1['venue'], row2['venue'])
                    if sim_venue >= 0.1:
                        matched_pairs = matched_pairs.append({'DBLP': row1['id'], 'ACM': row2['id']}, ignore_index=True)
                        print("This is a match!")
                        print("row1 ID:", row1["id"])
                        print("row2 ID:", row2["id"])

            '''if row1['title'] == row2['title'] and row1['year'] == row2['year']:
                print('same title found')
                sim_auth = trigram_similarity(row1['authors'], row2['authors'])
                if sim_auth >= 0.6:
                    sim_venue = trigram_similarity(row1['venue'], row2['venue'])
                    if sim_venue >= 0.6:
                        matched_pairs = matched_pairs.append({'id1': row1['id'], 'id2': row2['id']}, ignore_index=True)
                        print("This is a match!")
                        print("row1 ID:", row1["id"])
                        print("row2 ID:", row2["id"])'''
                        
    matched_pairs.to_csv(output_csv_path, index=False)
    print(f'Matched pairs written to {output_csv_path}')
    return matched_pairs