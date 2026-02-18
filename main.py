from scraper import scrape_ouedkniss

"""
Main Application Entry Point.
Configure the target category and execution limits here.
"""

if __name__ == "__main__":
    # TARGET CATEGORY: 'automobiles_vehicules' for car listings.
    # To find other slugs, inspect network requests on ouedkniss.com
    target_category = "automobiles_vehicules"
    
    # MAX PAGES: Limit how many initial pages the scraper scans for IDs.
    # Note: The actual processing limit is controlled by LIMIT_PER_RUN in settings.py
    # Change to None to scan the entire category catalog.
    max_scan_pages = 10  # None = scan ALL pages in the category
    
    print(f"--- Starting OuedKniss Scraper Session ---")
    print(f"Target: {target_category}")
    
    # Execute the scraper
    result_file = scrape_ouedkniss(category_slug=target_category, max_pages=max_scan_pages)
    
    if result_file:
        print(f"\nSession Complete. Data exported to: {result_file}")
    else:
        print("\nSession ended with no new data processed.")
