import logging
import os
import re
import time
from urllib.parse import quote_plus

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class FlipkartScraper:
    """Collect product name, price, rating and product URL from Flipkart search results."""

    def __init__(self, product_name="laptops", pages=2, headless=False):
        self.product_name = product_name.strip()
        self.pages = max(1, int(pages))
        self.products = []
        self.logger = logging.getLogger(__name__)

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options,
        )
        self.wait = WebDriverWait(self.driver, 20)

    @staticmethod
    def _first_text(element, selectors):
        for selector in selectors:
            try:
                value = element.find_element(By.XPATH, selector).text.strip()
                if value:
                    return value
            except Exception:
                continue
        return ""

    @staticmethod
    def _first_attribute(element, selectors, attribute):
        for selector in selectors:
            try:
                value = element.find_element(By.XPATH, selector).get_attribute(attribute)
                if value:
                    return value.strip()
            except Exception:
                continue
        return ""

    @staticmethod
    def _extract_price(text):
        match = re.search(r"₹\s*[\d,]+(?:\.\d+)?", text or "")
        return match.group(0).replace(" ", "") if match else ""

    @staticmethod
    def _extract_rating(text):
        match = re.search(r"\b([0-5](?:\.\d)?)\b", text or "")
        return float(match.group(1)) if match else np.nan

    def _scroll_page(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(2)

    def _scrape_current_page(self):
        self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-id]"))
        )
        cards = self.driver.find_elements(By.XPATH, "//div[@data-id]")
        print(f"Cards found: {len(cards)}")

        title_selectors = [
            ".//div[contains(@class,'KzDlHZ')]",
            ".//div[contains(@class,'_4rR01T')]",
            ".//a[contains(@class,'s1Q9rs')]",
            ".//a[contains(@class,'wjcEIp')]",
            ".//a[@title]",
            ".//img[@alt]",
        ]
        price_selectors = [
            ".//div[contains(@class,'Nx9bqj')]",
            ".//div[contains(@class,'_30jeq3')]",
            ".//*[contains(text(),'₹')]",
        ]
        rating_selectors = [
            ".//div[contains(@class,'XQDdHH')]",
            ".//div[contains(@class,'_3LWZlK')]",
            ".//span[contains(@class,'Wphh3N')]",
        ]

        for card in cards:
            try:
                title = ""
                for selector in title_selectors:
                    try:
                        element = card.find_element(By.XPATH, selector)
                        title = (
                            element.get_attribute("alt").strip()
                            if selector.endswith(".//img[@alt]")
                            else element.text.strip()
                        )
                        if title:
                            break
                    except Exception:
                        continue

                raw_price = self._first_text(card, price_selectors)
                price = self._extract_price(raw_price)

                rating_text = self._first_text(card, rating_selectors)
                rating = self._extract_rating(rating_text)

                product_link = self._first_attribute(
                    card,
                    [".//a[@href]"],
                    "href",
                )

                if title and price:
                    product = {
                        "Product Name": title,
                        "Price": price,
                        "Rating": rating,
                        "Product Link": product_link,
                    }

                    if product not in self.products:
                        self.products.append(product)

            except Exception as exc:
                self.logger.warning("Card parsing failed: %s", exc)

    def _go_to_next_page(self):
        try:
            next_button = self.driver.find_element(
                By.XPATH,
                "//span[normalize-space()='Next']/ancestor::a[1]",
            )
            self.driver.execute_script(
                "arguments[0].click();",
                next_button,
            )
            time.sleep(4)
            return True
        except Exception:
            return False

    def scrape(self):
        """Scrape the requested number of search-result pages."""
        query = quote_plus(self.product_name)
        url = f"https://www.flipkart.com/search?q={query}"

        try:
            self.driver.get(url)
            time.sleep(4)

            for page in range(1, self.pages + 1):
                print(f"\nScraping page {page}/{self.pages}")
                self._scroll_page()

                try:
                    self._scrape_current_page()
                except TimeoutException:
                    print("Timed out waiting for product cards.")
                    break

                if page < self.pages and not self._go_to_next_page():
                    print("No more pages available.")
                    break

        except WebDriverException as exc:
            self.logger.exception("WebDriver error")
            print(f"Scraping failed: {exc}")

        finally:
            self.driver.quit()

        print(f"\nTotal unique products collected: {len(self.products)}")
        return self.products

    def save_data(self, output_path="data/flipkart_products.csv"):
        """Save scraped records to CSV and return the DataFrame."""
        if not self.products:
            print("No products scraped!")
            return None

        df = pd.DataFrame(self.products).drop_duplicates()

        df["Brand"] = (
            df["Product Name"]
            .astype(str)
            .str.split()
            .str[0]
        )
        df["Category"] = self.product_name

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        df.to_csv(output_path, index=False)

        print(f"\nCSV saved: {output_path}")
        print(f"Rows saved: {len(df)}")
        return df
