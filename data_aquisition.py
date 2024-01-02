import os
import requests
import tarfile

def check_download_extract(url, folder_path):
    # Extract file name from URL
    file_name = url.split('/')[-1]
    file_path = os.path.join(folder_path, file_name)

    if not os.path.exists(file_path):
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
                print(f"File '{file_name}' downloaded and extracted successfully in '{folder_path}' folder.")
            else:
                print("Downloaded file is not a .tgz file.")
        else:
            print("Failed to download the file.")
    else:
        print(f"The file '{file_name}' already exists in the folder.")
