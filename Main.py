import sys
import pathlib
import Crawler
import InvertedIndex
import CosineSimilarity
import csv
import os

if len(sys.argv) == 2:
    htmlpagesdirectory = pathlib.Path.cwd().joinpath(sys.argv[1])
else:
    htmlpagesdirectory = pathlib.Path.cwd().joinpath('HtmlPages')


if __name__ == '__main__':

    crawledlistdirectory = pathlib.Path.cwd()

    print("\n --- UIC WEB SEARCH ENGINE ---     ")
    print("\n Please select your preferences for the search.. \n")
    print("1. Crawl the HtmlPages and get the data set to build inverted index and perform the search. ")
    print("2. Use the existing dataset to build inverted index and perform the search. ")
    print("3. Use the existing built inverted index to perform the search. ")

    while (True):
        input_option = input(
            "\n Please enter '1' or '2' or '3' for selecting your required preference: ")
        if (input_option not in {'1','2','3'}):
            print("\n Please enter a valid preference option.. ")
            continue
        else:
            print('..............................................................................')
            break



    # initialize inverted index
    inverted = {}

    # run crawler
    if(input_option == '1'):

        print('Crawling web pages')
        print('..............................................................................')
        Crawler.crawler(3000, 'https://www.cs.uic.edu')
        print('..............................................................................')
        print('Crawling web pages completed successfully')
        print('..............................................................................')

    # get document details from collection
    documents = InvertedIndex.documentsList(htmlpagesdirectory, crawledlistdirectory)


    # Build Inverted-Index for documents
    if(input_option == '1' or input_option == '2'):
        print('Calculating inverted index')
        print('..............................................................................')
        inverted = InvertedIndex.getInvertedIndex(documents)
        inverted_index_path = pathlib.Path.cwd().joinpath('Inverted', 'inverted.csv')

        dir = pathlib.Path.cwd().joinpath("Inverted").is_dir()
        if dir != True:
            os.mkdir(str(pathlib.Path.cwd().joinpath("Inverted")))
        else:
            filelist = [f for f in os.listdir("Inverted")]
            for f in filelist:
                os.remove(os.path.join("Inverted", f))

        with open(str(inverted_index_path), 'w') as f:
            for key in inverted.keys():
                f.write("%s,%s\n" % (key, inverted[key]))
        print('..............................................................................')
        print('Inverted index calculated succesfully')
        print('..............................................................................')


    # use an existing inverted index
    if (input_option == '3'):
        print('Initiating search')
        print('..............................................................................')
        inverted_index_path = pathlib.Path.cwd().joinpath('Inverted', 'inverted.csv')
        inverted = {}
        with open(str(inverted_index_path), 'r') as infile:
            reader = csv.reader(infile)
            v = {}
            for row in reader:
                k = row[0]
                v = {}
                for item in row[1:]:
                    i = item.split(': ')[0].replace('{', '')
                    j = item.split(': ')[1].replace('}', '')
                    v[i] = int(j)
                inverted[k] = v


    query = input("\n Please enter your query: ")


    # get the maximum term frequecies
    maxtf = CosineSimilarity.calculateMaxtf(inverted)

    # get the document lengths from Inverted-Index
    doclength = CosineSimilarity.calculateDocLengths(inverted, documents, maxtf)

    # tokenize queries and find CosSim between documents and query
    top50 = CosineSimilarity.calculateCosSim(documents, query, inverted, maxtf, doclength)

    if (len(top50) > 0):
        print("\n Query Results: ")
        for qword, pages in top50.items():
            for page in pages[:10]:
                page = page.replace(' ', '').replace('\'', '')
                print("\n", page)

        more_docs = input("\n \n Return more HtmlPages? Yes or No ?: ")

        if (more_docs.lower() == 'yes' or more_docs.lower() == 'y'):
            for qword, pages in top50.items():
                for page in pages[10:20]:
                    page = page.replace(' ', '').replace('\'', '')
                    print("\n", page)
            print(
                "\n \n Thank you for using the application, please run again to perform search on another query.\n")

        elif (more_docs.lower() == 'no' or more_docs.lower() == 'n'):
            print(
                "\n \n Thank you for using the application, please run again to perform search on another query.\n")

    else:
        print("\n There are no results for the query.")







