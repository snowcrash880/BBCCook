import requests
import time


def requestURL(url):
    '''Request routine to url. Catch errors and keep the connection active'''
    while True:
        try:
            r = requests.get(url, timeout = 5)
            r.raise_for_status()

        except requests.Timeout:
            print("\nTimeout!\n")
            continue

        except requests.ConnectionError:
            print("\nConnectionError!\n")
            continue

        except requests.HTTPError:
            print("\nHTTPError!\n")
            continue
        break
    return r


def getIngredients(delay = 1, write = False):
    '''Explore the bbc site to capture all ingredients.
    If write is True, the ingredient list is written in ingredient_list.txt.
    '''

    BASE_URL = "http://www.bbc.co.uk"
    r = requestURL(BASE_URL+"/food/ingredients")

    Soup = BeautifulSoup(r.text,"lxml")

    p = re.compile("/food/ingredients/by/letter/*") # create regular expression
    ing_pag = [BASE_URL+i.get("href") for i in Soup.find_all("a", {"href" :p})]

    ingredients = []
    for link in ing_pag:
        r = requestURL(link)
        Soup = BeautifulSoup(r.text,"lxml")
        l = [
            i.get("id") for i
            in Soup.find_all("li", {"class":"resource food"})]
        ingredients.extend(l)
        time.sleep(delay)
    if write:    # optionally write the ingredient-list on file
        with open("ingredient_list.txt", "w") as f:
            for ing in ingredients:
                f.write(ing+"\n")
    else:
        return ingredients


def extractRecipe(ingredient, l, delay = 0, verbose = False):
    '''Extract all recipes addresses from one ingredient. The
    url are saved in l list.'''

    BASE_URL = "http://www.bbc.co.uk"
    ingredient = "+".join(re.split("_", ingredient))
    url = BASE_URL+"/food/recipes/search?&keywords="+ingredient

    r = requestURL(url)


    Soup = BeautifulSoup(r.text, "lxml")

    p = re.compile("/food/recipes/search*")
    Next_page = Soup.find_all("a", {"href":p})
    if Next_page == [] : pages_number = 1
    else: pages_number = max([int(i.string) for i in Next_page if i.string != "Next"])

    p = re.compile("/food/recipes/*") # reg express

    if verbose: print("< "+ingredient+" > Start fetching. Page: ") # verbose

    for page in range(1,pages_number+1):
        r = requestURL(BASE_URL+"/food/recipes/"+"search?page="+str(page)+"&keywords="+ingredient)
        Soup = BeautifulSoup(r.text, "lxml")
        l_temp = [BASE_URL+i.get("href") for i in Soup.find_all("a", {"href":p})if "search" not in i.get("href")
                 if len(BASE_URL)+1 < len(i.get("href"))
                ]
        l.extend(l_temp)
        if verbose: print(page, end = " ")
        time.sleep(delay)


def getRecipeLinks(ingredients, delay = 1, verbose = False):
    """
    Starting from a list of ingredients crawls http://www.bbc.co.uk/food
    to collect all linked recipes links.

    Parameters
    ----------
    ingredients : list of str
    delay : int
        seconds of delay between requests to site
    """
    for ingredient_name in ingredients:
        recipes_address = []
        extractRecipe(ingredient_name, recipes_address, delay, verbose)
        f = open("recipe_links.txt", "a")
        for add in recipes_address:
            f.write(add+"\n")
        if verbose: print("< "+ingredient_name+" > complete!")
        f.close()


