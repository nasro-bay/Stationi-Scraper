import os
import shutil

"""
Merge Images → Tsawer/

Flattens all images from every 'downloads/announcement_<id>/' subfolder
into a single 'Tsawer/' directory.

Each image is renamed to '<announcement_id>_<original_filename>'
to avoid name collisions between posts.
"""

DOWNLOADS_DIR = "downloads"
OUTPUT_DIR = "Tsawer"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff"}


def merge_images(downloads_dir: str, output_dir: str):
    """
    Walks through all announcement subfolders in downloads_dir
    and copies every image into output_dir with a prefixed filename.

    Args:
        downloads_dir (str): Path to the downloads folder.
        output_dir (str): Path to the destination Tsawer folder.
    """
    if not os.path.exists(downloads_dir):
        print(f"❌ Downloads folder '{downloads_dir}' not found. Nothing to merge.")
        return

    # Create output folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output folder ready: '{output_dir}'")

    total_copied = 0
    total_skipped = 0
    total_folders = 0

    for entry in sorted(os.scandir(downloads_dir), key=lambda e: e.name):
        if not entry.is_dir() or not entry.name.startswith("announcement_"):
            continue

        ann_id = entry.name[len("announcement_"):]
        total_folders += 1

        images_in_folder = 0
        for filename in sorted(os.listdir(entry.path)):
            ext = os.path.splitext(filename)[1].lower()
            if ext not in IMAGE_EXTENSIONS:
                continue

            src_path = os.path.join(entry.path, filename)
            # Prefix with announcement ID to avoid collisions
            dest_filename = f"{ann_id}_{filename}"
            dest_path = os.path.join(output_dir, dest_filename)

            if os.path.exists(dest_path):
                total_skipped += 1
                continue

            shutil.copy2(src_path, dest_path)
            images_in_folder += 1
            total_copied += 1

        if images_in_folder > 0:
            print(f"  ✅ [{ann_id}] Copied {images_in_folder} image(s).")
        else:
            print(f"  ⚠️  [{ann_id}] No new images to copy.")

    print()
    print("=" * 50)
    print(f"  Merge Complete!")
    print(f"  Folders scanned : {total_folders}")
    print(f"  Images copied   : {total_copied}")
    print(f"  Already existed : {total_skipped}")
    print(f"  Output location : {os.path.abspath(output_dir)}")
    print("=" * 50)


if __name__ == "__main__":
    print("=" * 50)
    print("  Downloads → Tsawer Image Merge Tool")
    print("=" * 50)
    print()
    merge_images(DOWNLOADS_DIR, OUTPUT_DIR)
