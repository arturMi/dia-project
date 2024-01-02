import os
import requests
import tarfile

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