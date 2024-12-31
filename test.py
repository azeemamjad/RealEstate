from redfin_scraper import RedfinScraper

scraper = RedfinScraper()
scraper.setup(zip_database_path="/Users/tahirsiddique/Desktop/RealEstate/zip_code_database.csv", multiprocessing=False)
city_states = ['Arizona']  
print(scraper.scrape(city_states, sold=False))