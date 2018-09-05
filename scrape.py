import sys
import urllib2
from bs4 import BeautifulSoup
import re
from urlparse import *
import json

reload(sys)  
sys.setdefaultencoding('utf8')

dump = "["

class Chart:
    title = ""
    second_title = ""
    xaxis = ""
    yaxis = ""
    chart_type = ""
    results  = ""
    header = ""
    url = ""

    def __init__(self):
        self.title = ""
        self.second_title = ""
        self.xaxis = ""
        self.yaxis = ""
        self.chart_type = ""
        self.results  = ""
        self.header = ""
        self.url = ""

    def to_json(self):
        json_str = '"title": "'+self.title+'", "second_title": "'+self.second_title+'", "xaxis": "'+self.xaxis+'", "yaxis": "'+self.yaxis+'", "chart_type": "'+self.chart_type+'", "results": "'+self.results+'", "header": "'+self.header+'"'
        return json_str


class Channel:
    name = ""
    url = ""
    author = ""
    disc = ""
    tags = []
    charts = ""
    html = ""

    def pretty_print(self):
        print "\tname: " + self.name.encode('utf-8').strip()
        print "\turl: " + self.url.encode('utf-8').strip()
        print "\tauthor: " + self.author.encode('utf-8').strip()
        print "\tdisc: " + self.disc.encode('utf-8').strip()
        print "\ttags: " + str(self.tags).encode('utf-8').strip()
        print "\tcharts:" + str(self.charts).encode('utf-8').strip()
        #print "\thtml:" + self.html.encode('utf-8').strip()

    def dump_html(self):
#        json_str = '{"name": "' + self.name.encode('utf-8').strip() + '", "url": "' + self.url.encode('utf-8').strip() + '", "author": "' + self.author.encode('utf-8').strip() + '", "disc": "' + self.disc.encode('utf-8').strip() + '", "tags": ' + self.tags.encode('utf-8').strip() + ', "charts": ' + self.charts.encode('utf-8').strip() + '}';
        
        f = open("html/"+self.url.encode("utf-8").split("/")[-1]+".html", "a")
        f.write(self.html.encode("utf-8"))


    def to_json(self):
        json_str = '{"name": "' + self.name.encode('utf-8').strip() + '", "url": "' + self.url.encode('utf-8').strip() + '", "author": "' + self.author.encode('utf-8').strip() + '", "disc": "' + self.disc.encode('utf-8').strip() + '", "tags": ' + self.tags.encode('utf-8').strip() + ', "charts": ' + self.charts.encode('utf-8').strip() + '}';
        #parsed_json = json.loads(json_str)
        return json_str
        #return parsed_json
    
    def dump_json(self):
        f = open("json/"+self.url.encode("utf-8").split("/")[-1]+".json", "a")
        f.write(self.to_json().encode("utf-8"))
#    f.write(self.html.encode("utf-8"))


base_url = 'https://thingspeak.com/'
max_page = 0
cur_channel = Channel()

def find_links_in_page(soup):
    channels = soup.find_all('a', attrs={'class':'link-no-hover'})
    links = []
    for channel in channels:
        links.append(channel.get('href'))
    return links

def fetch_new_channel(link):
    global cur_channel
    channel = urllib2.urlopen(base_url+link)
    html = channel.read()
    cur_channel.url = base_url+link
    channel_soup = BeautifulSoup(html, 'html.parser')
    cur_channel.html = html.decode('utf-8')
    return channel_soup

def fetch_new_page(num):
    page = urllib2.urlopen(base_url+"channels/public?page="+str(num))
    page_soup = BeautifulSoup(page, 'html.parser')
    return page_soup

def parse_chart(chart_soup):
    cur = Chart()
    title = chart_soup.find('div','window-title').text
    header = chart_soup.find('iframe','window-iframe').get('src')
    qs = urlparse(header)[4]
    o = parse_qs(qs)
    try:
        cur.chart_type = str(o['type'][0])
    except:
        pass
    try:
        cur.results = str(o['results'][0])
    except:
        pass
    try:
        cur.second_title = str(o['title'][0])
    except:
        pass
    try:
        cur.yaxis = str(o['yaxis'][0])
    except:
        pass
    try:
        cur.xaxis = str(o['xaxis'][0])
    except:
        pass
    cur.header = header
    cur.title = title
    return cur.to_json()

def extract_chart_data(channel_soup):
    global cur_channel
    charts_soup = channel_soup.find_all('div', attrs={'class':'window-container'})
    charts = []
    json_charts = '['
    for chart_soup in charts_soup:
        charts.append(parse_chart(chart_soup))
    for chart in charts:
        json_charts += "{ " + chart + "},"
    json_charts = json_charts[:-1] + "]"
    cur_channel.charts = json_charts 

def extract_meta_data(channel_soup):
    global cur_channel
    name = channel_soup.find('h1', attrs={'id':'channel-name-header'}).text
    author = channel_soup.find('ul', attrs={'id':'table-channel-metadata'}).find_all('li')[1].text.split(":")[1].strip()
    disc = channel_soup.find_all('div', attrs={'class':'col-xs-6 col-sm-4'})[1].text.split('\n')[1].strip()
    cur_channel.author = author
    cur_channel.disc = disc
    cur_channel.name = name

def extract_tags(channel_soup):
    global cur_channel
    tags = []
    tag_soup = channel_soup.find_all('a', attrs={'id':'channel-tags'})
    json_tags = '['
    for tag in tag_soup:
        tags.append(tag.text)
    for tag in tags:
        json_tags += '"' + tag + '",'
    json_tags = json_tags[:-1] + "]"
    cur_channel.tags = json_tags

def extract_channel(channel_soup):
    extract_meta_data(channel_soup)
    extract_chart_data(channel_soup)
    extract_tags(channel_soup)


def run(times):
    global dump
    for x in xrange(1, times+1):
        #sys.stderr.write("page " + str(x) + " of " + str(times+1))
        page_soup = fetch_new_page(x)
        links = find_links_in_page(page_soup)
        for link in links:
            channel_soup = fetch_new_channel(link)
            extract_channel(channel_soup)
            json = cur_channel.to_json()
            dump += json + ","
            cur_channel.dump_html()
            cur_channel.dump_json()
    dump = dump[:-1]
    dump = dump + "]"
    print dump

def prefetch():
    global max_page
    page = urllib2.urlopen(base_url+"channels/public")
    soup = BeautifulSoup(page, 'html.parser')
    pages = soup.find_all('li')
    max_page = 0
    for page in pages:
        try:
            if int(page.text) > max_page:
                max_page = int(page.text)
        except:
            continue

prefetch()
run(max_page)
#run(2)






