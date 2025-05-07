#!/usr/bin/env python3
import asyncio
import argparse
import json
import os
import re
from pathlib import Path

import aiohttp
import aiofiles
from bs4 import BeautifulSoup

BASE_URL = 'https://www.ebay.com/sch/i.html?_ssn=garlandcomputer'

ITEM_ID_RE = re.compile(r'/itm/(\d+)')

def parse_items(html: str, condition_filter: str = None):
    soup = BeautifulSoup(html, 'html.parser')
    rows = []
    for li in soup.select('li.s-item'):
        title_tag = li.select_one('.s-item__info .s-item__title')
        link_tag  = li.select_one('.s-item__info a.s-item__link')
        cond_tag  = li.select_one('.s-item__subtitle .SECONDARY_INFO')

        title = title_tag.get_text(strip=True) if title_tag else None
        url   = link_tag['href'] if link_tag and link_tag.has_attr('href') else None
        cond  = cond_tag.get_text(strip=True) if cond_tag else None

        # apply condition filter if requested
        if condition_filter and (not cond or condition_filter.lower() not in cond.lower()):
            continue

        # extract numeric ID from URL
        m = ITEM_ID_RE.search(url or "")
        if not (title and url and cond and m):
            continue
        item_id = m.group(1)

        # price
        price_tag = li.select_one('.s-item__price')
        price = price_tag.get_text(strip=True) if price_tag else None

        rows.append({
            "ItemID": item_id,
            "Title": title,
            "Price": price,
            "ListingUrl": url,
            "Condition": cond
        })
    return rows

async def fetch_page(session, page_num):
    url = BASE_URL + (f"&_pgn={page_num}" if page_num > 1 else "")
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.text()

async def save_item(data_dir: Path, item: dict):
    file_path = data_dir / f"{item['ItemID']}.json"
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(item, ensure_ascii=False, indent=2))

async def crawl(start_page: int, max_pages: int, condition: str):
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for pg in range(start_page, start_page + max_pages):
            html = await fetch_page(session, pg)
            items = parse_items(html, condition_filter=condition)
            for item in items:
                tasks.append(save_item(data_dir, item))
        # fire off all writes concurrently
        await asyncio.gather(*tasks)
    print(f"✅ Saved {len(tasks)} items into {data_dir.resolve()}")

def main():
    p = argparse.ArgumentParser(
        description="Asynchronous eBay crawler for garlandcomputer store"
    )
    p.add_argument('--start-page', type=int, default=1,
                   help="First page to crawl (default: 1)")
    p.add_argument('--max-pages',  type=int, default=1,
                   help="How many pages to crawl (default: 1)")
    p.add_argument('--condition',   type=str, default=None,
                   help="Only include items whose condition contains this (e.g. 'New')")
    args = p.parse_args()

    asyncio.run(crawl(
        start_page=args.start_page,
        max_pages=args.max_pages,
        condition=args.condition
    ))

if __name__ == '__main__':
    main()
