import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import os
from utils import clean_price, clean_rating, clean_stock

def scrape_all_books():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = []
    
    for page in tqdm(range(1, 51), desc="Scraping pages"):
        response = requests.get(base_url.format(page))
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        
        for book in soup.select("article.product_pod"):
            # Get book details from main listing
            title = book.select_one("h3 a")["title"]
            price = clean_price(book.select_one("p.price_color").text)
            rating = clean_rating(book.select_one("p.star-rating")["class"])
            
            # --- NEW: VISIT INDIVIDUAL BOOK PAGE FOR STOCK ---
            book_path = book.select_one("h3 a")["href"].replace("../../../", "")
            book_url = f"http://books.toscrape.com/catalogue/{book_path}"
            
            try:
                book_response = requests.get(book_url)
                book_soup = BeautifulSoup(book_response.text, "html.parser")
                stock_text = book_soup.select_one("p.availability").text.strip()
                stock = clean_stock(stock_text)
            except Exception as e:
                stock = 0  # Default if scraping fails
            
            all_books.append({
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Stock": stock
            })
            
            time.sleep(0.5)  # Be polite to the server
        
        time.sleep(1)  # Delay between pages
    df = pd.DataFrame(all_books)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/raw_books.csv", index=False)
    
    # Clean the data (example: filter out books with 0 ratings)
    cleaned_df = df[df["Rating"] > 0]  # Remove books with 0 ratings
    os.makedirs("output", exist_ok=True)
    cleaned_df.to_csv("output/cleaned_books.csv", index=False)
    
    return cleaned_df

def create_top_rated_report(cleaned_df):
    # Filter and sort top-rated books
    top_books = cleaned_df.sort_values(by=["Rating", "Price"], ascending=[False, True])
    top_books = top_books.head(10)  # Top 10
    
    # Create a polished Excel report
    with pd.ExcelWriter("outputs/top_rated_books.xlsx") as writer:
        top_books.to_excel(writer, index=False, sheet_name="Top Rated Books")
        
        # Access the worksheet to format
        worksheet = writer.sheets["Top Rated Books"]
if __name__ == "__main__":
    df = scrape_all_books()
    create_top_rated_report(df)  
    print("Scraping complete! Clean data saved to output/cleaned_books.csv. Top-rated report saved to outputs/top_rated_books.xlsx")
