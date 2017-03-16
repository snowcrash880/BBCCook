
def retrieveRecipe(rec_num):
    '''Retrieve a recipe from the disk give the recipe number.'''
    headers = ["Title", "Author", "CookTime", "Prep_Time",
                 "Serves", "Description", "Dietary", "Instructions",
                 "Ingredient_list"]
    path = "recipes/"+str(rec_num).zfill(5)+ ".txt"
    rec = pd.read_csv(path, sep = "\t", header = None)

    rec = rec.rename(columns = {i:headers[i] for i in range(0,8)})
    rec = rec.rename(columns = {i:"Ingredients"
                      for i in range(8,rec.shape[1])})
    return rec

def loadVocabulary():
    '''Load Vocabulary File'''
    vocabulary = {}
    with open("vocabulary.txt") as f:
        for line in f:
            l = line.split()
            vocabulary[l[0]] = (l[1], l[2])
    return vocabulary

def loadIndex():
    '''Load Index file.'''
    index = {}
    with open("index.txt") as f:
        for line in f:
            l = line.split("\t")
            l = [i.strip() for i in l if i.strip()]
            l1 = [i.split() for i in l[1:]]
            for i in range(len(l1)):
                pos = [int(i) for i in l1[i][3].split("-")]
                l1[i].pop(3)
                l1[i].append(pos)
            index[l[0]] = l1
    return index

def posting(term, index, vocabulary):
    '''Take a term and return its posting list.'''
    term_num = vocabulary[term][0]
    return index[term_num]
