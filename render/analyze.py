import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def analyze_website_structure(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"요청 실패: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    print(f"\n사이트: {urlparse(url).netloc}")
    
    print("\n=== Title 후보 태그 ===")
    for tag in soup.find_all(['h1', 'h2', 'title']):
        text = tag.get_text(strip=True)
        if text:
            print(f"[{tag.name}] {text[:100]}")

    print("\n=== 본문 유력 태그 (p, div 일부) ===")
    for tag in soup.find_all(['p', 'div'], limit=10):
        text = tag.get_text(strip=True)
        if len(text) > 50:
            print(f"[{tag.name} class={tag.get('class')}] {text[:100]}")

    print("\n=== Meta 정보 ===")
    for tag in soup.find_all('meta'):
        if tag.get('name') in ['description', 'author', 'keywords']:
            print(f"[meta name={tag.get('name')}] -> {tag.get('content')}")


# 실행 파트
if __name__ == "__main__":
    user_url = input("분석할 웹사이트 URL을 입력하세요: ")
    analyze_website_structure(user_url)
