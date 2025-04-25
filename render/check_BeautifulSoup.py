# 뉴스 제목 태그가 실제로 있는지 확인
from bs4 import BeautifulSoup
import requests

url = "https://www.stocktitan.net/news/NVDA/"
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# 뉴스 카드 확인
cards = soup.select("div.card")
print(f"뉴스 카드 수: {len(cards)}")

if cards:
    for c in cards[:3]:  # 3개만 미리보기
        title = c.select_one("h2.card-title")
        print("제목:", title.text.strip() if title else "없음")
else:
    print("뉴스 카드 없음 → JS 렌더링 가능성 있음")
