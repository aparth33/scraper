import logging
import os
from pymongo import MongoClient
from typing import List

from app.storage import StorageBackend

class MongoStorageBackend(StorageBackend):
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[os.getenv('MONGO_COLLECTION_NAME')]

    def save(self, data: list):
        # Ensure all items in the list are dicts
        if all(isinstance(item, dict) for item in data):
            self.collection.insert_many(data)
        else:
            raise ValueError("All items in the data list must be dictionaries")

    def load(self) -> list:
        return list(self.collection.find({}, {'_id': 0}))

    def update(self, query: dict, new_document: dict, upsert: bool = False):
        """
        Replaces the entire document in the collection based on the query.

        :param query: A dictionary to match the document to be replaced.
        :param new_document: The new document that will replace the matched document.
        :param upsert: If True, insert the document if it does not exist.
        """
        # Replace the entire document with new_document
        replace_result = self.collection.replace_one(query, new_document, upsert=upsert)
        
        # Log the outcome of the operation
        if replace_result.matched_count > 0:
            logging.info(f"Replaced document matching query: {query}.")
        elif upsert:
            logging.info(f"Inserted new document as no match was found: {new_document}")
        else:
            logging.warning(f"No document matched the query: {query}. Nothing was updated.")

        return replace_result.modified_count  # Return the number of documents modified (usually 1 or 0)