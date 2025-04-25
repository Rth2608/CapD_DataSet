docker-compose down
docker-compose up -d

사이트 분석 시작
   ├─  HTML에 데이터가 있음 → requests + BeautifulSoup
   ├─  JavaScript 렌더링 필요 → Selenium or Playwright
   │     ├─ 서버에서 실행 불안정함 → Playwright 추천
   │     └─ 안정된 UI 필요하면 Selenium 사용
   ├─  RSS 피드 있음 → feedparser 사용
   └─  API가 존재 → REST API 크롤링 (권장)


1. requests.get(url).text → 내용 비어 있음
2. 브라우저 F12 → Elements 탭: 데이터는 있음
3. F12 → Network 탭 → XHR/fetch 확인 → JS 요청으로 데이터 받아오는지 확인