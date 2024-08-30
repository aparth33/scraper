import datetime
import requests
from bs4 import BeautifulSoup
from app.models import Product
from app.utils import save_image
from app.database import Database
from app.cache import Cache
import time

class Scraper:
    def __init__(self, db: Database, cache: Cache):
        self.db = db
        self.cache = cache

    def scrape_catalogue(self, pages: int = 5, proxy: str = None):
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {"http": proxy, "https": proxy} if proxy else None
        scraped_products = []

        for page in range(1, pages + 1):
            if page==1:
                url = f"https://dentalstall.com/shop"
            else:
                url = f"https://dentalstall.com/shop/page/{page}/"
            
            try:
                response = requests.get(url, headers=headers, proxies=proxies)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                products = self.parse_page(soup)
                print("number of products on page number "+str(page)+"is "+str(len(products)))
                for product in products:
                    if not self.cache.is_cached(product):
                        self.db.update_or_add(product)
                        scraped_products.append(product)
                        self.cache.cache_product(product)
        
            except requests.RequestException as e:
                time.sleep(5)
                continue

        return scraped_products

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
