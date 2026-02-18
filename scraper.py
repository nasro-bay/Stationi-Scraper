from datetime import datetime
import time
from fetch_api import OuedKnissAPI
from settings import *
from downloader import download_announcement_images
from utils import load_scraped_ids, save_scraped_id

"""
Core Scraper Engine.
Coordinates API fetching, data processing, persistence, and image downloading.
"""

# Dynamic component loading based on extraction depth (see settings.py)
if TYPE=="MINI":
    from process import CSVManagerMini as CSVManager, DataProcessorMini as DataProcessor
elif TYPE=="ALL":
    from process import CSVManagerALl as CSVManager, DataProcessorAll as DataProcessor


def scrape_ouedkniss(category_slug: str, max_pages:int = None) -> str:
    """
    Main entry point for scraping OuedKniss categories.
    
    Args:
        category_slug (str): The OuedKniss category identifier.
        max_pages (int, optional): Limit on how many pages to scan. 
                                   None scans all available pages.
    
    Returns:
        str: The filename of the generated CSV, or None on failure.
    """
    # Initialize API connector and Data Processor
    api = OuedKnissAPI()
    processor = DataProcessor()
    
    # Step 1: Initialize Persistence (Skip duplicates)
    scraped_ids = load_scraped_ids(TRACKING_FILE)
    print(f"Loaded {len(scraped_ids)} already scraped IDs from {TRACKING_FILE}.")
    
    try:
        # Step 2: Fetch Announcement IDs
        print(f"Fetching announcement IDs for category: {category_slug}...")
        announcement_ids = api.get_announcement_ids_from_pages(category_slug, max_pages)
        print(f"Found {len(announcement_ids)} total announcement IDs in category.")
        
        # Filter: Keep only IDs we haven't seen before
        new_announcement_ids = [aid for aid in announcement_ids if str(aid) not in scraped_ids]
        print(f"Filtered: {len(new_announcement_ids)} new announcements found.")
        
        # Filter: Keep only announcements with even IDs
        new_announcement_ids = [aid for aid in new_announcement_ids if int(aid) % 2 == 1]
        print(f"Even-ID filter applied: {len(new_announcement_ids)} announcements remaining.")
        
        # Apply per-run throughput limit (see settings.py)
        # If LIMIT_PER_RUN is None, process ALL new announcements
        if LIMIT_PER_RUN is not None:
            target_ids = new_announcement_ids[:LIMIT_PER_RUN]
        else:
            target_ids = new_announcement_ids
        print(f"Processing {len(target_ids)} announcements for this session (limit: {'None (ALL)' if LIMIT_PER_RUN is None else LIMIT_PER_RUN}).")
        
        if not target_ids:
            print("No new announcements to process. Exiting.")
            return None

        # Step 3: Collect full data and download images
        print("Collecting announcement details and media...")
        all_raw_data = []
        processed_ids = []
        
        for i, ann_id in enumerate(target_ids):
            print(f"Fetching {i+1}/{len(target_ids)}: ID {ann_id}")
            raw_data = api.get_announcement_details(ann_id)
            if not raw_data:
                continue
                
            all_raw_data.append(raw_data)
            
            # Sub-process: Download car/product images
            if raw_data.get("medias"):
                download_announcement_images(ann_id, raw_data["medias"])
            
            # Mark as processed only if details were fetched
            processed_ids.append(ann_id)
                
            # Internal rate limiting between detail requests
            time.sleep(WAIT_TIME)
        
        # Step 4: Metadata analysis (Detect unique technical specifications)
        # This allows us to handle dynamic car specs like "Kilométrage" or "Brand"
        print("Analyzing specifications for tabular alignment...")
        all_spec_labels = processor.collect_all_specs(all_raw_data)
        
        # Step 5: Export to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ouedkniss_{category_slug.replace('-', '_')}_{timestamp}.csv"
        csv_manager = CSVManager(filename, all_spec_labels)
        csv_manager.open()
        
        print(f"Processing data and writing to {filename}...")
        processed_data_list = []
        
        for raw_data in all_raw_data:
            processed_data = processor.process_announcement(raw_data, all_spec_labels)
            if processed_data:
                processed_data_list.append(processed_data)
        
        written_count = csv_manager.write_rows(processed_data_list)
        csv_manager.close()
        
        # Step 6: Commit persistence
        # Only save IDs to tracking file AFTER successful CSV write
        print("Updating tracking records...")
        for aid in processed_ids:
            save_scraped_id(TRACKING_FILE, aid)
        
        print(f"\nSuccessfully processed {written_count} announcements.")
        return filename
        
    except Exception as e:
        print(f"Critical Error in scraping flow: {e}")
        return None
