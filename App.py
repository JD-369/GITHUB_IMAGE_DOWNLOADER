from flask import Flask, request, jsonify
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/download_images', methods=['POST'])
def download_images():
    data = request.json
    repo_url = data['repo_url']
    save_dir = data.get('dir', 'images')

    os.makedirs(save_dir, exist_ok=True)
    response = requests.get(repo_url)
    soup = BeautifulSoup(response.content, "html.parser")

    base_raw_url = "https://raw.githubusercontent.com/"
    username_repo = repo_url.split("github.com/")[1].split("/tree/")[0]

    img_tags = soup.find_all("a", href=True)
    img_urls = [
        base_raw_url + username_repo + "/main/" + tag["href"].split("/blob/main/")[-1]
        for tag in img_tags if tag["href"].endswith((".png", ".jpg", ".jpeg", ".svg"))
    ]

    downloaded = []
    for img_url in img_urls:
        img_name = os.path.basename(img_url)
        img_path = os.path.join(save_dir, img_name)
        try:
            with open(img_path, "wb") as f:
                f.write(requests.get(img_url).content)
            downloaded.append(img_name)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"downloaded": downloaded})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
