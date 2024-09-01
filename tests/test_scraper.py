import unittest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
import datetime

from app.scraper import Scraper
from dotenv import load_dotenv

load_dotenv('.env')
class TestScraper(unittest.TestCase):

    @patch('app.scraper.Product')  # Replace 'your_module' with the actual module name where Product is defined
    @patch('app.scraper.datetime')  # Mock datetime to control the output of datetime.now()
    def test_parse_page(self, mock_datetime, MockProduct):
        # Setup
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 9, 1, 12, 0, 0)
        
        # Example HTML snippet to simulate the structure of the page being parsed
        html_content = '''
        <div class="product-inner">
            <h2 class="woo-loop-product__title">Product 1</h2>
            <span class="woocommerce-Price-amount">₹1,250.00</span>
            <img class="attachment-woocommerce_thumbnail" data-lazy-src="https://example.com/image1.jpg">
        </div>
        <div class="product-inner">
            <h2 class="woo-loop-product__title">Product 2</h2>
            <span class="woocommerce-Price-amount">₹2,500.00</span>
            <img class="attachment-woocommerce_thumbnail" data-lazy-src="https://example.com/image2.jpg">
        </div>
        '''
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Mock the Product constructor
        MockProduct.side_effect = lambda **kwargs: kwargs  # Mocking Product to return the kwargs dict

        # Create an instance of the scraper and call parse_page
        scraper = Scraper()  # Replace 'Scraper' with the actual class name containing parse_page
        products = scraper.parse_page(soup)
        
        # Assertions
        self.assertEqual(len(products), 2)
        
        expected_product_1 = {
            'product_title': 'Product 1',
            'product_price': 1250.00,
            'path_to_image': 'https://example.com/image1.jpg',
            'absolute_path': 'https://example.com/image1.jpg',
            'last_updated': 'Fri 01 Sep 2023, 12:00PM'
        }
        expected_product_2 = {
            'product_title': 'Product 2',
            'product_price': 2500.00,
            'path_to_image': 'https://example.com/image2.jpg',
            'absolute_path': 'https://example.com/image2.jpg',
            'last_updated': 'Fri 01 Sep 2023, 12:00PM'
        }

        self.assertDictEqual(products[0], expected_product_1)
        self.assertDictEqual(products[1], expected_product_2)

if __name__ == '__main__':
    unittest.main()
