import re
import os
import pandas as pd

class DataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.paper_id_regex = re.compile(r'#index(\w+)')
        self.title_regex = re.compile(r'#\*(.+)')
        self.author_regex = re.compile(r'#@(.+)')
        self.venue_regex = re.compile(r'#c(.+)')
        self.year_regex = re.compile(r'#t(\d+)')

    def extract_info(self, data):
        entries = []
        entry = {}
        for line in data:
            if line.startswith('#index'):
                if entry:
                    entries.append(entry)
                    entry = {}
                entry['id'] = self.paper_id_regex.search(line).group(1)
            elif line.startswith('#*'):
                entry['title'] = f" {self.title_regex.search(line).group(1).strip()}" if self.title_regex.search(line) else ""
            elif line.startswith('#@'):
                authors_match = self.author_regex.search(line)
                if authors_match:
                    authors = authors_match.group(1).strip().replace(', ', ',')
                    entry['authors'] = f" {authors}" if authors else ""
                else:
                    entry['authors'] = ""
            elif line.startswith('#c'):
                venue_match = self.venue_regex.search(line)
                if venue_match:
                    entry['venue'] = f" {venue_match.group(1).strip()}" if venue_match else ""

            elif line.startswith('#t'):
                year_match = self.year_regex.search(line)
                if year_match:
                    entry['year'] = year_match.group(1)

        if entry:
            entries.append(entry)
        return entries

    def filter_entries(self, data):
        filtered_entries = [entry for entry in data if (
            entry.get('year') and 
            ((entry.get('venue', '').find('VLDB') != -1) or (entry.get('venue', '').find('SIGMOD') != -1)) and 
            (1995 <= int(entry['year']) <= 2004)
        )]
        return filtered_entries

    def process_dblp(self):
        with open(self.file_path, 'r') as data_file:
            data = data_file.readlines()

        db_entries = self.extract_info(data)
        filtered_db = self.filter_entries(db_entries)
        df = pd.DataFrame(filtered_db)
        df.to_csv(f'./data/DBLP_1995_2004.csv', index=False)

        return print(f'DBLP is processed, mit {len(df)} entries.')
        
    def process_acm(self):
        with open(self.file_path, 'r') as data_file:
            data = data_file.readlines()

        db_entries = self.extract_info(data)
        filtered_db = self.filter_entries(db_entries)
        df = pd.DataFrame(filtered_db)
        df.to_csv(f'./data/ACM_1995_2004.csv', index=False)

        return print(f'ACM is processed, mit {len(df)} entries.')
