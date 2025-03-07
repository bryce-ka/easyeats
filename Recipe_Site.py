from pymongo import MongoClient

class RecipeSite:
    
    def __init__(self, site_name, db):
        self.site_name = site_name
        self.collection = db[site_name] 
        self.recipe_links = self.read_recipe_file()
        self.failed_links = []

    def insert_one(self, recipe):
        """Insert a single recipe into the collection"""
        self.collection.insert_one(recipe)
    
    def insert_many(self, recipes):
        """Insert recipes into the collection"""
        self.collection.insert_many(recipes)
    
    def read_recipe_file(self):
        """read in recpie links from the sites file"""
        links_set = set()
        file_path = "site_files/"+self.site_name+".txt"
        try:
            with open(file_path, "r") as file:
                for line in file:
                    links_set.add(line.strip())
        except FileNotFoundError:
            print(f"⚠️ File {file_path} not found, initializing empty list.")
        return list(links_set)

    def get_all_recipes(self):
        """Retrieve all recipes"""
        return list(self.collection.find())