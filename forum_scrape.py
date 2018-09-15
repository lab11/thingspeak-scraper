import sys
import urllib2
from bs4 import BeautifulSoup
import re
from urlparse import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


base_url = "https://community.thingspeak.com/forum/"
delay = 5
dump = {}
forums = {}
threads = {}
remote = False


def get_all_forums():
    global forums
    if not remote:
        forums =  {u'microcontrollers': 2, u'other': 2, u'matlab': 8, u'announcements': 3, u'installation': 4, u'raspi': 2, u'thingspeak-plugins': 6, u'thingspeak-projects': 5}
        #forums = {u'thingspeak-apps': 19, u'esp8266-wi-fi': 10, u'thingspeak-api': 43, u'mobile-apps': 3, u'arduino': 13, u'general': 12, u'feature-requests': 5, u'microcontrollers': 2, u'other': 2, u'matlab': 8, u'announcements': 3, u'installation': 4, u'raspi': 2, u'thingspeak-plugins': 6, u'thingspeak-projects': 5}
    else:
        browser = webdriver.Chrome()
    	browser.get(base_url)
	try:
        	WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="spMainContainer"]')))
        	forum_source = browser.page_source
        	forum_soup = BeautifulSoup(forum_source, 'html.parser')
        	links = forum_soup.find_all('a', attrs={'class':'spInRowForumPageLink'})
	        for link in links:
                    href = link.get('href')
                    if "page" in href:
                        s_href = href.split("/")
	                forum_topic = s_href[-3]
                        forum_page =s_href[-2].split("-")[1]
                        try:
                            if forums[forum_topic] <= int(forum_page):
                                forums[forum_topic] = int(forum_page)
                        except:
                            forums[forum_topic] = int(forum_page)
    	except TimeoutException:
        	pass
        browser.close()

def construct_url_list(topic, max_page):
    print topic, max_page
    url_list = []
    for x in range(1, max_page+1):
        url_list.append("https://community.thingspeak.com/forum/"+topic+"/page-"+str(x)+"/")
    return url_list

def gather_post(post_soup):
    post = {}
    date = post_soup.find('div', attrs={'class': 'spPostUserDate'}).text
    username = post_soup.find('div', attrs={'class': 'spPostUserName'}).text
    content = post_soup.find('div', attrs={'class': 'spPostContent'}).text.replace('"', "'").replace("\n", '').replace("\\", "").replace("\t", '').replace("\r", '')
    num_user_posts = post_soup.find('div', attrs={'class': 'spPostUserPosts'}).text.strip().split(":")[-1]
    post['date'] = date
    post['author'] = username
    post['content'] = content
    post['num_user_post'] = num_user_posts
    return post


def visit_thread(thread_url):
    thread = {}
    posts = []
    thread_req = urllib2.urlopen(thread_url)
    html = thread_req.read()
    thread_soup = BeautifulSoup(html, 'html.parser')
    posts_soup = thread_soup.find_all('div', attrs={'class':'spTopicPostSection'})# spOdd spFirstPost spType-User spRank-new-member spUsergroup-members spUserPost spAuthorPost'})
    for post_soup in posts_soup:
        post = gather_post(post_soup)	    
        posts.append(post)
    thread['posts'] = posts
    thread['url'] = thread_url
    return thread
        

def visit_all_forums():
#    dump = []
    for key, value in forums.iteritems():
        url_list = construct_url_list(key, value)
        full_forum = []
        for forum_url in url_list:
            name = forum_url.split("/")[-3]
            forum = {}
            threads = []
            channel = urllib2.urlopen(forum_url)
            html = channel.read()
            forum_soup = BeautifulSoup(html, 'html.parser')
            threads_soup = forum_soup.find_all('a',attrs={'class', 'spRowName'})
            for thread_soup in threads_soup:
                thread_url = thread_soup.get('href')
                thread = visit_thread(thread_url)
                threads.append(thread)
            forum['url'] = forum_url
            forum['threads'] = threads
            #print "\t" + forum_url
            full_forum.append(forum)
            print forum_url
        f = open("forums/"+name+".json", "w")
        f.write(str(full_forum))
#    print dump

get_all_forums()
visit_all_forums()

#visit_thread('https://community.thingspeak.com/forum/thingspeak-apps/weird-channel-graphs-days1-goes-back-to-3-days-1')



