import requests
from bs4 import BeautifulSoup
import time
import random
import json
from datetime import datetime
import os

class IrecommendScraper:
    def __init__(self):
        self.base_url = "https://irecommend.ru"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.reviews = []
        
    def get_book_reviews(self, book_url, max_reviews=200):
        """Scrape reviews for a specific book"""
        page = 1
        while len(self.reviews) < max_reviews:
            url = f"{book_url}?page={page}"
            print(f"Scraping page {page}...")
            
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all review elements
                review_elements = soup.find_all('div', class_='reviewItem')
                
                if not review_elements:
                    print("No more reviews found.")
                    break
                
                for review in review_elements:
                    if len(self.reviews) >= max_reviews:
                        break
                        
                    try:
                        # Extract review data
                        title = review.find('h2', class_='reviewTitle').text.strip()
                        text = review.find('div', class_='reviewText').text.strip()
                        rating = len(review.find_all('span', class_='active'))
                        date = review.find('span', class_='reviewDate').text.strip()
                        author = review.find('a', class_='userName').text.strip()
                        
                        review_data = {
                            'title': title,
                            'text': text,
                            'rating': rating,
                            'date': date,
                            'author': author
                        }
                        
                        self.reviews.append(review_data)
                        print(f"Collected review {len(self.reviews)}: {title[:50]}...")
                        
                    except Exception as e:
                        print(f"Error processing review: {e}")
                        continue
                
                # Add random delay to avoid being blocked
                time.sleep(random.uniform(2, 5))
                page += 1
                
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                break
    
    def save_reviews(self, filename):
        """Save collected reviews to a JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.reviews, f, ensure_ascii=False, indent=4)
        
        print(f"Saved {len(self.reviews)} reviews to {filename}")

def main():
    # Example book URLs from irecommend.ru
    book_urls = [
        "https://irecommend.ru/content/1984-dzhordzh-oruell",
        "https://irecommend.ru/content/master-i-margarita-mikhail-bulgakov",
        "https://irecommend.ru/content/prestuplenie-i-nakazanie-fedor-dostoevskii"
    ]
    
    scraper = IrecommendScraper()
    
    for url in book_urls:
        print(f"\nScraping reviews from: {url}")
        scraper.get_book_reviews(url, max_reviews=70)  # Get ~70 reviews per book
    
    # Save all collected reviews
    scraper.save_reviews("book_reviews")

if __name__ == "__main__":
    main() 