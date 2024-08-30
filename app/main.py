from fastapi import FastAPI, Depends, HTTPException, Query
from app.scraper import Scraper
from app.auth import get_current_user
from app.models import ScrapeResult
from app.database import Database
from app.cache import Cache
from app.notifications import notify

app = FastAPI()

# Initialize components
db = Database('scraped_data.json')
cache = Cache()
scraper = Scraper(db, cache)

@app.get("/scrape", response_model=ScrapeResult)
async def scrape_catalogue(
    pages: int = Query(5, description="Number of pages to scrape"),
    proxy: str = Query(None, description="Proxy string if required"),
    user: str = Depends(get_current_user)
):
    scraped_data = scraper.scrape_catalogue(pages=pages, proxy=proxy)
    notify(f"Scraping completed: {len(scraped_data)} products scraped.")
    return {"status": "success", "products_scraped": len(scraped_data)}