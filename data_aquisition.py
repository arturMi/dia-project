import os
import requests
import tarfile

def download_and_extract(url, file_name):
    folder_path = "./data/"
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        print(f"The file '{file_name}' already exists in the folder.")
    else:
        # Make a GET request to download the file
        response = requests.get(url)

        if response.status_code == 200:
            # Save the downloaded file
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            # Check if the file is a .tgz and extract it
            if file_name.endswith('.tgz'):
                with tarfile.open(file_path, 'r:gz') as tar:
                    tar.extractall(folder_path)
                print(f"File '{file_name}' downloaded and extracted successfully.")
            else:
                print("Downloaded file is not a .tgz file.")
        else:
            print("Failed to download the file.")