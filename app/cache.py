class Cache:
    def __init__(self):
        self.cache = {}

    def is_cached(self, product):
        cached_product = self.cache.get(product.product_title)
        return cached_product and cached_product['product_price'] == product.product_price

    def cache_product(self, product):
        self.cache[product.product_title] = product.model_dump()