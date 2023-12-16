import pandas as pd
from data_preparation import DataExtractor
from data_blocking import create_year_blocks
from data_matching import calculate_similarities

def main():
    # paths for dblp and acm
    #dblp_path = './data/citation-acm-v8.txt'
    #acm_path = './data/dblp.txt'

    #extract_dblp = DataExtractor(dblp_path)
    #extract_dblp.process_dblp()

    #extract_acm = DataExtractor(acm_path)
    #extract_acm.process_acm()

    # -------------------WORKS--------------------------

    # create blocks, change likewise to get better
    year_ranges = [(1995, 1996), (1997, 1998), (1999, 2000), (2001,2002), (2003,2004)]

    df_dblp_path = pd.read_csv('data/DBLP_1995_2004.csv')
    df_acm_path = pd.read_csv('data/ACM_1995_2004.csv')

    # get blocks as dictionary
    result_blocks_dblp = create_year_blocks(df_dblp_path, year_ranges)
    result_blocks_acm = create_year_blocks(df_acm_path, year_ranges)

    print(result_blocks_dblp)
    print(result_blocks_acm)

    #similarity_df = calculate_similarities(df_dblp_path, df_acm_path, threshold=0.5, column_name='Title')
    #print(similarity_df.head())

if __name__ == "__main__":
    main()
