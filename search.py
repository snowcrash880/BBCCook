def intersect(a,b, k):
    '''Algorithm to intersect two posting lists. k is the distance
    parameter in the proximity search.'''
    i = 0
    j = 0
    answer = []

    while j < len(b) and i < len(a):
        if a[i][0] == b[j][0]:    # same filenumber
            if k == 0:    # not proximity search
                answer.append(a[i])
            if k != 0 and proximitySearch(a[i][3], b[j][3],k)!=[]:
                answer.append(a[i])
            i +=1; j+=1
        else:
            if (int(a[i][0]) > int(b[j][0])):
                skip = hasSkip(b, j)
                if skip : j = int(skip)
                else: j+=1
            else:
                skip = hasSkip(a, i)
                if skip : i = int(skip)
                else: i+=1
    return answer

def hasSkip(posting, pos):
    '''Check if a posting list has a skip in a certain position.'''
    skip = int(posting[pos][2])
    if skip != 0: return skip
    else : return False

def proximitySearch(pp1,pp2, k):
    '''Perform a proximity search.'''
    answer = []
    l = []
    ii = 0
    jj = 0
    while ii< len(pp1) :    #
        while jj < len(pp2):
            if abs(pp1[ii] - pp2[jj]) <= k:
                l.append(pp2[jj])
            elif pp2[jj] > pp1[ii]:
                break
            jj += 1
        while l != [] and abs(l[0]-pp1[ii]) > k:
            l.pop(0)
        for i in l:
            answer.append([pp1[ii]]+[i])
        ii += 1
    return answer

def processQuery(query):
    """
    Stopword removal, normalization, stemmings.
    """
    ps = PorterStemmer()
    stop = stopwords.words('english')
    l = word_tokenize(query)
    l = [i for word in query for i in word.split(".") if i]
    l = [ps.stem(re.sub(r'[^a-zA-Z]', '', i.lower()))
         for i in word_tokenize(query)
         if i not in stop ]
    l = list(filter(None, l))
    l = [i for i in l if len(i)>2]
    if len(l) == 1 : l = str(*l)
    return l


def checkProx(s):
    '''check if there query contains a proximity search with sintax [word1] /[distance] [word2]}.
    Return the couples of word to search and the proximity range.'''
    couples = {}
    s = s.split("/")
    for i in range(len(s)-1):
        couples[processQuery(s[i].split()[-1]), processQuery(s[i+1].split()[1])] = s[i+1].split()[0]
    return couples


def search(query, index, vocabulary):
    '''Conjunctive search algorithm.'''

    couples = checkProx(query) # control if the query contain proximity
    query = processQuery(query)    # process query like recipes

    if type(query) == str : query = [query]  # transform single query in list

    for term in query:    # remove terms not in vocabulary
        if term not in voc.keys(): query.remove(term)

    sbf = sorted([(term, voc[term][1]) for term in query],
                 reverse = True,
                 key = lambda x : x[1] )
    terms = []
    if couples:    # if there is a proximity search
        couples_temp = couples.copy()
        for i,j in couples.keys():
            if i or j not in voc.keys(): del couples_temp[i,j]
        couples = couples_temp.copy()
        for i,j in couples.keys():
            sbf = [k for k in sbf if k[0] != i ]
            sbf = [k for k in sbf if k[0] != j ]
            a = posting(i, *X)
            b = posting(j, *X)
            terms.extend(intersect(a,b, int(couples[i,j])))
    if sbf:
        results = posting(sbf[0][0], index, vocabulary)
        terms.extend([posting(term[0],index, vocabulary) for term in sbf[1:]])
    else: return terms
    while terms != [] and results != []:
        results = intersect(results,
                            terms[0], 0)
        terms = terms[1:]
    return results


def cosSim(query, docIDResults, ind, voc):
    '''Cosine similarity between documents.'''    # To select search results.
    N = len(docIDResults)
    query = processQuery(query)
    if type(query) == str : query = [query]

    for term in query:
        if term not in voc.keys(): query.remove(term)

    Scores = {i:0 for i in docIDResults}
    Length = []

    for doc in docIDResults:
        Length.append(len(processRecipe("recipes/"+doc+".txt")))

    for term in query:
        wtq = float(voc[term][1])  # idf
        for i in ind[ voc[term][0] ]:
            if i[0] in docIDResults:
                Scores[i[0]] += wtq*float(i[1])  # idf-tf
    for n,i in enumerate(docIDResults):
        Scores[i] = Scores[i]/Length[n]

    Scores = sorted(Scores, key = Scores.get, reverse= True)
    return Scores

def printResults(results):
    '''Printout search results.'''
    for doc in results:
        df = retrieveRecipe(doc)
        print("Title: "+df["Title"][0])
        print("Author: "+ df["Author"][0])
        print("-"*(len(df["Title"][0])+7))
        print("Description :"+df["Description"][0])
        print("-"*(len(df["Title"][0])+7))
        print("Cooking Time :"+df["CookTime"][0])
        print("Preparation Time: "+df["Prep_Time"][0])
        print("Serves: "+df["Serves"][0])
        print("Dietary: "+df["Dietary"][0])
        print("-"*(len(df["Title"][0])+7))
        l = [i.strip() for i in df["Ingredients"].to_csv().split("\"") if not i.startswith("Ingredients")  if i !=""][1:]
        l = [i.replace(",", "") for i in l if i]
        print("Ingredient List:\n")
        print(*l, sep = "\n")
        print("-"*(len(df["Title"][0])+7))
        print("Instructions:\n"+df["Instructions"][0])
        print("\n")
