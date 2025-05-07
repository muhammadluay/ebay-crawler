# eBay Seller Crawler

An asynchronous Python crawler that scrapes items from a specified eBay seller. By default, it targets **garlandcomputer**, but you can point it at any seller by updating the `BASE_URL` in `crawler2.py`.

This repo contains:

* **crawler2.py** — the main crawler script
* **README.md** — usage instructions and examples


## Features

* **Async HTTP requests** with `aiohttp`
* **Async file writes** with `aiofiles`
* **Pagination** via `--start-page` and `--max-pages`
* **Condition filtering** via `--condition` (e.g. "New", "Pre-Owned")
* **JSON output**: one file per item, named `{ITEM_ID}.json`


## Prerequisites

* Python 3.7+
* `pip` package manager


## Installation

```bash
# clone your fork or the official repo
git clone https://github.com/muhammadluay/ebay-crawler.git
cd ebay-crawler

# install dependencies
pip install aiohttp aiofiles beautifulsoup4
```


## Configuration

Open **crawler2.py** and locate the `BASE_URL` constant near the top:

```python
BASE_URL = 'https://www.ebay.com/sch/i.html?_ssn=garlandcomputer'
```

Replace the seller ID (`garlandcomputer`) with any valid eBay seller name to crawl their listings.


## Usage

```bash
python crawler2.py [--start-page N] [--max-pages M] [--condition CONDITION]
```

| Option         | Description                                          | Default |
| -------------- | ---------------------------------------------------- | ------- |
| `--start-page` | First page to crawl                                  | `1`     |
| `--max-pages`  | Number of pages to crawl                             | `1`     |
| `--condition`  | Filter listings whose condition contains this string | *none*  |

### Examples

* **Crawl page 1** (all conditions) from default seller:

  ```bash
  python crawler2.py
  ```

* **Crawl pages 1–3** for **New** items only:

  ```bash
  python crawler2.py --max-pages 3 --condition New
  ```

* **Switch to another seller** (e.g. `mySeller123`):

  1. Edit `BASE_URL` in `crawler2.py` to:

     ```python
     BASE_URL = 'https://www.ebay.com/sch/i.html?_ssn=mySeller123'
     ```
  2. Run:

     ```bash
     python crawler2.py --start-page 2 --max-pages 3
     ```


## Output

All items are saved under `data/` as individual JSON files:

```
data/
├── 234908325972.json
├── 376214302926.json
└── 235718537637.json
```

Each JSON file structure:

```json
{
  "ItemID": "234908325972",
  "Title": "Example Item Title",
  "Price": "$199.99",
  "ListingUrl": "https://www.ebay.com/itm/234908325972?...",
  "Condition": "Pre-Owned"
}
```
