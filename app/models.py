from pydantic import BaseModel

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str
    absolute_path: str
    last_updated: str

class ScrapeResult(BaseModel):
    status: str
    products_scraped: int
    products_added: int
    products_updated: int
