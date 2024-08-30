import json
from app.models import Product
from typing import List

class Database:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def update_or_add(self, product: Product):
        for item in self.data:
            if item['product_title'] == product.product_title:
                item.update(product.model_dump())
                self.save_data()
                return
        self.data.append(product.model_dump())
        self.save_data()
