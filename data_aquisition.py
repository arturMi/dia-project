import os
import requests
import tarfile

def check_download_extract(url, file_name, folder_path):
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        print(f"The file '{file_name}' already exists in the folder.")
    else:
        response = requests.get(url)

        if response.status_code == 200:
            with open(file_path, 'r') as file:
                file.write(response.content)
            
            if file_name.endswith('.tgz'):
                with tarfile.open(file_path, 'r:gz') as tar:
                    tar.extractall(folder_path)
                print(f"File '{file_name}' downloaded and extracted successfully.")
            else:
                print("Downloaded file is not a .tgz file.")
        else:
            print("Failed to download the file.")