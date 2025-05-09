#!/usr/bin/env python3
"""
linkedin_direct_scraper.py: Scrape LinkedIn profiles for name, title, email, phone, and website using Playwright. If email is not found, use Google Custom Search API as fallback.

Requirements:
  pip install playwright beautifulsoup4 phonenumbers python-dotenv requests
  playwright install

Setup:
  1. Create urls.txt with LinkedIn profile URLs.
  2. Create .env file in the same directory with:
       GOOGLE_CSE_API_KEY=your_google_api_key
       GOOGLE_CSE_ID=your_custom_search_engine_id
  3. Run: python linkedin_direct_scraper.py
"""
import os
import csv
import time
import requests
import phonenumbers
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# --- Load config ---
load_dotenv()
GOOGLE_CSE_API_KEY = os.getenv("GOOGLE_CSE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

URL_FILE = "urls.txt"
OUTPUT_CSV = "linkedin_contacts_direct.csv"

# --- Helpers ---
def extract_phone_numbers(text, region="US"):
    phones = set()
    for m in phonenumbers.PhoneNumberMatcher(text, region):
        if phonenumbers.is_valid_number(m.number):
            phones.add(phonenumbers.format_number(m.number, phonenumbers.PhoneNumberFormat.E164))
    return list(phones)

def google_email_fallback(full_name, title):
    query = f'"{full_name}" "{title}" email contact site:*.com'
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_CSE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": 3
    }
    try:
        res = requests.get(url, params=params)
        items = res.json().get("items", [])
        for item in items:
            snippet = item.get("snippet", "")
            match = extract_emails(snippet)
            if match:
                return match[0]
    except Exception as e:
        print(f"⚠️ Google Search fallback error: {e}")
    return ''

def extract_emails(text):
    import re
    return re.findall(r"[\w\.-]+@[\w\.-]+", text)

def scrape_profile(page, url):
    page.goto(url, timeout=60000)
    time.sleep(3)
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')

    # Name
    h1 = soup.select_one('h1')
    name = h1.get_text().strip() if h1 else ''
    parts = name.split()
    first = parts[0] if parts else ''
    last = parts[-1] if len(parts) > 1 else ''
    full_name = f"{first} {last}"

    # Title
    title_el = soup.select_one('.text-body-medium.break-words')
    title = title_el.get_text().strip() if title_el else ''

    # Contact Info Modal Button
    contact_btn = page.locator("a:has-text('Contact info')")
    email = ''
    website = ''
    if contact_btn.is_visible():
        contact_btn.click()
        page.wait_for_timeout(1000)
        modal_html = page.content()
        modal_soup = BeautifulSoup(modal_html, 'html.parser')
        for a in modal_soup.select('a[href^="mailto:"]'):
            email = a.get_text().strip()
            break
        for a in modal_soup.select('a[href^="http"]'):
            if "linkedin.com" not in a.get("href"):
                website = a.get("href")
                break

    # Extract phone numbers from page
    phones = extract_phone_numbers(soup.get_text())

    # Fallback to Google CSE if email not found
    if not email and GOOGLE_CSE_API_KEY and GOOGLE_CSE_ID:
        email = google_email_fallback(full_name, title)

    return {
        'ProfileURL': url,
        'FirstName': first,
        'LastName': last,
        'Title': title,
        'Company': '',
        'Email': email,
        'Phone': phones[0] if phones else '',
        'Website': website
    }

# --- Main ---
def main():
    if not os.path.exists(URL_FILE):
        print(f"⛔ {URL_FILE} not found. Create it with LinkedIn URLs, one per line.")
        return

    with open(URL_FILE) as f:
        urls = [u.strip() for u in f if u.strip()]
    if not urls:
        print("⛔ No URLs to process.")
        return

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir='linkedin_user_data', headless=False, slow_mo=150
        )
        page = browser.new_page()
        for url in urls:
            print(f"Processing: {url}")
            try:
                result = scrape_profile(page, url)
                results.append(result)
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")
        browser.close()

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'ProfileURL','FirstName','LastName','Title','Company','Email','Phone','Website'
        ])
        writer.writeheader()
        writer.writerows(results)
    print(f"✅ Saved {len(results)} records to {OUTPUT_CSV}")

if __name__ == '__main__':
    main()
