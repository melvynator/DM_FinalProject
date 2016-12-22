from bs4 import BeautifulSoup
import re
import cookielib, time
import json
import re
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

SEED_URL = "https://www.hopenglish.com"
YOUTUBE_URL = "https://www.youtube.com/watch?v="
CJ = cookielib.CookieJar()
OPENER = urllib2.build_opener(urllib2.HTTPCookieProcessor(CJ))

def get_categories():
    categories_link = []
    response = OPENER.open(SEED_URL)
    html_text = response.read()
    soup = BeautifulSoup(html_text, 'html.parser')
    category_listing = soup.find("li", { "data-type" : "subject" })
    categories_html = category_listing.findAll("li")
    for category_listing in categories_html:
        category_link = category_listing.find("a")
        category_name = category_link['href'].split('?')
        categories_link.append(category_name[0])
    return categories_link

def get_last_page(category):
    category_page = SEED_URL + category
    response = OPENER.open(category_page)
    html_text = response.read()
    html_parsed = BeautifulSoup(html_text, 'html.parser')
    pagination = html_parsed.find("div", { "class" : "pager" })
    if not pagination:
        return '1'
    last_page_link = pagination.findAll("a")[-1]
    url = last_page_link['href']
    splited_url = url.split('/')
    last_page_number = splited_url[-1]
    return last_page_number

def get_pages_per_category(category):
    last_page = get_last_page(category)
    pages = []
    for page in range(1, int(last_page) + 1):
        page_url_per_category = SEED_URL + category
        page_url_per_category += ('/' + str(page))
        pages.append(page_url_per_category)
    return pages

def get_video_url_from_a_page(url):
    response = OPENER.open(url)
    html_text = response.read()
    html_parsed = BeautifulSoup(html_text, 'html.parser')
    video_links = html_parsed.findAll("a", { "class" : "videolink" })
    links = []
    for link in video_links:
        links.append(SEED_URL + link['href'])
    return links

def build_crawl_listing(pace=None):
    if not pace:
        links = []
        categories = get_categories()
        for category in categories:
            print category
            pages = get_pages_per_category(category)
            for page in pages:
                videos_links = get_video_url_from_a_page(page)
                for link in videos_links:
                    links.append(link)
        crawl_listing = open("crawl_listing", "w")
        for link in links:
            crawl_listing.write(link + '\n')
        crawl_listing.close()

class Extractor:
    def __init__(self, url):
        response = OPENER.open(url)
        html_text = response.read()
        self.youtube_link = self.get_youtube_url(html_text)
        self.post_id = self.get_postid(html_text)
        html_parsed = BeautifulSoup(html_text, 'html.parser')
        self.word_list = self.get_scripts(html_parsed)
        self.url = url


    def get_postid(self, html):
        step_one = html.split('var post_id = ')
        step_two = step_one[1].split('var share_link')
        video_id_string = step_two[0]
        video_id = video_id_string.replace(';', '').strip()
        return video_id

    def get_youtube_url(self, html):
        m = re.search('vID = "(.*?)"', html)
        youtube_id_polluted = m.group(0)
        youtube_id = youtube_id_polluted.split(' = "')[1]
        youtube_link = YOUTUBE_URL + youtube_id[:-1]
        return youtube_link

    def get_scripts(self, html_parsed):
        main_div = html_parsed.find("div", {"id":"tabs-1"})
        content_div = main_div.find("div", {"class":"content"})
        paragraphs = content_div.findAll("p")
        text = ""
        for paragraph in paragraphs:
            word_dictionnaries = paragraph.findAll("span")
            for word_dictionnary in word_dictionnaries:
                text += " " + word_dictionnary.text
        exclude = ['!', ',', '.', '-', '_', u'\u2014', '?', '(', ')', ';', '/', '=', '+', '%', '"', "'"]
        for char in text:
            if char in exclude:
                text = text.replace(char, ' ')
        text = text.lower().strip().split()
        word_list = [str(word.encode('ascii', 'ignore')) for word in text]
        return word_list
