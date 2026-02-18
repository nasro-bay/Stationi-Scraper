import os
from settings import TRACKING_FILE

"""
Sync Downloads → scraped_ids.txt

Scans the 'downloads/' folder for all 'announcement_<id>' subdirectories,
extracts their IDs, and appends any missing ones to the tracking file.
This is useful for recovering state after a crash or manual download session.
"""

DOWNLOADS_DIR = "downloads"


def get_ids_from_downloads(downloads_dir: str) -> set:
    """
    Scans the downloads folder and extracts announcement IDs
    from directory names formatted as 'announcement_<id>'.

    Args:
        downloads_dir (str): Path to the downloads directory.

    Returns:
        set: A set of ID strings found in the downloads folder.
    """
    found_ids = set()

    if not os.path.exists(downloads_dir):
        print(f"Downloads folder '{downloads_dir}' does not exist. Nothing to sync.")
        return found_ids

    for entry in os.scandir(downloads_dir):
        if entry.is_dir() and entry.name.startswith("announcement_"):
            # Extract the ID part after 'announcement_'
            ann_id = entry.name[len("announcement_"):]
            if ann_id.isdigit():
                found_ids.add(ann_id)
            else:
                print(f"  Skipping unrecognized folder: {entry.name}")

    return found_ids


def load_existing_ids(tracking_file: str) -> set:
    """
    Reads already-tracked IDs from the tracking file.

    Args:
        tracking_file (str): Path to scraped_ids.txt.

    Returns:
        set: Set of ID strings already in the file.
    """
    if not os.path.exists(tracking_file):
        return set()
    with open(tracking_file, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())


def append_new_ids(tracking_file: str, new_ids: set):
    """
    Appends new IDs to the tracking file, one per line.

    Args:
        tracking_file (str): Path to scraped_ids.txt.
        new_ids (set): IDs to append.
    """
    with open(tracking_file, 'a', encoding='utf-8') as f:
        for ann_id in sorted(new_ids, key=lambda x: int(x)):
            f.write(f"{ann_id}\n")


if __name__ == "__main__":
    print("=" * 50)
    print("  Downloads → scraped_ids.txt Sync Tool")
    print("=" * 50)

    # Step 1: Scan downloads folder
    print(f"\n[1] Scanning '{DOWNLOADS_DIR}' folder...")
    downloaded_ids = get_ids_from_downloads(DOWNLOADS_DIR)
    print(f"    Found {len(downloaded_ids)} announcement folder(s).")

    if not downloaded_ids:
        print("\nNothing to sync. Exiting.")
        exit(0)

    # Step 2: Load existing tracked IDs
    print(f"\n[2] Loading existing IDs from '{TRACKING_FILE}'...")
    existing_ids = load_existing_ids(TRACKING_FILE)
    print(f"    {len(existing_ids)} IDs already tracked.")

    # Step 3: Compute the difference
    new_ids = downloaded_ids - existing_ids
    already_tracked = downloaded_ids & existing_ids

    print(f"\n[3] Comparison results:")
    print(f"    Already in tracking file : {len(already_tracked)}")
    print(f"    New IDs to add           : {len(new_ids)}")

    if not new_ids:
        print("\nAll downloaded IDs are already tracked. Nothing to do.")
        exit(0)

    # Step 4: Append new IDs
    print(f"\n[4] Appending {len(new_ids)} new ID(s) to '{TRACKING_FILE}'...")
    append_new_ids(TRACKING_FILE, new_ids)

    print(f"\n✅ Done! {len(new_ids)} ID(s) added to '{TRACKING_FILE}'.")
    print("   These announcements will be skipped in future scraping sessions.")
    print("=" * 50)
