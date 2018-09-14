from bs4 import BeautifulSoup
from urlparse import *
import urllib2
import time
import requests
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def make_json_str(to_convert):
    json_str = '['
    for item in to_convert:
        if item:
            json_str += "{ " + item + "},"
    if not json_str == '[':
        json_str = json_str[:-1] + "]"
    else:
        json_str = '[]'
    return json_str

def load(link):
    #print "loading " + link
    #link = 'https://thingspeak.com//apps/matlab_visualizations/160288?size=iframe'
    browser = webdriver.Chrome()
    browser.get(link)
    delay = 5
    values = []
    sub_values = []
    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]')))
        matlab_source = browser.page_source 
        iframe_soup = BeautifulSoup(matlab_source, 'html.parser')
        vis_type_line = iframe_soup.find('g', attrs={'class':'type-line type-viz-mark line'})
        vis_type_multi_line = iframe_soup.find('g', attrs={'class':'type-line type-viz-mark line1'})
        vis_type_scatter = iframe_soup.find('g', attrs={'class':'type-symbol type-viz-mark markers'})
        if vis_type_line:
            values.append("line")
#            values.append('"type": "line"')
        elif vis_type_multi_line:
            values.append("multi-line")
#            values.append('"type": "multi-line"')
        elif vis_type_scatter:
            values.append("scatter")
#            values.append('"type": "scatter"')
        else:
            values.append("unknown")
#            values.append('"type": "unknown"')
        text_elements = iframe_soup.find_all('g', attrs={'class':'type-text'})
        cnt = 0
        for text_element in text_elements:
            for text_item in text_element.find_all('text'):
                try:
                    if text_item.text[0]:
                        str_text = str(text_item.text)
			sub_values.append(str_text)

                        #values.append('"value'+str(cnt)+'": "'+str_text+'"')        
                        cnt = cnt + 1;
                except:
                    pass
        browser.close() 
    except TimeoutException:
        source = browser.page_source
        iframe_soup = BeautifulSoup(source, 'html.parser')
        error = iframe_soup.find('p', attrs={'class', 'flash alert alert-danger'})
        if error:
            values.append("matlab_err")
            #values.append('"type": "matlab code error"')
        else:
            img = iframe_soup.find('img', attrs={'class', 'plot_image'})
            if img:
                values.append("img")
                #values.append('"type": "img"')
            else:
                values.append("parse_error")
                #values.append('"type": "parse error"')
        browser.close()
        return values[0]
    return values[0]



#print load('https://thingspeak.com//apps/matlab_visualizations/20035?size=iframe')
#print load('https://thingspeak.com//apps/matlab_visualizations/190296?size=iframe')
#TODO print load('https://thingspeak.com//apps/matlab_visualizations/141714?size=iframe')
#print load('https://thingspeak.com//apps/matlab_visualizations/173485?size=iframe')

