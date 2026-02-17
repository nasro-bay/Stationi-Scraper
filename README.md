# OuedKniss Car & Product Scraper

A robust Python-based web scraper for extracting detailed product listings and media from OuedKniss.com. This tool leverages the official GraphQL API to provide high-speed, structured data extraction for any category, including specialized support for car listings.

## 🚀 Key Features

- **GraphQL API Integration**: Direct communication with the backend for maximum speed and data accuracy.
- **Image Downloading**: Automatically downloads and organizes product images for every listing.
- **Smart Tracking System**: Remembers already scraped items using `scraped_ids.txt` to prevent duplicates and save bandwidth.
- **Automated Rate Limiting**: Intelligent delays between requests to ensure respectful scraping and avoid IP blocking.
- **Dynamic Specifications**: Automatically detects and maps technical fields (like Mileage, Year, Brand, etc.) into CSV columns.
- **Dual Extraction Modes**:
  - `MINI`: Speed-focused, fetches essential fields only.
  - `ALL`: Comprehensive details including store info, variants, and full media records.
- **Configurable Sessions**: Set a limit on how many items to scrape per execution (`LIMIT_PER_RUN`).

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/abdelhak-k/OuedKniss-Scraper.git
   cd ouedkniss-scraper
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 How to Use

### 1. Configure the Target
Open `settings.py` or `main.py` to adjust your scraping parameters.

- **Category Slug**: Identify your target in `main.py`. For example, `automobiles_vehicules` for cars.
- **Extraction Depth**: Set `TYPE = "ALL"` in `settings.py` if you need technical specs and images.
- **Throughput**: Adjust `LIMIT_PER_RUN` in `settings.py` (Default: 10 items).

### 2. Run the Scraper
```bash
python main.py
```

### 3. Review Results
- **CSV Data**: Saved as `ouedkniss_<category>_<timestamp>.csv`.
- **Media**: Downloaded into `downloads/announcement_<id>/`.
- **Persistence**: `scraped_ids.txt` will be updated with the processed IDs.

## ⚙️ Configuration (`settings.py`)

| Setting | Description | Recommended |
| :--- | :--- | :--- |
| `WAIT_TIME` | Delay between API requests | `0.5` seconds |
| `TYPE` | Deep or Shallow extraction | `"ALL"` for cars |
| `LIMIT_PER_RUN`| Max new items per execution | `10` or higher |
| `HEADER` | Browser User-Agent string | Keep updated |

## 📂 Project Structure

- `main.py`: Interactive entry point for the user.
- `scraper.py`: Coordinates the extraction, tracking, and image logic.
- `downloader.py`: Dedicated module for media handling and storage.
- `fetch_api.py`: Low-level GraphQL communication client.
- `utils.py`: Contains API payloads and persistence helpers.
- `process.py`: Logic for flattening nested API data into tabular CSV format.

## ⚠️ Important Considerations

- **Ethical Scraping**: Always use reasonable `WAIT_TIME` to protect the servers.
- **Data Privacy**: Ensure local compliance when handling user data (stores/usernames).
- **Maintenance**: GraphQL queries in `utils.py` may need updates if OuedKniss changes its API schema.

---
*Disclaimer: Use this tool responsibly. The authors are not responsible for any misuse or legal actions resulting from the use of this software.*
