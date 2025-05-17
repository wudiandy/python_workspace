# This script collects nature images from Unsplash and saves them to a JSON file.

import requests
from bs4 import BeautifulSoup
import json
from time import sleep

image_urls = []

for i in range(1, 4):
    url = f"https://unsplash.com/napi/topics/nature/photos?page={i}&per_page=10"
    print(f"Fetching page {url}...")
    try:
        # Set request headers to simulate browser access
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if request is successful
        sleep(2)  # Set request delay to avoid being blocked for too frequent requests
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        exit()
    # Parse JSON content
    data = response.json()
    for item in data:
        # Get image URL
        image_url = item["slug"]
        image_urls.append("https://unsplash.com/photos/" + image_url)
        print(f"Image URL: {image_url}")

json_array = []
for image_url in image_urls:
    # Download image
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check if request is successful
        sleep(2)  # Set request delay to avoid being blocked for too frequent requests
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    html_content = response.content
    # Parse HTML content
    soup = BeautifulSoup(html_content, "lxml")
    # Find the image tag
    image_tag = soup.find("img", class_="czQTa")
    if image_tag:
        # Get the image URL
        image_url = image_tag["src"]
        alt = image_tag["alt"]
        # 把 image_url 和 alt 组成一个 JSON 对象
        json_data = {"image_url": image_url, "alt": alt}
        json_array.append(json_data)
        print(f"Image URL: {image_url}")
    else:
        print("Image not found")

# Open nature_images.json, if it doesn't exist, create it
try:
    with open("nature_images.json", "r") as f:
        existing_data = json.load(f)
except FileNotFoundError:
    existing_data = []

# Save json_array to nature_images.json
with open("nature_images.json", "w") as f:
    # Merge existing data with new data
    existing_data.extend(json_array)
    json.dump(existing_data, f, indent=4)

print("All images downloaded successfully.")
