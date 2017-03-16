from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


from numpy import sqrt
from math import log


def processRecipe(path):
    """
    Stopword removal, normalization, stemmings.
    """
    ps = PorterStemmer()
    stop = stopwords.words('english')
    with open(path, encoding = "utf-8") as f:
        s = f.read()

    l = word_tokenize(s)
    l = [i for word in l for i in word.split(".") if i]
    l = [ps.stem(re.sub(r'[^a-zA-Z]', '', i.lower())) for i in word_tokenize(s) if i not in stop ]
    l = list(filter(None, l))
    l = [i for i in l if len(i)>2]

    return l


def tf(path):
    '''Compute the term frequency of a word in a document as
    the number of the term appear in the document divided the total
    count of the word in the document.'''
    freq = {}
    l = processRecipe(path)    # the document is preprocessed
    tot_count = len(l)    # so we don't keep in consideration stopword etc.
    for word in l:
        if word in freq:
            freq[word] += 1
        if word not in freq:
            freq[word] = 1

    for key in freq.keys():
        freq[key] = round(freq[key]/tot_count,4)

    return freq


# Compile dictionary used to write vocabulary and index
def recipeDict():
    '''Create a dictionary who has parsed recipes keywords has keys,
    a list of lists containing [path_to_file in which keyword appear,
    frequency of the word in the document, position]. The frequency is
    the tf (term frequency)'''
    my_dict = {}
    for file_path in os.listdir("recipes/"):
        freq = tf("recipes/"+file_path)
        word_list = processRecipe("recipes/"+file_path)

        for word in set(word_list):
            pos = [n for n, i in enumerate(word_list) if i == word]
            if word in my_dict.keys():
                my_dict[word].append([file_path.strip(".txt"), freq[word], pos])

            if word not in my_dict.keys():
                my_dict[word] = [[file_path.strip(".txt"),freq[word], pos]]

    return my_dict

# Add skip pointers to index
def add_skip(index):
    '''Add skip to posting lists. Skip has step equal to square root
    of posting list length.'''
    for term in index.keys():
        pos_length = len(index[term])
        step = int(sqrt(pos_length))
        for n in range(pos_length):
            if n in range(0, pos_length-step, step): index[term][n].insert(2, n+step)
            else : index[term][n].insert(2, 0)


def vocabulary(my_dict):
    '''Write the vocabulary on disk, each term has associated termID
    and overall frequency (# documents occur / tot doc)'''
    word_list = list(my_dict.keys())
    word_list.sort()
    word_num = len(os.listdir("./recipes/"))
    with open("vocabulary.txt","w") as f:
        i = 0
        for word in word_list:
            idf = log(word_num/len(my_dict[word]))
            f.write(word+"\t" +str(i).zfill(len(str(word_num)))+ "\t" +str(round(idf,3))+"\n")
            i+=1

# Write the index on disk
def index(my_dict):
    '''Write the index on disk.'''
    vocabulary = {}
    with open("vocabulary.txt") as f:
        for line in f:
            l = line.split()
            vocabulary[l[0]] = (l[1],l[2])
    g = open("index.txt", "w")
    for word in vocabulary.keys():
        g.write(vocabulary[word][0]+"\t")
        for file_ref in my_dict[word]:
            pos = "-".join([str(i) for i in file_ref[3]])
            tfidf = str( round( file_ref[1]*float(vocabulary[word][1]),3 ) )
            g.write(file_ref[0]+ " " + tfidf + " " + str(file_ref[2]) + " " + pos +"\t")
        g.write("\n")
    g.close()

