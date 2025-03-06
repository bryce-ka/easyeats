'''
a parallel computing script for webscrapaing from various recipie sites using https://github.com/hhursev/recipe-scrapers.

The goal of this program is to collect a catalog of recipies from across the web in a standardized format based on the package above. 
These recipies will be combined into a single database to be used by an application later on.
'''

import aiohttp
import asyncio
from pymongo import MongoClient
from recipe_scrapers import SCRAPERS



# import proxies 
proxy_list = []
with open("working_proxies.txt") as file:
    for line in file:
        proxy_list.append(line)

# create mongo db and start thinking through the collections 
client = MongoClient()
db = client['recipe_db']

# add collection per site via  f"{site_name}_recipes" = db[f"{site_name}"]
urls = list(SCRAPERS.keys())

for url in urls:
    f"{url}_recipes" = db[f"{url}"]
    

    


# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.text()[:100]

# async def main():
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch(session, url) for url in urls]
#         results = await asyncio.gather(*tasks)  # Runs all requests concurrently
#         print(results)

# asyncio.run(main())
