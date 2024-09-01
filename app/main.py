import logging
from logging.handlers import RotatingFileHandler
import os
from fastapi import FastAPI, Depends, HTTPException, Query
from app.mongoStorage import MongoStorageBackend
from app.scraper import Scraper
from app.auth import get_current_user
from app.models import ScrapeResult
from app.database import Database
from app.cache import Cache
from app.notifications import notify, send_email

app = FastAPI()

# Initialize components
db = Database('scraped_data.json')
cache = Cache()
mongoDB = MongoStorageBackend(os.getenv('MONGO_URI'), os.getenv('MONGO_DATABASE_NAME'))
# Loading products - this will either hit the cache or the database
products = mongoDB.load()

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')
# Set up a rotating file handler
handler = RotatingFileHandler(
    'logs/app.log', 
    maxBytes=2000,  # Rotate after 2KB
    backupCount=5   # Keep 5 old log files
)

# Configure logging
logging.basicConfig(
    handlers=[handler],
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# # Configure logging to output to the console
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flush all keys in the current database
cache.clear()
cache.cache_all_products(products)

scraper = Scraper(db, cache, mongoDB)

@app.get("/scrape", response_model=ScrapeResult)
async def scrape_catalogue(
    pages: int = Query(5, description="Number of pages to scrape"),
    proxy: str = Query(None, description="Proxy string if required"),
    user: str = Depends(get_current_user)
):
    
    scraped_data, new_products, updated_products = scraper.scrape_catalogue(pages=pages, proxy=proxy)
    notify(f"Scraping completed: {len(scraped_data)} products scraped-{len(new_products)} new products added and {len(updated_products)} products updated.")
    return {"status": "success", "products_scraped": len(scraped_data), "products_added": len(new_products), "products_updated": len(updated_products)}