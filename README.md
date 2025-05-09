# Linkedin_Detail_Extractor
LinkedIn Private API Scraper is a Python-based automation tool that extracts public information from LinkedIn profiles

🚀 LinkedIn Private API Scraper
This tool scrapes publicly visible LinkedIn profile information such as name, title, website, phone, and attempts to discover email addresses via a fallback using the Google Custom Search API.

It simulates the capabilities of tools like Apollo and ContactOut using browser automation and open web intelligence.

🔧 Features
✅ Scrapes LinkedIn profiles using Playwright and a logged-in session

✅ Extracts full name, job title, website, and phone number

✅ Opens and parses LinkedIn's "Contact info" modal

✅ If no email is found, it automatically:

Performs a Google search for the person

Extracts emails from search snippets using regex

✅ Outputs structured CSV file for easy enrichment or outreach

📁 Folder Structure
bash
Copy
Edit
linkedin_scraper/
├── linkedin_direct_scraper.py     # Main scraping script
├── login.py                       # Manual login launcher for session init
├── urls.txt                       # List of LinkedIn profile URLs
├── .env                           # Contains API keys for Google CSE
├── linkedin_user_data/           # Stores your login session (cookies)
└── linkedin_contacts_direct.csv   # Final output file
⚙️ Setup
1. Install Requirements
bash
Copy
Edit
pip install playwright beautifulsoup4 phonenumbers python-dotenv requests
playwright install
2. Save URLs
Create a file urls.txt with one LinkedIn profile per line:

ruby
Copy
Edit
https://www.linkedin.com/in/example1/
https://www.linkedin.com/in/example2/
3. Save Google API Keys
Create a .env file in the project folder:

env
Copy
Edit
GOOGLE_CSE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id
Get your keys via:

Google Programmable Search Engine

Google Cloud Console → Custom Search API

4. Log into LinkedIn (One-time Setup)
Run this once to initialize and save your session:

bash
Copy
Edit
python login.py
Log into LinkedIn manually in the opened Chromium browser. Your session will be saved to linkedin_user_data/.

▶️ Usage
Once setup is complete, run:

bash
Copy
Edit
python linkedin_direct_scraper.py
After scraping, results will be saved to linkedin_contacts_direct.csv.

🛡️ Disclaimer
This tool is for educational and research purposes only. Scraping LinkedIn content may violate their Terms of Service. Use responsibly and with permission.