import datetime
import os
import requests
from bs4 import BeautifulSoup
from app.models import Product
from app.storage import StorageBackend
from app.utils import save_image
from app.database import Database
from app.cache import Cache
import time

class Scraper:
    def __init__(self, db: Database, cache: Cache, storage_backend:StorageBackend):
        self.db = db
        self.cache = cache
        self.storage_backend = storage_backend

    def scrape_and_store(self, products_data: list):
        # Perform scraping logic here and populate products_data
        # ...
        self.storage_backend.save(products_data)

    def scrape_catalogue(self, pages: int = 5, proxy: str = None):
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {"http": proxy, "https": proxy} if proxy else None
        scraped_products = []
        new_products=set([])
        updated_products=set([])
        for page in range(1, pages + 1):
            if page==1:
                url = os.getenv('TARGET_WEBSITE')
            else:
                url = os.getenv('TARGET_WEBSITE')+f"/page/{page}/"
            
            try:
                response = requests.get(url, headers=headers, proxies=proxies)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                products = self.parse_page(soup)
                for product in products:
                    if not self.cache.is_cached(product):
                        # updating scraped_data.json file
                        self.db.update_or_add(product)
                        # updating in mongo
                        query = {"product_title": product.product_title}
                        modified_count=self.storage_backend.update(query, product.model_dump(), upsert=True)
                        if modified_count==0:
                            new_products.add(product.product_title)
                        else:
                            updated_products.add(product.product_title)
                        #updating the scraped_products array
                        scraped_products.append(product)
                        #updating in redis
                        self.cache.cache_product(product)
        
            except requests.RequestException as e:
                time.sleep(os.getenv('RETRY_TIME'))
                continue

        return scraped_products, new_products, updated_products

    def parse_page(self, soup):
        products = []
        
        for item in soup.select('.product-inner'):
            title = item.select_one('.woo-loop-product__title').get_text(strip=True)
            price = item.select_one('.woocommerce-Price-amount').get_text(strip=True).replace('₹', '').replace(',', '')
            image_url = item.select_one('img.attachment-woocommerce_thumbnail')['data-lazy-src']
            image_path = save_image(image_url, title)
            product = Product(
                product_title=title,
                product_price=float(price),
                path_to_image=image_path,
                absolute_path=image_url,
                last_updated=datetime.datetime.now().strftime('%a %d %b %Y, %I:%M%p')
            )
            products.append(product)
        return products
