import pandas as pd
import time
from data_aquisition import check_download_extract
from data_preparation import DataExtractor
from data_matching import create_year_blocks, find_matches


def main():

    # check if DBLP and ACM are in the data folder, if not download and extract them
    folder_path = './data/'
    dblp_url = 'https://lfs.aminer.cn/lab-datasets/citation/dblp.v8.tgz'
    check_download_extract(dblp_url, folder_path)


    acm_url = 'https://lfs.aminer.cn/lab-datasets/citation/citation-acm-v8.txt.tgz'
    check_download_extract(acm_url, folder_path)


    dblp_path = './data/dblp.txt'
    acm_path = './data/citation-acm-v8.txt'

    extract_acm = DataExtractor(acm_path)
    extract_acm.process_acm()

    extract_dblp = DataExtractor(dblp_path)
    extract_dblp.process_dblp()

    print("DATA WAS EXTRACTED")

    # -------------------WORKS--------------------------

    # create blocks, change likewise to get better
    year_ranges = [(1995, 1996), (1997, 1998), (1999, 2000), (2001,2002), (2003,2004)]

    df_dblp_path = pd.read_csv('data/DBLP_1995_2004.csv')
    df_acm_path = pd.read_csv('data/ACM_1995_2004.csv')

    #df_dblp_path = pd.read_csv('data/DBLP2.csv', engine='python')
    #df_acm_path = pd.read_csv('data/ACM.csv', engine='python')

    # get blocks as dictionary
    result_blocks_dblp = create_year_blocks(df_dblp_path, year_ranges)
    result_blocks_acm = create_year_blocks(df_acm_path, year_ranges)

    print(result_blocks_dblp)
    print(result_blocks_acm)
    
    print("BLOCKS WERE CREATED AND SIMILARITY WILL BE CALCULATED")

    output_csv_path = './data/matched_pairs.csv'
    matched_pairs_df = find_matches(df_dblp_path, df_acm_path, output_csv_path)
    print(matched_pairs_df)


if __name__ == "__main__":
    main()
