'''
a script for webscrapaing from various recipie sites using https://github.com/hhursev/recipe-scrapers.

The goal of this program is to collect a catalog of recipies from across the web in a standardized format based on the package above. 
These recipies will be combined into a single database to be used by an application later on.
'''

from pymongo import MongoClient
from recipe_scrapers import SCRAPERS
from os import listdir as ls 
from Recipe_Site import RecipeSite 
# from recipe_scrapers import scrape_me
import random
import requests
from recipe_scrapers import scrape_html
import time
import os
# import proxies 
proxy_list = []
with open("working_proxies.txt") as file:
    for line in file:
        proxy_list.append(line)

# create mongo db and start thinking through the collections 
client = MongoClient()
db = client['recipe_db']

site_files = []
for file in ls("site_files"):
    if file[-3:] == "txt" and file != "proxies_list.txt":
        site_files.append(file)

site_objects = {site_name[:-4]: RecipeSite(site_name[:-4], db) for site_name in site_files}

def random_index(lst):
    """Return a random non zero index from the given list."""
    nonzero_indices = [i for i, val in enumerate(lst) if val != 0]  # Get indices of non-zero values
    if not nonzero_indices:  # Check if there are any non-zero values
        return None
    return random.choice(nonzero_indices)  # Pick a random non-zero index

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}


#number of links in each site
rps = [len(site_objects[key].recipe_links) for key in site_objects]
prev_sel = 0
while sum(rps) != 0:
    print(rps)
    # select random site 
    sel = random_index(rps)
    if sel is None:
        break 
    # update array 
    rps[sel]-=1
    # avoid http errors (hopefully)
    if sel == prev_sel:
        time.sleep(2)
    
    this_site = site_objects[list(site_objects.keys())[sel]]
    if this_site.recipe_links != []:
        this_link = this_site.recipe_links.pop()
        try:
            response = requests.get(this_link, headers=HEADERS, timeout=5)
            response.raise_for_status()
            html_content = response.text
            this_link_info = scrape_html(html_content, org_url = this_link)
            this_recipe = this_link_info.to_json()
            this_site.insert_one(this_recipe)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    os.system('cls' if os.name == 'nt' else 'clear')
    