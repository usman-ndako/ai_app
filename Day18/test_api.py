import requests
import os

# Local API endpoint
url = "http://127.0.0.1:8000/predict/"

# Folder containing test images
test_folder = "test_images/"  # make sure this folder exists

# Loop through all images
for filename in os.listdir(test_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".jfif")):
        file_path = os.path.join(test_folder, filename)
        files = {"file": open(file_path, "rb")}
        response = requests.post(url, files=files)
        print(f"{filename} -> {response.json()}")
