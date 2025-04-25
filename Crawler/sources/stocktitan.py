from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime

SCROLL_COUNT = 5


def get_stock_news_links(ticker):
    links = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.stocktitan.net/news/{ticker}/")
        page.wait_for_timeout(2000)

        for _ in range(SCROLL_COUNT):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1000)

        soup = BeautifulSoup(page.content(), "html.parser")
        a_tags = soup.select(f"a[href^='/news/{ticker}/']")

        for a_tag in a_tags:
            href = a_tag.get("href", "")
            if href.endswith(".html"):
                full_url = "https://www.stocktitan.net" + href
                if full_url not in links:
                    links.append(full_url)

        browser.close()
    return links


def fetch_news_detail(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
        except Exception:
            browser.close()
            return {
                "url": url,
                "title": "제목 없음",
                "date": "날짜 없음",
                "content": "본문 없음",
            }

        soup = BeautifulSoup(page.content(), "html.parser")

        title_tag = (
            soup.select_one("h1.article-title")
            or soup.select_one("h1.article-page-title")
            or soup.select_one("h1")
        )
        title = title_tag.text.strip() if title_tag else "제목 없음"

        time_tag = soup.select_one("time")
        if time_tag and time_tag.has_attr("datetime"):
            try:
                fromiso = time_tag["datetime"].replace("Z", "+00:00")
                dt = datetime.fromisoformat(fromiso)
                date = dt.strftime("%Y-%m-%d %H:%M")
            except:
                date = time_tag["datetime"]
        else:
            date = "날짜 없음"

        content = "본문 없음"
        if time_tag:
            paragraphs = []
            next_elem = time_tag.find_next_sibling()
            while next_elem:
                if next_elem.name == "p":
                    text = next_elem.get_text(strip=True)
                    if text:
                        paragraphs.append(text)
                elif next_elem.name == "/div":
                    break
                next_elem = next_elem.find_next_sibling()
            if paragraphs:
                content = "\n".join(paragraphs)

        browser.close()
        return {
            "url": url,
            "title": title,
            "date": date,
            "content": content,
        }