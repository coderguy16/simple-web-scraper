## 📚 Books to Scrape - Web Scraper
**Automates extraction of book details (titles, prices, ratings, and stock)**  

### Features
- Scrapes 1000 books across 50 pages from [books.toscrape.com](http://books.toscrape.com)
- Ethical delays between requests  
- Data cleaning and export to CSV/Excel  
- Sample reports: `outputs/top_rated_books.xlsx` `outputs/cleaned_books.csv`  

### Tech Stack
- Python, BeautifulSoup, pandas  
- Progress tracking with `tqdm`

## 📥 Installation & Usage
```bash
# Clone repo
git clone https://github.com/coderguy16/simple-web-scraper.git

# Change directory
cd simple-web-scraper
# Set up environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Scrape data from website
python src/scraper.py
