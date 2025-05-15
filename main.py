# url: https://book.douban.com/latest?subcat=全部

import requests
from bs4 import BeautifulSoup

# 发送请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 依次访问前5页内容
for page in range(1, 6):
    # 构造URL
    url = f'https://book.douban.com/latest?subcat=全部&p={page}&updated_at='
    print(f"正在请求第{page}页")
    # 重试3次
    for attempt in range(3):
        try:
            # 发送请求
            response = requests.get(url, headers=headers)
            # 如果响应状态码不是200，抛出异常
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            continue
        else:
            # 如果响应状态码是200，获取响应内容，然后跳出循环
            print(f"请求成功: {response.status_code}")
            # 获取响应内容
            content = response.content.decode('utf-8')
            # 解析HTML
            soup = BeautifulSoup(content, 'lxml')
            book_list = soup.select_one('div#wrapper div#content ul')
            # 获取书籍信息
            for book in book_list.select('li'):
                title = book.select_one('div.media__body h2 a').get_text(strip=True)
                author = book.select_one('div.media__body p').get_text(strip=True)
                # 图书评分块
                rating_block = book.select('div.media__body p.subject-rating span')
                # 评分
                rating = rating_block[1].get_text(strip=True) if rating_block[1].get_text(strip=True) else '无评分'
                # 评价人数
                rating_count = rating_block[2].get_text(strip=True) if rating_block[2].get_text(strip=True) else '无评价人数'
                print(f"书名: {title}")
                print(f"作者: {author}")
                print(f"评分: {rating}")
                print(f"评价人数: {rating_count}")
                print('-' * 20)
            break