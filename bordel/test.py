import cloudscraper
from bs4 import BeautifulSoup
import time
import re


def search_discord_servers(BASE_URL, CATEGORY, MAX_PAGES, DELAY, MAX_MEMBERS):
    scraper = cloudscraper.create_scraper()
    
    def scrape_listing_page(category, page=1):
        url = f"{BASE_URL}/browse/{category}?page={page}"
        print(f"Scraping listing: {url}")
        res = scraper.get(url)
        if res.status_code != 200:
            print(f"Error during the request on {url}")
            return []
    
        soup = BeautifulSoup(res.text, "html.parser")
        results = []
    
        # Each server is in a block <a href="/server/...">
        for server_block in soup.find_all("a", href=lambda href: href and href.startswith("/server/")):
            title = server_block.find("div", class_="text-lg font-semibold")
            description = server_block.find("p")
            server_url = BASE_URL + server_block["href"]
            results.append({
                "name": title.text.strip() if title else "N/A",
                "url": server_url,
                "description": description.text.strip() if description else ""
            })
    
        return results
    
    def scrape_server_details(server):
        print(f"Scraping server page: {server['url']}")
        res = scraper.get(server["url"])
        if res.status_code != 200:
            print(f"Error during the request on {server['url']}")
            return server
    
        soup = BeautifulSoup(res.text, "html.parser")
    
        # Extract the Discord invitation link (Join button)
        invite_link = None
        join_button = soup.find("button", class_="Button_btn__uiLDq Button_small__KpkXO Button_cta__rDW1i")
        if join_button:
            invite_link = server["url"]  # The Join button does not always contain the href, so we keep the current page
    
        # Extract the number of online users
        online_count = None
        user_icon = soup.find("svg", {"data-icon": "users"})
        if user_icon:
            parent = user_icon.find_parent("span")
            if parent and parent.text:
                online_count = re.search(r"\d[\d ,.]*", parent.text)
                if online_count:
                    online_count = online_count.group(0).replace(" ", "").replace(",", "")
    
        # No total members clearly available, so we can leave it empty
        total_members = "Not indicated"
    
        server["invite"] = invite_link or "Not available"
        server["online"] = online_count or "Not available"
        server["members"] = total_members
        return server
    
    
    
    # Step 1: Scrape the listing pages
    all_servers = []
    for page in range(1, MAX_PAGES + 1):
        servers = scrape_listing_page(CATEGORY, page)
        all_servers.extend(servers)
        time.sleep(DELAY)
    
    # Step 2: Scrape the details of each server
    detailed_servers = []
    for server in all_servers:
        detailed = scrape_server_details(server)
        detailed_servers.append(detailed)
        time.sleep(DELAY)
    
    # Display the results
    for server in detailed_servers:
      if int(server["online"]) <= MAX_MEMBERS:
        print(f"\n🧷 {server['name']}")
        print(f"🔗 Page: {server['url']}")
        print(f"📄 Description: {server['description']}")
        print(f"🔗 Invitation: {server['invite']}")
        print(f"👥 Online members: {server['online']}")
        print(f"👥 Total members: {server['members']}")

BASE_URL = "https://discordservers.com"
CATEGORY = "gaming"  # Replace with the desired category
MAX_PAGES = 1        # Number of pages to scrape
DELAY = 0.5          # Delay between requests to avoid blocking
MAX_MEMBERS = 1000   # Maximum number of members to filter servers

search_discord_servers(BASE_URL, CATEGORY, MAX_PAGES, DELAY, MAX_MEMBERS)
#last line