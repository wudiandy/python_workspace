import gspread
import csv
from google_auth_oauthlib.flow import InstalledAppFlow

# 设置Google Sheets API的范围
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# 创建Google Sheets API的凭据
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
# 创建Google Sheets API的客户端
service = gspread.authorize(creds)
# 打开Google Sheets
spreadsheet = service.open_by_url('https://docs.google.com/spreadsheets/d/12Yumt1GPXUcRAxcshe4S-2uJRDW1y-Yd2K4HTyMrYig/edit')
# 选择工作表
worksheet = spreadsheet.sheet1

with open("test_quotes.csv", "r") as f:
    # 读取CSV文件
    reader = csv.reader(f)
    for row in reader:
        worksheet.append_row(row)

# 提示用户数据已成功写入
print("数据已成功写入Google Sheets！")