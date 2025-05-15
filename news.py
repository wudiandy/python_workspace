# url: https://www.cnn.com

import requests
from bs4 import BeautifulSoup

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # 发送请求
    # 访问CNN首页
    print("正在请求: https://www.cnn.com")
    response = requests.get('https://www.cnn.com', timeout=5, headers=headers)
    response.raise_for_status()  # 检查请求是否成功
    # 解析HTML
    # 使用lxml解析器
    soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
    # 筛选出class="body tabcontent active",data-tabcontent="Content"的section标签
    section = soup.find('section', class_='body tabcontent active', attrs={'data-tabcontent': 'Content'})
    # 获取section标签下的所有a标签的href属性
    links = [a['href'] for a in section.find_all('a', href=True)]
    # 只保留以/2025/开头的链接
    links = [link for link in links if link.startswith('/2025/')]
    # 循环遍历所有链接
    for link in links:
        # 访问链接
        full_url = f'https://www.cnn.com{link}'
        print(f"正在请求: {full_url}")
        response = requests.get(full_url, timeout=5)
        response.raise_for_status()
        # 解析HTML
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        # 获取h1标签的文本
        title = soup.find('h1').get_text(strip=True)
        print(f"该页面的h1标签文本: {title.replace("'", "").replace("[", "").replace("]", "")}")
        # 打印所有class="timestamp vossi-timestamp"的div标签的文本
        timestamp = soup.find('div', class_='timestamp vossi-timestamp').get_text(strip=True)
        # 去除timestamp中的换行符和空格
        print(f"该页面的时间戳: {timestamp.replace(' ', '').replace('\n', ': ')}")
        print('-' * 20)
except requests.RequestException as e:
    print(f"请求失败: {e}")
except Exception as e:
    print(f"发生错误: {e}")