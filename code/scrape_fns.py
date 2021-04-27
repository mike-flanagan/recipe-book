def scrape(recipe_url):
    """
    This function takes a URL link to a recipe and, using the imported recipe-scrapers package, 
    adds the scraped content to a dictionary.
    
    To use this function, please first install the package and run the following import statement:
        pip install recipe-scrapers
        from recipe_scrapers import scrape_me    
    """
    scraper = scrape_me(recipe_url)
    
    title = scraper.title()
    total_time = scraper.total_time()
    yields = scraper.yields()
    ingredients = scraper.ingredients()
    instructions = scraper.instructions()
    image = scraper.image()
    host = scraper.host()
    links = scraper.links()
    nutrients = scraper.nutrients()
    
    recipe_dict = {
        'title': title,
        'cooktime': total_time,
        'yields': yields,
        'ingredients': ingredients,
        'instructions': instructions,
        'nutrients': nutrients,
        'image': image,
        'host': host,
        'links': links
    }
    return recipe_dict


def collect_urls(recipe_url):
    """
    This function takes a URL link to a recipe and, using the imported recipe-scrapers package, 
    adds the weblinks from the scraped content's webpage to a list.
    """
    recipe_dict = scrape(recipe_url)
    urls_list = []
    for i in recipe_dict['links']:
        if i['href'][:30] == '//www.foodnetwork.com/recipes/' and i['href'] not in urls_list and i['href'][30:36] != ['photos'] and i['href'][30:38] != ['packages']:
            urls_list.append(i['href'])
        else:
            continue
    return urls_list

