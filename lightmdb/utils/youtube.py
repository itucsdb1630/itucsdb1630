import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

"""
Youtube Search Plugin.
@author Emin Mastizada
"""

def search_video(keyword, count=1):
    url = "https://www.youtube.com/results?search_query={query}%20trailer"
    data = requests.get(url.format(query=quote(keyword))).content
    soup = BeautifulSoup(data, "html.parser")
    result = []
    counter = 0
    for video in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        result.append("https://www.youtube.com/embed/" + video['href'].replace('/watch?v=', ''))
        counter += 1
        if counter == count:
            break
    return result
