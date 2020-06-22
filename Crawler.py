import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import tldextract
import os
import pathlib

requests.packages.urllib3.disable_warnings()


def getPageContent(s, PageUrl):
    for script in s(["script", "style"]):
        script.extract()
    htmltext = s.get_text()
    rawtext = htmltext.splitlines()
    lines = []
    for line in rawtext:
        line = line.strip()
        if line != '':
            line = line + '\n'
            lines.append(line)
    cleantext = "".join(lines)
    file_name = PageUrl[7:].replace('/', '-')
    f = open("HtmlPages/" + file_name + '.txt', "w")
    f.write(cleantext)
    f.close()


def crawler(maxPages,WebUrl):
    if(maxPages>0):
        numberVisited = 0
        pagesVisited = []
        pagesToVisit = [WebUrl]
        dir = pathlib.Path.cwd().joinpath("HtmlPages").is_dir()
        if dir != True:
            os.mkdir(str(pathlib.Path.cwd().joinpath("HtmlPages")))
        else:
            filelist = [f for f in os.listdir("HtmlPages")]
            for f in filelist:
                os.remove(os.path.join("HtmlPages", f))
        crawledlistfile = open("CrawledPagesList.txt", "w")
        crawledlistfile.close()

        while len(pagesVisited) < maxPages and pagesToVisit != []:
            numberVisited = numberVisited + 1
            url = pagesToVisit[0]
            url = url.replace("www.","")
            pagesToVisit = pagesToVisit[1:]

            try:
                code = requests.get(url, verify=False)
                content_type = code.headers.get('content-type')
                if 'text/html' not in content_type:
                    continue
                plain = code.text
                s = BeautifulSoup(plain, "html.parser")
                getPageContent(s, url)
                pagesVisited = pagesVisited + [url]

                for link in s.findAll('a', href=True):
                    exc_ext = ""
                    excluded = [".pdf", ".docx", ".doc", ".jpg", ".jpeg", ".png", ".ppt",".gif", ".gz", ".rar", ".tar", ".tgz", ".zip", ".exe", ".js", ".css", ".mp4", ".avi"]
                    if "http" not in link['href']:
                        link['href'] = urljoin(url, link['href'])
                    result = tldextract.extract(link['href'])
                    domain = result.domain + '.' + result.suffix
                    if domain == "uic.edu" and "https" in link['href']:
                        link['href'] = link['href'].replace("www.", "")
                        link['href'] = link['href'].replace("\n", "")
                        if link['href'][-1:] == "/":
                            link['href'] = link['href'][:-1]
                        for ext in excluded:
                            if ext in link['href']:
                                exc_ext = "true"
                                break
                        if exc_ext == "true":
                            continue
                        if "#" in link['href']:
                            continue
                        if link['href'] not in pagesToVisit and link['href'] not in pagesVisited:
                            pagesToVisit = pagesToVisit + [link['href']]

                crawledlistfile = open("CrawledPagesList.txt", "a+")
                crawledlistfile.write(url + "\n")
                crawledlistfile.close()

            except:
                print("Failed!", url)


        return pagesVisited

if __name__ == '__main__':
    pagesVisited = crawler(3000, 'https://www.cs.uic.edu')

