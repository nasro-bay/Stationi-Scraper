import requests
import time
from settings import *
from utils import get_payload_search

"""
API Client for OuedKniss GraphQL.
Handles searching for IDs and fetching full announcement details.
"""

# Dynamic import of detail payload structure
if TYPE=="MINI":
    from utils import get_payload_post_mini as get_payload_post
elif TYPE=="ALL":
    from utils import get_payload_post_all as get_payload_post

class OuedKnissAPI:
    def __init__(self):
        self.api_url = API_URL
        self.headers = HEADER


    def get_announcement_ids_from_pages(self, category_slug, max_pages=None):
        """
        Scans OuedKniss category pages to build a list of announcement IDs.
        
        Args:
            category_slug (str): The category to scan.
            max_pages (int, optional): Max pages to scan. If None, scans until end.
            
        Returns:
            set: Unique set of announcement IDs.
        """
        # If max_pages is not provided, fetch the first page to determine the total page count
        if not max_pages:
            payload = get_payload_search(category_slug, 1)
            try:
                response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=30)
                paginator = response.json()["data"]["search"]["announcements"]["paginatorInfo"]
                max_pages = paginator.get("lastPage", 1)
            except Exception as e:
                print("Could not fetch initial page info, retrying might be necessary.")
                print(e)

        all_ids = set()
        
        print(f"Starting ID extraction across {max_pages} pages...")
        for page in range(1, max_pages + 1):        
            print(f"Scanning Page {page}...")
            
            payload = get_payload_search(category_slug, page)
            
            # Implementation of the retry logic for network stability
            for attempt in range(TRIES):  
                try:
                    response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=15)
                    break
                except Exception as e:
                    print(f"Error on page {page} (attempt {attempt + 1}/{TRIES}): {e}")
                    
                    if attempt < TRIES - 1:
                        time.sleep(WAIT_TIME_RETRY)
                    else:
                        print(f"Failed to fetch page {page} after {TRIES} attempts.")
                        continue

            if response.status_code != 200:
                print(f"Skip: HTTP {response.status_code} on page {page}.")
                continue
            
            try:
                data = response.json()
                announcements = data["data"]["search"]["announcements"]["data"]
                
                if not announcements:
                    print(f"End of data reached at page {page}.")
                    break                

                # Collect IDs from the current page
                for announcement in announcements:
                    all_ids.add(announcement["id"])
                
                # Dynamic pagination check
                paginator = data["data"]["search"]["announcements"]["paginatorInfo"]
                has_more = paginator.get("hasMorePages", False)
                
                print(f"Progress: {len(all_ids)} IDs found so far.")
                
                if not has_more:
                    break
            
                time.sleep(WAIT_TIME)
                
            except (KeyError, TypeError) as e:
                print(f"Data format error on page {page}: {e}")
                
        print(f"ID extraction completed. {len(all_ids)} total unique IDs found.")
        return all_ids


    def get_announcement_details(self, ann_id):
        """
        Fetches full details for a single announcement ID.
        
        Args:
            ann_id (str): The announcement ID.
            
        Returns:
            dict: Parsed announcement data.
        """
        payload = get_payload_post(ann_id)
        
        for attempt in range(TRIES):
            try:
                response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=10)
                
                if response.status_code != 200:
                    print(f"Error for ID {ann_id}: HTTP {response.status_code}")
                    return None
                
                return response.json()["data"]["announcement"]
                
            except Exception as e:
                print(f"Connection error for ID {ann_id} (attempt {attempt + 1}/{TRIES}): {e}")
                if attempt < TRIES - 1:
                    time.sleep(WAIT_TIME_RETRY)
                else:
                    return None
