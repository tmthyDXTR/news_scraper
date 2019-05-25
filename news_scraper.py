import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
import os
import webbrowser


"""Abstract length in sentences"""
sentences = 12

"""News Sites --- Add RSS urls to scan"""
urls = [
    "https://taz.de/!s=&ExportStatus=Intern&SuchRahmen=Online;rss/",
    "https://www.faz.net/rss/aktuell/",
    "http://rss.sueddeutsche.de/rss/Topthemen",
    #"http://www.handelsblatt.com/contentexport/feed/top-themen",
    "https://www.welt.de/feeds/topnews.rss",
    "http://newsfeed.zeit.de/index",
    "https://www.fr.de/politik/rssfeed.rdf",
    "https://www.heise.de/rss/heise-top-atom.xml",
        ]



items_number = 0
timestamp = datetime.now().strftime("%A %d-%m-%Y %H:%M")

save_path_file = "C:/Users/dxtr/Documents/news/daily_news_" \
                 + time.strftime("%Y%m%d-%H%M") + ".html"

f = open(save_path_file, "w", encoding="utf-8")

wrapper = """<html>
<head>
<link rel="stylesheet" href="style.css">
<title>NEWS</title>
</head>
<body>
"""

info = "<h2>articles collected on " + timestamp + "</h2>"
wrapper += info

for url in urls:

    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, features="xml")

    items = soup.findAll("item")

    news_items = []

    if len(items) != 0:

        paper_title = soup.find("title").text

        title = """<h1>%s</h1>
        """
        wrapper += title % (paper_title)

        for n, item in enumerate(items, 1):
            news_item = {}
            news_item["id"] = str(n)
            news_item["title"] = item.title.text
            news_item["link"] = item.link.text
            #get_abstract(news_item["link"])
            news_items.append(news_item)
            url_clean = news_item["link"]\
                .replace("/", "") \
                .replace(".", "") \
                .replace(":", "")\
                .replace("?", "")

            item = """<p>%s <a href="%s" target="_blank" style="text-decoration: none">%s</a>
             - <a href="https://smmry.com/""" + news_item["link"] + """/#&SM_LENGTH="""\
                   + str(sentences) + """&SM_HEAT_MAP" target="_blank" style="text-decoration: none">abstract</a></p>
            """
            wrapper += item % (n, news_item["link"], news_item["title"])
            items_number += 1

            """Heise Exception: item = entry"""
    elif len(items) == 0:

        entries = soup.findAll("entry")
        paper_title = soup.find("title").text

        title = """<h1>%s</h1>
                """
        wrapper += title % (paper_title)

        for n, entry in enumerate(entries, 1):
            news_item = {}
            news_item["id"] = str(n)
            news_item["title"] = entry.title.text
            news_item["link"] = entry.find("link")["href"]
            news_items.append(news_item)

            item = """<p>%s <a href="%s" target="_blank" style="text-decoration: none">%s</a>
             - <a href="https://smmry.com/""" + news_item["link"] + """/#&SM_LENGTH="""\
                   + str(sentences) + """&SM_HEAT_MAP" target="_blank" style="text-decoration: none">abstract</a></p>
                    """
            wrapper += item % (n, news_item["link"], news_item["title"])
            items_number += 1


tail = """
<h2>%s articles collected on %s</h2>
</body>
</html>
"""

wrapper += tail % (items_number, timestamp)



f.write(wrapper)
f.close()

webbrowser.open(save_path_file)

