import time
import random
import requests
from bs4 import BeautifulSoup
from .headers import get_headers

def get_story_urls(base_url, max_stories=4000):
    story_urls, page = [], 1
    while len(story_urls) < max_stories:
        url = f"{base_url}trang-{page}/"
        try:
            response = requests.get(url, headers=get_headers())
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            story_links = soup.select("div.list-truyen div.row h3.truyen-title a")
            if not story_links:
                break

            for link in story_links:
                if len(story_urls) >= max_stories:
                    break
                story_urls.append(link["href"])

            page += 1
            time.sleep(random.uniform(1, 3))  # tránh bị chặn
        except Exception as e:
            print(f"Lỗi khi lấy danh sách truyện từ trang {page}: {e}")
            break
    return story_urls
