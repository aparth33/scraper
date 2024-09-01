import json
import os
import redis
from app.storage import StorageBackend


class Cache():
    def __init__(self, redis_host=os.getenv('REDIS_HOST'), redis_port=int(os.getenv('REDIS_PORT')), redis_db=0):
         # Initialize Redis connection
        self.cache = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

    def is_cached(self, product):
        cached_product = self.cache.get(product.product_title)
        if cached_product:
            serialized_product=json.loads(cached_product)
            return serialized_product and serialized_product['product_price'] == product.product_price

    def object_to_dict(self, obj):
        # Convert the object to a dictionary manually or using a method
        # Example if the object has attributes directly accessible
        return {
            'product_title': obj.product_title,
            'product_price': obj.product_price,
            'path_to_image': obj.path_to_image,
            'absolute_path': obj.absolute_path,
            'last_updated': obj.last_updated
        }
    
    def cache_product(self, product):
        # Convert the product object to a dictionary
        # If it's a custom object, replace this with your own method to convert it to a dict
        if not isinstance(product, dict):
            product_dict = self.object_to_dict(product)  # Custom method for conversion
        else:
            product_dict=product
        # Serialize the product dictionary to a JSON string
        serialized_product = json.dumps(product_dict)
        
        # Store the JSON string in Redis using the product title as the key
        self.cache.set(product_dict['product_title'], serialized_product)

    def clear(self):
        self.cache.flushdb()

    def cache_all_products(self, products):
        # Iterate through all products and cache each one
        for product in products:
            self.cache_product(product)