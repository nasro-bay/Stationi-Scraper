import os
import requests
import time
from settings import HEADER, WAIT_TIME

def download_announcement_images(ann_id, media_list):
    """
    Downloads and organizes images for a specific announcement.
    
    Args:
        ann_id (str): The unique identifier for the announcement.
        media_list (list): A list of media dictionaries from the API containing 'mediaUrl'.
    """
    if not media_list:
        return
    
    # Define and create the destination directory
    base_dir = "downloads"
    ann_dir = os.path.join(base_dir, f"announcement_{ann_id}")
    
    if not os.path.exists(ann_dir):
        os.makedirs(ann_dir, exist_ok=True)
        print(f"Created directory: {ann_dir}")
    else:
        # Optimization: Skip if images are already present
        existing_files = os.listdir(ann_dir)
        if len(existing_files) >= len(media_list):
            print(f"Images already exist for ID {ann_id}, skipping.")
            return

    # Iterate and download each media asset
    for i, media in enumerate(media_list):
        url = media.get("mediaUrl")
        if not url:
            continue
        
        # Determine file extension (defaulting to .jpg)
        ext = ".jpg"
        url_no_params = url.split("?")[0] if "?" in url else url
            
        if url_no_params.lower().endswith((".png", ".jpeg", ".webp", ".jpg")):
            ext = os.path.splitext(url_no_params)[1]
            
        file_path = os.path.join(ann_dir, f"image_{i+1}{ext}")
        
        # Avoid redownloading existing individual files
        if os.path.exists(file_path):
            continue

        print(f"  Downloading image {i+1}/{len(media_list)} for ID {ann_id}...")
        try:
            # Use stream=True for large files to keep memory usage low
            response = requests.get(url, headers=HEADER, stream=True, timeout=15)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            else:
                print(f"  Failed to download image: HTTP {response.status_code}")
                
            # Respectful delay between media downloads to prevent rate limiting
            time.sleep(WAIT_TIME)
            
        except Exception as e:
            print(f"  Error downloading image {url}: {e}")

if __name__ == "__main__":
    # Simple test case for independent verification
    test_media = [{"mediaUrl": "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"}]
    download_announcement_images("test_id", test_media)
