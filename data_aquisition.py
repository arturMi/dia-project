import os
import requests
import tarfile
import codecs

def download_file(url, file_name, folder_path):
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        print(f"The file '{file_name}' already exists in the folder.")
    else:
        response = requests.get(url)

        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"File '{file_name}' downloaded successfully to '{folder_path}'.")
        else:
            print("Failed to download the file.")

def extract_all_tgz_files(folder_path):
    tgz_files = [f for f in os.listdir(folder_path) if f.endswith('.tgz')]

    for tgz_file in tgz_files:
        file_path = os.path.join(folder_path, tgz_file)
        if os.path.exists(file_path):
            with tarfile.open(file_path, 'r:gz') as tar:
                tar.extractall(folder_path)
            print(f"File '{tgz_file}' extracted successfully in '{folder_path}' folder.")
        else:
            print(f"File '{tgz_file}' does not exist in '{folder_path}'.")

def convert_txt_to_utf8(folder_path):
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            with codecs.open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"File '{txt_file}' converted to UTF-8 in '{folder_path}' folder.")
        else:
            print(f"File '{txt_file}' does not exist in '{folder_path}'.")
