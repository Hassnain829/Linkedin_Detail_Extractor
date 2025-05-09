import os
from playwright.sync_api import sync_playwright

# Optional: make session directory customizable
SESSION_DIR = os.getenv("LINKEDIN_SESSION_DIR", "linkedin_user_data")

def main():
    with sync_playwright() as p:
        print("🔐 Opening Chromium browser for manual LinkedIn login...")
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            args=["--start-maximized"]
        )
        page = browser.new_page()
        page.goto("https://www.linkedin.com/login", timeout=60000)

        print("\n📝 Please log in manually. Once you're on your LinkedIn feed, close the browser window.")
        browser.wait_for_event("close")
        print(f"✅ Session saved to: {SESSION_DIR}")

if __name__ == "__main__":
    main()
