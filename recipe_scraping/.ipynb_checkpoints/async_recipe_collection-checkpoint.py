import asyncio
import aiohttp
import random
import os
from pymongo import MongoClient
from os import listdir as ls
from Recipe_Site import RecipeSite
from recipe_scrapers import scrape_html

# MongoDB setup
client = MongoClient()
db = client['recipe_db']

# Load site files
site_files = [file for file in ls("site_files") if file.endswith(".txt") and file != "proxies_list.txt"]
site_objects = {site_name[:-4]: RecipeSite(site_name[:-4], db) for site_name in site_files}

# Async Headers & Semaphore (Limits concurrent requests)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
MAX_CONCURRENT_REQUESTS = 3  # Prevent overloading sites
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

# Function to get a random non-zero index
def random_index(lst):
    nonzero_indices = [i for i, val in enumerate(lst) if val != 0]
    return random.choice(nonzero_indices) if nonzero_indices else None

# Async function to scrape a recipe
async def scrape_recipe(session, this_site):
    """Scrapes a recipe from a site asynchronously and inserts it into MongoDB."""
    async with semaphore:
        if not this_site.recipe_links:
            return
        
        this_link = this_site.recipe_links.pop()
        try:
            async with session.get(this_link, headers=HEADERS, timeout=5) as response:
                response.raise_for_status()
                html_content = await response.text()
                
                # Parse and insert recipe
                this_link_info = scrape_html(html_content, org_url=this_link)
                this_recipe = this_link_info.to_json()
                this_site.insert_one(this_recipe)
                
                print(f"Inserted recipe from {this_link}")
        except Exception as e:
            print(f"Request failed: {e}")

# Main async function
async def main():
    """Main function that runs the scraping process asynchronously."""
    rps = [len(site_objects[key].recipe_links) for key in site_objects]
    
    async with aiohttp.ClientSession() as session:
        while sum(rps) > 0:
            print(rps)
            
            sel = random_index(rps)
            if sel is None:
                break  # Exit if all sites are processed
            
            # Reduce available recipe count
            rps[sel] -= 1
            
            # Select site and scrape
            this_site = site_objects[list(site_objects.keys())[sel]]
            asyncio.create_task(scrape_recipe(session, this_site))  # Non-blocking
            
            # Reduce rapid requests to the same site
            await asyncio.sleep(0.5)
        
        # Ensure all tasks complete before finishing
        await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})

# Run the async scraper
if __name__ == "__main__":
    asyncio.run(main())
