import requests
from bs4 import BeautifulSoup

def check_js_rendering(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"요청 실패: {e}")
        return

    html = response.text
    print(f"\nHTML 응답 길이: {len(html)}\n")

    # 미리보기
    print("HTML 미리보기 (상위 1000자):\n")
    print(html[:1000])
    print("\n" + "-"*50 + "\n")

    # 콘텐츠 여부 판단
    soup = BeautifulSoup(html, "html.parser")

    keywords = ["nvidia", "nvda", "news", "card", "article", "headline"]
    found_keywords = [kw for kw in keywords if kw in html.lower()]

    if not soup.find_all("h2") and len(found_keywords) < 2:
        print("결과: JS 렌더링된 콘텐츠일 가능성이 높습니다 (데이터 없음)")
    else:
        print("결과: 정적 HTML로 콘텐츠가 포함되어 있습니다")

if __name__ == "__main__":
    test_url = "https://www.stocktitan.net/news/NVDA/"
    check_js_rendering(test_url)
