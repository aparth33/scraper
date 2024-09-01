# Product Scraping Tool

## Overview

This Python project is a web scraping tool built using the FastAPI framework. It automates the process of scraping product data (such as product name, price, and image) from a target website and stores the scraped information in a local database. The project also includes features such as caching scraped data using Redis, sending notifications via Slack or email, and error handling with logging.

## Features

- **Web Scraping**: Scrapes product data (name, price, image) from a specified website.
- **Custom Settings**:
  - Limit the number of pages to scrape.
  - Use a proxy for scraping.
- **Data Storage**: Stores scraped data in a JSON file and supports additional storage backends such as MongoDB and Redis.
- **Caching**: Caches scraped data using Redis to avoid redundant updates.
- **Notifications**: Sends notifications upon completion of the scraping process via Slack or email.
- **Retry Mechanism**: Implements retry logic to handle temporary scraping failures.
- **Logging**: Logs events and errors to a file in a rotating log handler, stored in a `logs` directory.

## Installation

### Prerequisites

- Python 3.7+
- Redis (for caching)
- MongoDB (if using MongoDB as a storage backend)

### Step-by-Step Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/aparth33/scraper.git
   cd scraper

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install Dependencies: Install all required Python packages using the requirements.txt file**:
   ```bash
   pip3 install -r requirements.txt

4. **Environment Variables: Create a .env file in the project root to store environment variables:**:
   ```bash
   PORT=8000
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook/url
   GMAIL_USERNAME=your-email@gmail.com
   GMAIL_PASSWORD=your-email-password
Customize the variables as needed.

5. **Run the Application: Start the FastAPI application**:
   ```bash
   python3 run.py

## Usage
### Scraping API
The API provides an endpoint to initiate the scraping process:

- **Endpoint: `/scrape`**
- **Method: `GET`**
- **Parameters**:
    - ***`pages`***: (Optional) Number of pages to scrape. Example: ***`5`***.
    - ***`proxy`***: (Optional) Proxy URL to use for scraping.
- **Example Request**
    ```bash
    GET /scrape?pages=3&proxy=http://myproxy:8000

## Notifications
The application sends notifications upon the completion of the scraping process, which can be configured to use Slack or email.

## Logging
Logs are stored in the ***`logs`*** directory as ***`app.log`*** files. The log files are rotated to maintain a manageable size.

## Configuration
- **Storage Backends**: The project supports storing data in a local JSON file, MongoDB, or any other storage backend. You can configure the backend by modifying the Storage class in the code.
- **Cache**: The Redis cache is used to store previously scraped products to avoid redundant updates. This can be configured in the cache_product method.
## Development
### Run Tests
To run tests, you can use ***`pytest`***:
    ```bash
    pytest

## Contact
For any questions or issues, please contact agg09parth@gmail.com.

