import pandas as pd

# Function to create year blocks
def create_year_blocks(dataframe, year_ranges):
    blocks = {}
    dataframe = dataframe.sort_values(by='Year')
    for i, (start, end) in enumerate(year_ranges):
        block_name = f'Block_{start}_{end}'
        blocks[block_name] = dataframe[(dataframe['Year'] >= start) & (dataframe['Year'] <= end)]
    return blocks

