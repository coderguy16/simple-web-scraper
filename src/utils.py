# def clean_price(price_str):
#     """Convert £10.24 → 10.24"""
#     return float(price_str.replace("£", ""))

import re

def clean_price(price_str):
    """Remove non-numeric characters and convert to float"""
    # Remove all non-digit/non-dot characters (e.g., Â, £)
    cleaned = re.sub(r"[^\d.]", "", price_str)
    return float(cleaned) if cleaned else 0.0  # Handle empty strings
def clean_rating(rating_classes):
    """Convert ['star-rating', 'Three'] → 3/5"""
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return ratings.get(rating_classes[1], 0)

def clean_stock(stock_str):
    """Convert 'In stock (22 available)' → 22"""
    import re
    match = re.search(r"\d+", stock_str)
    return int(match.group()) if match else 0
