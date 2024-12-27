import os
import requests
from bs4 import BeautifulSoup

# GitHub repository URL
newurl = input("paste the url here: ")
dir = input ("Enter the a name for your folder.(The images will be saved there): ")
repo_url = newurl # Replace with your repo's folder URL
save_dir = dir

# Directory to save images
os.makedirs(save_dir, exist_ok=True)

# Get repository page content
response = requests.get(repo_url)
soup = BeautifulSoup(response.content, "html.parser")

# Base URL for raw content on GitHub
base_raw_url = "https://raw.githubusercontent.com/"
username_repo = repo_url.split("github.com/")[1].split("/tree/")[0]  # Extract username and repo

# Find all image links
img_tags = soup.find_all("a", href=True)
img_urls = [
    base_raw_url + username_repo + "/main/" + tag["href"].split("/blob/main/")[-1]
    for tag in img_tags
    if tag["href"].endswith((".png", ".jpg", ".jpeg", ".svg"))
]

# Download images
for img_url in img_urls:
    img_name = os.path.basename(img_url)
    img_path = os.path.join(save_dir, img_name)
    try:
        with open(img_path, "wb") as f:
            f.write(requests.get(img_url).content)
        print(f"Downloaded {img_name}")
    except Exception as e:
        print(f"Failed to download {img_name}: {e}")


