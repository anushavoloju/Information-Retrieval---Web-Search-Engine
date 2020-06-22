import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


_STOP_WORDS = set(stopwords.words("english"))

# function to extract documentid, title and text from the documents of the collection
def documentsList(htmlpagesdirectory, crawledlistdirectory):
    documents = dict()
    crawledlistfile = open(str(crawledlistdirectory.joinpath("CrawledPagesList.txt")))
    fail = []
    for line in crawledlistfile.readlines():
        try:
            line = line.replace('\n', '')
            url = line
            line = line[7:].replace('/', '-')
            line = line + ".txt"
            file = open(str(htmlpagesdirectory.joinpath(line)), "r")
            data = file.read().replace('\n', ' ')
            documents[url] = data
        except:
            fail.append(line)

    return documents


# function to tokenize the text into words
def tokenizeText(text):
    wordslist = []
    currentword = []
    indexofword = None
    punctuations = set(string.punctuation)
    for x in text:
        if x in punctuations:
            text = text.replace(x, "")
    for i, char in enumerate(text):
        if char.isalnum():
            currentword.append(char)
            indexofword = i
        elif currentword:
            word = u''.join(currentword)
            wordslist.append((indexofword - len(word) + 1, word))
            currentword = []
    if currentword:
        word = u''.join(currentword)
        wordslist.append((indexofword - len(word) + 1, word))
    return wordslist


# function to remove 1 and 2 character words and stop words
def cleanUp(words):
    cleanedwords = []
    for index, word in words:
        if len(word) < 3 or word in _STOP_WORDS:
            continue
        cleanedwords.append((index, word))
    return cleanedwords


# function to remove punctuations in the text, perform stemming and normalize the words
def normalize(words):
    ps = PorterStemmer()
    normalizedwords = []
    punctuations = set(string.punctuation)
    for index, word in words:
        word = ps.stem(word)
        for x in word:
            if x in punctuations:
                word = word.replace(x, "")
        if word.isdigit():
            continue
        normalizedword = word.lower()
        normalizedwords.append((index, normalizedword))
    return normalizedwords


# function to implement text preprocessing
def processText(text):
    words = tokenizeText(text)
    cleanedwords = cleanUp(words)
    normalizedwords = normalize(cleanedwords)
    processedwords = cleanUp(normalizedwords)
    return processedwords


# function to build document locations of a word
def buildInvertedIndex(text):
    index = {}
    for i, word in processText(text):
        lists = index.setdefault(word, [])
        lists.append(i)
    return index


# function to implement inverted index with word and document locations (term frequencies)
def addToInvertedIndex(invertedindex, docid, index):
    for word, locations in index.items():
        indices = invertedindex.setdefault(word, {})
        indices[docid] = len(locations)
    return invertedindex


# construct inverted index
def getInvertedIndex(documents):
    invertedindex = {}
    docno = 0
    for docid, text in documents.items():
        docno = docno + 1
        try:
            index = buildInvertedIndex(text)
            addToInvertedIndex(invertedindex, docid, index)
            #print(docno, " doc added", docid)
        except:
            print("failed", docid)

    return invertedindex

