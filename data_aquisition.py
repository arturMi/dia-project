import os
import requests
import tarfile
import chardet

def download_extract_read(url, file_name):
    folder_path = "./data/"
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        print(f"The file '{file_name}' already exists in the folder.")
    else:
        response = requests.get(url)

        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            if file_name.endswith('.tgz'):
                with tarfile.open(file_path, 'r:gz') as tar:
                    tar.extractall(folder_path)
                print(f"File '{file_name}' downloaded and extracted successfully.")

                # Now read the extracted file with detected encoding
                extracted_file_path = os.path.join(folder_path, os.path.splitext(file_name)[0])  # Change extension
                with open(extracted_file_path, 'rb') as extracted_file:
                    raw_data = extracted_file.read()
                    detected_encoding = chardet.detect(raw_data)['encoding']

                with open(extracted_file_path, 'r', encoding=detected_encoding) as extracted_file:
                    data = extracted_file.readlines()

                print("Data read successfully.")
            else:
                print("Downloaded file is not a .tgz file.")
        else:
            print("Failed to download the file.")

