## BUILDING COLLECTION

getIngredients(write = True)
getRecipeLinks(ingredients[304:], delay = 0, verbose = True)

## Load Ingredient List

with open("./ingredient_list.txt") as f:
    ingredients = [line.strip() for line in f if line.strip()]

## Load recipesAddresses

with open("./recipe_links.txt") as f:
    recipes_add = list(set([line.strip() for line in f if line.strip()]))

buildCollection(recipes_add, delay = 1)

# Make dictionary and add skipping list. Then create vocabulary and index.
rec_dic = recipeDict()  # 3.5 minuti
add_skip(rec_dic)
vocabulary(rec_dic)
index(rec_dic)
