import time
import requests
from bs4 import BeautifulSoup
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow

# Set the scope for Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# Create credentials for Google Sheets API
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)
# Create a client for Google Sheets API
service = gspread.authorize(creds)
# Open Google Sheets
spreadsheet = service.open_by_url(
    "https://docs.google.com/spreadsheets/d/12Yumt1GPXUcRAxcshe4S-2uJRDW1y-Yd2K4HTyMrYig/edit"
)
# Select worksheet
worksheet = spreadsheet.sheet1
# Clear worksheet
worksheet.clear()
# Set header row
worksheet.append_row(["书名", "价格", "评分", "库存状态"])

# List to store all book data
all_books = []

# Get HTML content from https://books.toscrape.com, total 50 pages
for i in range(1, 50):
    url = f"https://books.toscrape.com/catalogue/page-{i}.html"
    try:
        # Set request headers to simulate browser access
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if request is successful
        # Set request delay to avoid being blocked for too frequent requests
        time.sleep(2)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        exit()
    # Parse HTML content
    soup = BeautifulSoup(response.text, "lxml")
    # Get all article tags
    articles = soup.find_all("article", class_="product_pod")
    # Iterate through each article tag
    for article in articles:
        # Get book title
        title = article.h3.a["title"]
        # Get price
        price = article.find("p", class_="price_color").text
        # Get rating
        rating = article.p["class"][1]
        # Get availability
        availability = article.find("p", class_="instock availability").text.strip()
        # Write data to all_books list
        all_books.append([title, price, rating, availability])
        print(f"书名: {title}")

# Batch write data to Google Sheets
worksheet.append_rows(all_books, value_input_option="USER_ENTERED")
# Notify user that data has been successfully written
print("数据已成功写入Google Sheets！")
