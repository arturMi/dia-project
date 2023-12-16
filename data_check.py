import os
import requests
import tarfile

def download_and_extract_tgz(file_name, directory_path='./data/', http_link=None, extracted_file_extension='.txt'):
    if file_name + extracted_file_extension in os.listdir(directory_path):
        print("File exists locally.")
        file_path = os.path.join(directory_path, file_name + extracted_file_extension)
        return file_path  # Return file path

    else:
        if http_link is None:
            print("HTTP link not provided. Cannot download the file.")
            return None

        print("File does not exist locally. Downloading from HTTP link.")
        response = requests.get(http_link)
        if response.status_code == 200:
            # Save the downloaded file locally
            with open(os.path.join(directory_path, file_name + '.tgz'), 'wb') as file:
                file.write(response.content)
            print("File downloaded successfully.")

            tgz_file_path = os.path.join(directory_path, file_name + '.tgz')

            # Extract the downloaded .tgz file
            with tarfile.open(tgz_file_path, "r:gz") as tar:
                tar.extractall(path=directory_path)
                print(f"Extracted contents of {file_name}.tgz")

            # Find the specific .txt file within the extracted contents
            txt_file_path = os.path.join(directory_path, file_name + extracted_file_extension)
            if os.path.exists(txt_file_path):
                print(f"Found {file_name}{extracted_file_extension} in extracted contents")
                return txt_file_path  # Return path to the .txt file
            else:
                print(f"Could not find {file_name}{extracted_file_extension} in extracted contents")
                return None

        else:
            print("Failed to download the file. Status code:", response.status_code)
            return None