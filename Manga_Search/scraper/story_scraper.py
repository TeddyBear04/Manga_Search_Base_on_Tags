import requests
from bs4 import BeautifulSoup
from .headers import get_headers

def scrape_story(story_url, driver=None):
    try:
        response = requests.get(story_url, headers=get_headers())
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Tên truyện
        title = soup.select_one("h3.title")
        title = title.get_text().strip() if title else "N/A"

        # Cốt truyện
        description_div = soup.select_one("div.desc-text")
        if description_div:
            has_br = description_div.find("br") is not None
            if has_br:
                all_text = list(description_div.stripped_strings)
                desc = " ".join(all_text[1:]) if len(all_text) > 1 else "N/A"
            else:
                desc = " ".join(description_div.get_text().split())
        else:
            desc = "N/A"

        # Tags
        tags = [tag.get_text().strip() for tag in soup.select('div.info div a[href*="/the-loai/"]')]
        tags_str = ", ".join(tags) if tags else "N/A"

        # Tác giả
        author = soup.select_one("a[itemprop='author']")
        author_name = author.get_text().strip() if author else "N/A"

        # Trạng thái
        status = soup.select_one("span.text-success")
        status_text = status.get_text().strip() if status else "Đang cập nhật"

        # Đánh giá
        rating = soup.select_one("span[itemprop='ratingValue']")
        rating_value = rating.get_text().strip() if rating else "N/A"

        # Các truyện khác của tác giả
        other_stories = [link.get_text().strip() for link in soup.select("div.row h3 a")]
        other_stories_str = ", ".join(other_stories) if other_stories else "N/A"

        # Ngày phát hành
        release_date_meta = soup.select_one("meta[property='book:release_date']")
        release_date = release_date_meta["content"] if release_date_meta else "N/A"

        return {
            "Tên truyện": title,
            "Cốt truyện": desc,
            "Tags": tags_str,
            "Tác giả": author_name,
            "Trạng thái": status_text,
            "Đánh giá": rating_value,
            "Các truyện khác của tác giả": other_stories_str,
            "Ngày phát hành": release_date,
            "URL": story_url,
        }
    except Exception as e:
        print(f"Lỗi khi cào dữ liệu từ {story_url}: {e}")
        return None
