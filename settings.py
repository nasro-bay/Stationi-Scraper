"""
Configuration settings for the OuedKniss Scraper.
Adjust these values to control the scraper's behavior, rate limiting, and extraction depth.
"""

# The GraphQL endpoint for OuedKniss
API_URL = "https://api.ouedkniss.com/graphql"


# Headers to mimic a real browser session and avoid bot detection
HEADER = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Extraction settings
COUNT= 60 # Number of items per page (60 is the API maximum)
TRIES=3 # Number of retry attempts for failed network requests
WAIT_TIME_RETRY=3 # Seconds to wait between retry attempts
WAIT_TIME= 0.5 # Delay between consecutive requests (Recommended: 0.2 - 0.5s to avoid IP blocking)

# Extraction Mode:
# "MINI" = Essential fields only (faster, less bandwidth)
# "ALL"  = Full details including all technical specifications (slower, comprehensive)
TYPE= "ALL" 

# Persistence and Tracking
# This file stores IDs of already scraped announcements to prevent duplicates
TRACKING_FILE = "scraped_ids.txt"

# Limit the number of new announcements processed in a single execution
LIMIT_PER_RUN = 100