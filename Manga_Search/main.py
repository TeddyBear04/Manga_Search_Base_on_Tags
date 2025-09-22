import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scraper.url_scraper import get_story_urls
from scraper.story_scraper import scrape_story
from utils.cleaner import clean_story_data
from analysis.analyzer import analyze_tags, analyze_authors, analyze_status
from analysis.visualizer import plot_bar

def main():
    base_url = "https://truyenfull.vision/danh-sach/truyen-hot/"
    output_file = "TruyenFull.xlsx"
    max_stories = 100  # có thể chỉnh lại

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)

    all_stories = []
    try:
        story_urls = get_story_urls(base_url, max_stories)
        print(f"Đã tìm thấy {len(story_urls)} URL truyện.")
        for url in story_urls:
            story_data = scrape_story(url, driver)
            if story_data:
                story_data = clean_story_data(story_data)
                all_stories.append(story_data)
            time.sleep(random.uniform(1, 3))

        if all_stories:
            df = pd.DataFrame(all_stories)
            df.to_excel(output_file, index=False)
            print(f"Đã lưu dữ liệu vào {output_file}")

            # Phân tích cơ bản
            print("\nTop Tags:")
            print(analyze_tags(df))
            print("\nTop Tác giả:")
            print(analyze_authors(df))
            print("\nTrạng thái:")
            print(analyze_status(df))

            # Trực quan hóa
            plot_bar(analyze_tags(df), "Top Tags", "Tag", "Số lượng")
            plot_bar(analyze_authors(df), "Top Tác giả", "Tác giả", "Số lượng")
            plot_bar(analyze_status(df), "Phân bố trạng thái", "Trạng thái", "Số lượng")
        else:
            print("Không có dữ liệu để lưu.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
