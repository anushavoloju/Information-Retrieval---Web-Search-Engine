from math import log2
from math import sqrt
from collections import defaultdict
import InvertedIndex

#calculate maximum term frequency for each document
def calculateMaxtf(inverted):
    maxtf = dict()
    for word, docLists in inverted.items():
       for docid,tf in docLists.items() :
            if (maxtf.get(docid, 0) < tf) :
                maxtf[docid] = tf
    return maxtf


# calculate maximum term frequency, tfidf and document lengths for all documents
def calculateDocLengths(inverted, documents, maxtf):
    docsqlength = dict()
    doclength = dict()
    for word, docLists in inverted.items():
       docfreq = len(docLists)
       for docid,tf in docLists.items():
            tfidf = (tf/maxtf[docid]) * log2(len(documents)/docfreq)
            docsqlength[docid] = docsqlength.get(docid, 0) + (tfidf * tfidf)
    for docid, length in docsqlength.items():
        doclength[docid] = sqrt(docsqlength[docid])
    return doclength


# tokenize queries and find CosSim between documents and queries
def calculateCosSim(documents, query, inverted, maxtf, doclength):
    top50 = defaultdict(list)

    querywords = InvertedIndex.processText(query)
    qf = dict()
    # get query frequencies
    for index, word in querywords:
        qf[word] = qf.get(word, 0) + 1

    # find the maximum query frequency for each query
    maxqf = 0
    for word, f in qf.items():
        if maxqf < f:
            maxqf = f

    # get documents which has atleast one query word and find CosSim weight between each document and query
    cosSimWeight = dict()
    cosSim = dict()
    for index, word in querywords:
        docs = dict()
        if word in inverted:
            docs = inverted[word]
            df = len(docs)
            for docid, tf in docs.items():
                docweight = (tf / maxtf[docid]) * log2(len(documents) / df)
                queryweight = (qf[word] / maxqf) * log2(len(documents) / df)
                totalweight = docweight * queryweight
                cosSimWeight[docid] = cosSimWeight.get(docid, 0) + totalweight

    # calculate CosSim by dividing CosSim weight by doclength
    for docid, weight in cosSimWeight.items():
        cosSim[docid] = cosSimWeight[docid] / doclength[docid]

    # map query with retrieved ranked documents
    for docid in sorted(cosSim, key=cosSim.get, reverse=True)[:20]:
        top50[query].append(docid)

    return top50