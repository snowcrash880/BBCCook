def parseRecipe(url):
    """
    Parse a recipe from http://www.bbc.co.uk/food.

    Parameters
    ----------
    url :
    Returns
    -------
    recipe : dict
        dictionary containing Title, Author, CookTime, Prep_Time, Serves,
        Description, Dietary, Ingredient_list, Instructions
    """

    r = requestURL(url)
    Soup = BeautifulSoup(r.text, "lxml")
    recipe = {}

    Title = Soup.find("meta", {"property":"og:title"})
    recipe["Title"] = Title.get("content") if Title else "Empty"

    Author = Soup.find("a", {"class":"chef__link"})
    recipe["Author"] = Author.text if Author else "Empty"

    CookTime = Soup.find("p", {"class":"recipe-metadata__cook-time"})
    recipe["CookTime"] = CookTime.text if CookTime else "Empty"

    Prep_Time = Soup.find("p", {"class":"recipe-metadata__prep-time"})
    recipe["Prep_Time"] = Prep_Time.text if Prep_Time else "Empty"

    Serves = Soup.find("p", {"class":"recipe-metadata__serving"})
    recipe["Serves"] = Serves.text if Serves else "Empty"

    Description = Soup.find("div", {"class":"recipe-description"})
    recipe["Description"] = Description.get_text(strip = True) if Description else "Empty"

    Dietary = Soup.find("div", {"class":"recipe-metadata__dietary"})
    recipe["Dietary"] = Dietary.get_text(strip = True) if Dietary else "Empty"


    ingredients_body = Soup.find_all("div", {"class":"recipe-ingredients"})[0]
    headers = []
    headers.extend([i.string for i in ingredients_body.find_all("h2")])
    headers.extend([i.string for i in ingredients_body.find_all("h3")])
    ingredients_sub = ingredients_body.find_all("ul")


    Ingredient_list = {}
    for i in range(len(ingredients_sub)):
        if len(headers) != len(ingredients_sub):
            Ingredient_list[headers[i+1]] = ["".join(j.strings)
                                            for j in ingredients_sub[i].find_all("li")]


        else:
            Ingredient_list[headers[i]] = ["".join(j.strings)
                                        for j in ingredients_sub[i].find_all("li")]




    recipe["Ingredient_list"] = Ingredient_list
    recipe["Instructions"] = ["".join(j.stripped_strings)
                            for j in Soup.find_all("li", {"itemprop":"recipeInstructions"})]



    return recipe


def recipeWrite(filename, recipe):
    '''Write recipe on disk as docID.txt'''

    header = ["Title", "Author", "CookTime", "Prep_Time",
             "Serves", "Description", "Dietary", "Ingredient_list",
             "Instructions"]
    s_first = "\t".join(["".join(recipe[i]) for i in header[:7] ])

    s_instr = "".join(recipe["Instructions"])
    s_ing = ""
    for key in recipe["Ingredient_list"].keys():
        s_ing = s_ing + "\t".join([i for i in recipe["Ingredient_list"][key]])

    s = s_first + "\t" + s_instr + "\t" + s_ing

    f = open(filename,"w")
    f.write(s)
    f.close()


def buildCollection(recipesAddresses, delay = 1, last_num = 0):
    """
    Parse every recipe on from http://www.bbc.co.uk/food.
    Each repice is written in a tab separated text file with
    a hierarchy of folders, in the folderPath.
    """
    if not os.path.exists("recipes"):
        os.makedirs("recipes")
    recipesAddresses = list(set(recipesAddresses))
    for url in recipesAddresses:
        #try: recipe = parseRecipe(url)
        #except:
        #    print("\nParsing error occurred. At: "+str(last_num)+"\n")
        #    return last_num
        recipe = parseRecipe(url)
        filename = "recipes/"+str(last_num).zfill(5)+".txt"
        recipeWrite(filename, recipe)
        print(str(last_num).zfill(5))
        last_num +=1
        time.sleep(delay)
    return last_num

