# @author Anusha Voloju
# UID : 677775723
# Net Id : avoloj2
# University of Illinois, Chicago
# CS 582, Spring 2019
# Final Project - UIC Web Search Engine


Functionality: 

1. The logic is written in four python files Crawler.py, Main.py, InvertedIndex.py and CosineSimilarity.py.


2. Main.py is the main file which executes all the steps of the search engine.


3. When Main.py is executed, the user is given three options to select his preferences for the search engine.
First option is to Crawl the pages and get the data set to build the inverted index and perform search.
Second option is to Use the existing dataset to build inverted index and perform the search.
Third option is to Use the existing built inverted index to perform the search.

4. After selecting one of the options, the user is asked to input a query.

5. Before entering the query, for selecting the preferences, if the user selects first option, Main.py calls crawler function in Crawler.py file to crawl 3000 pages starting with https://www.cs.uic.edu/

6. Crawler.crawler() performs web traversal using breadth first search. The pages to be visited are stored in a queue. For each url being processed from the queue, it verifies if the content-type is text/html, extracts all the links in the page using BeautifulSoup and for each link it checks if it is not in excluded list(like .pdf, .docx, .jpeg etc), checks if the it is in uic domain, converts relative urls to complete urls, deletes ending slash and also checks if not already visited. Then finally adds the link to the queue.

7. For each visited url, the url is added to CrawledPagesList.txt file and the text content of the page is extracted using BeautifulSoup and a text file is created in HtmlPages folder(in the current directory). The name of the text file is created from the page url by replacing slash with hyphen.

8. After completing the crawling and creating text files which is the data set, Main.py file calls InvertedIndex.documentsList(files) loops through all the text files in the data set, using the url list in CrawledPages.txt and stores the text details in a dictionary with url as the key and the text content of the text file as the value.

9. After creating the dictionary for the pages, Main.py calls InvertedIndex.getInvertedIndex(documents) which uses InvertedIndex.buildInvertedIndex(text) and InvertedIndex.addToInvertedIndex(inverted, docid, docindex) to construct the inverted index. 

If the user had selected the second option, the crawling step would be skipped and the inverted index would be built using the data set of text files.

InvertedIndex.buildInvertedIndex(text) and InvertedIndex.addToInvertedIndex(inverted, docid, docindex) uses the words list formed by InvertedIndex.processText(text) to forms lists of indexes of each word and map the indexes with url respectively.

InvertedIndex.processText(text) uses three functions 

InvertedIndex.tokenizeText(text) which removes the punctuations, tokenizes the text using 
enumerate(text) to get words list. 

InvertedIndex.cleanUp(words) cleans the words by removing the words whose length is less 
than three and by removing the stop words.

InvertedIndex.normalize(words) stems the words using PorterStemmer and normalizes the words by removing numbers, punctuations and by converting the words to lower case.

After calling these three functions, it again calls the InvertedIndex.cleanUp(words) to remove the stop words generated after stemming the words.

10. Once the inverted index is built, Main.py creates inverted.csv file in Inverted folder(in the current directory) to store the built inverted index.

If the user had selected the third option, the crawling step and building inverted index steps would be skipped and the built inverted index stored as inverted.csv would be used to perform the search.

11. After building the inverted index, Main.py calls CosineSimilarity.calculateMaxtf(inverted) which scans the inverted index and calculates the maximum term frequency of each page url.

12. After getting maxtf, Main.py calls CosineSimilarity.calculateDocLengths(inverted, documents, maxtf) which scans the inverted index and calculates the tfidf of each term and uses these tfidf values to form the document length for each text document. 

13. Once the document length are calculated, Main.py calls CosineSimilarity.calculateCosSim(documents, querypath, inverted, maxtf, doclength) which scans the input query and calls InvertedIndex.processText(text) and gets the 
text documents having at least one word in the query. For each query, the text document and query weights are calculated and from these values the dot product of the weights is calculated, and all the weights are divided by the corresponding document lengths to get the cosine similarities. Based on the cosine similarities, the urls of the corresponding text documents are sorted and retrieved.

14. Once the ranked urls are retrieved, Main.py displays top 10 urls relevant to the query and asks if the user wants to return more documents. If the user selects yes, 10 more urls are displayed. If the user selects no, no more urls are displayed and the program exits.



Instructions for executing the program:

Required packages :
1. sys
2. pathlib
3. csv
4. os
5. requests
6. urljoin
7. BeautifulSoup
8. tldextract
9. string
10. nltk
11. math
12. collections


Steps to run the program :

1. Navigate to the location of Main.py.


2. Crawler.py, Main.py, InvertedIndex.py, CosineSimilarity.py, CrawledPagesList.txt files should be in same directory. The Inverted folder with inverted.csv should also be in same directory


3. These files are written in python3, please use appropriate python interpreter to run 
the program.


4. Dropbox link: https://www.dropbox.com/sh/5fcb8l3ua42g42q/AACIB64ILpOcllQmuCpYEBhBa?dl=0

If you want to use the existing data set to build inverted index and perform search (needs "HtmlPages" to build inverted index) 
(or) 
If you want to use the existing inverted index to perform the search (still needs "HtmlPages" to calculate the document lengths 
for calculating cosine similarity)

In both cases, copy "HtmlPages" folder(which is a sub folder in "information-retrieval-project" folder in the given dropbox link) from the above dropbox link and place the folder in the same directory in which the python files are present.

If you want to give a relative path of "HtmlPages" directory while executing the program use the command 
"python Main.py <relative path of 'HtmlPages'> 

otherwise, use "python Main.py" to run the program. (This assumes that Main.py, Crawler.py, InvertedIndex.py, CosineSimilarity.py, CrawledPagesList.txt, HtmlPages and Inverted folder(having inverted.csv) are all in same directory). An "ls" command in this directory should have  
 following output

     Main.py  Crawler.py  InvertedIndex.py  CosineSimilarity.py  CrawledPagesList.txt  Inverted  HtmlPages




Output:

  --- UIC WEB SEARCH ENGINE ---     

 Please select your preferences for the search.. 

1. Crawl the HtmlPages and get the data set to build inverted index and perform the search. 
2. Use the existing dataset to build inverted index and perform the search. 
3. Use the existing built inverted index to perform the search. 

 Please enter '1' or '2' or '3' for selecting your required preference: 3
..............................................................................
Initiating search
..............................................................................

 Please enter your query: graduate fellowships

 Query Results: 

 https://grad.uic.edu/fellowships-awards/university-fellowship

 https://grad.uic.edu/fellowship-office-information

 https://cs.uic.edu/graduate/admissions/financial-aid-and-funding

 https://grad.uic.edu/graduate-college-fellowships

 https://grad.uic.edu/fellowships-awards/graduate-access-fellowship

 https://grad.uic.edu/fellowship-information-session-schedule

 https://grad.uic.edu/online-funding-resources

 https://grad.uic.edu/deans-scholar-fellowship

 https://grad.uic.edu/uic-u-i-system-and-federal-opportunities

 https://grad.uic.edu/graduate-college-fellowship-and-award-deadlines

 
 Return more HtmlPages? Yes or No ?: y

 https://grad.uic.edu/funding-your-education

 https://grad.uic.edu/graduate-funding-overview

 https://grad.uic.edu/external-fellowship-campus-deadlines

 https://grad.uic.edu/fmc-technologies-educational-fund

 https://grad.uic.edu/graduate-college-professional-success-program-psp-fellows

 https://grad.uic.edu/funding-seminars

 https://grad.uic.edu/chancellors-graduate-internship-award

 https://grad.uic.edu/my-waiver-didnt-post-what-do-i-do

 https://grad.uic.edu/information-about-assistantships

 https://grad.uic.edu/graduate-college-tuition-and-fee-waivers

 
 Thank you for using the application, please run again to perform search on another query.








