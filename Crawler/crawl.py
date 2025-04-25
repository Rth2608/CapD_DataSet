from celery import Celery
from celery.schedules import crontab
import os
import redis

from Crawler.stocklist import load_stock_list
from Crawler.db import save_to_db
from Crawler.sources.stocktitan import get_stock_news_links, fetch_news_detail

celery = Celery(__name__, broker=os.getenv("CELERY_BROKER_URL"))
celery.conf.timezone = 'Asia/Seoul'

# Beat 스케줄 등록 (매 5분마다 실행)
celery.conf.beat_schedule = {
    'crawl-stocks-every-5-minutes': {
        'task': 'Crawler.crawl.crawl_all_stocks',
        'schedule': crontab(minute='*/5'),
    },
}

# Redis 클라이언트 설정
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@celery.task
def crawl_all_stocks():
    lock_key = "lock:crawl_all_stocks"

    if redis_client.get(lock_key):
        print("[중복 방지] 이미 작업이 실행 중입니다.")
        return

    try:
        redis_client.set(lock_key, "1", ex=600)  # 10분 TTL
        print("[뉴스 크롤링 시작]")

        STOCK_LIST = load_stock_list()
        for ticker in STOCK_LIST:
            print(f"[{ticker}] [뉴스 수집 시작]")
            links = get_stock_news_links(ticker)
            news_items = []

            for url in links[:10]:
                news = fetch_news_detail(url)
                news['ticker'] = ticker
                news_items.append(news)

            save_to_db(news_items)

        print("[뉴스 수집 완료]")
    finally:
        redis_client.delete(lock_key)
        print("[Redis 락 해제 완료]")


celery = Celery(__name__, broker=os.getenv("CELERY_BROKER_URL"))
celery.conf.timezone = 'Asia/Seoul'

# 스케줄 등록
celery.conf.beat_schedule = {
    'crawl-stocks-every-5-minutes': {
        'task': 'Crawler.crawl.crawl_all_stocks',
        'schedule': crontab(minute='*/5'),  # 매 5분마다 실행
    },
}