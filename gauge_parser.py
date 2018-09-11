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

from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor

from pyjsparser import PyJsParser
p = PyJsParser()

# https://thingspeak.com//apps/plugins/166139
# https://thingspeak.com//apps/plugins/6732


def load(link):
    delay = 5
    values = []
    sub_values = []
    gauge_source = ""

    done = False
    
    # 'image 1
    '''
    channel = urllib2.urlopen(link)
    html = channel.read()
    img_soup = BeautifulSoup(html, 'html.parser')
    if img_soup.find('img'):
        values.append('gauge_img')
        return values
    '''

    browser = webdriver.Chrome()
    browser.get(link)

    #gauge
    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gauge_div"]/table/tbody/tr'))) #'//*[@id="gauge_div"]')))
        gauge_source = browser.page_source 
        iframe_soup = BeautifulSoup(gauge_source, 'html.parser')
        charts_soup = iframe_soup.find_all('text')
        values.append("gauge")
        for chart_soup in charts_soup:
            sub_values.append(chart_soup.text)
        done = True
    except TimeoutException:
        pass
    
    # "multi-gauge"
    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="chart_div2"]/table'))) #'//*[@id="chart_div1"]')))
        gauge_source = browser.page_source 
        iframe_soup = BeautifulSoup(gauge_source, 'html.parser')
        charts_soup = iframe_soup.find_all('div', {"id" : lambda L: L and L.startswith('chart_div')})
        values.append('multi-gauge')
        for chart_soup in charts_soup:
            gauges_soup = chart_soup.find_all('text')
            for gauge_soup in gauges_soup:
                sub_values.append(gauge_soup.text)
        done = True
    except:
        pass
    
    #gauge1
    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gauge1_div"]/table/tbody/tr'))) #'//*[@id="gauge_div"]')))
        gauge_source = browser.page_source 
        iframe_soup = BeautifulSoup(gauge_source, 'html.parser')
        charts_soup = iframe_soup.find_all('text')
        values.append("gauge")
        for chart_soup in charts_soup:
            sub_values.append(chart_soup.text)
        done = True
    except TimeoutException:
        pass

    #led
    try:
        if not done:
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="AQI"]'))) #'//*[@id="gauge_div"]/table/tbody/tr'))) #'//*[@id="gauge_div"]')))
            gauge_source = browser.page_source 
            values.append("LED")
            iframe_soup = BeautifulSoup(gauge_source, 'html.parser')
            led = iframe_soup.find('div', attrs={'id':'LED'})
            values.append(led.get('class')[0])
            value = iframe_soup.find('p', attrs={'id': 'AQI'})
            values.append(value.text)
            state = iframe_soup.find('p', attrs={'id': 'STATE'})
            values.append(state.text)
            done = True
    except TimeoutException:
        pass

    # chart
    try:
        if not done:
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="chart-container"]'))) 
            gauge_source = browser.page_source 
            iframe_soup = BeautifulSoup(gauge_source, 'html.parser')

            try:
                if iframe_soup.find('img'):
                    values.append('gauge_image')
                    done = True
                bar = False
                if iframe_soup.find('g', attrs={'class':'highcharts-markers highcharts-series-0 highcharts-column-series '}):
                    bar = True
                if bar and not done:
                    values.append("gauge_bar_chart")
                    values.append(iframe_soup.find('g', attrs={'class':'highcharts-title'}).find('tspan').text)
                else: 
                    values.append("gauge_chart")
                    legends_soup = iframe_soup.find_all('g',attrs={'class','highcharts-legend-item'})
                    for legend_soup in legends_soup:
                        values.append(legend_soup.text)
                    title_soup = iframe_soup.find('text', attrs={'class','highcharts-title'}).find('tspan').text
                    values.append(title_soup)
                    axi_soup = iframe_soup.find_all('g', 'highcharts-axis')
                    for axis_soup in axi_soup:
                        if axis_soup.find('text', attrs={'transform':'translate(0,0)'}): #xaxis
                            sub_values.append(axis_soup.find('tspan').text) 
                        else:
                            sub_values.append(axis_soup.find('tspan').text)
                    done = True
            except:
                pass
    except TimeoutException:
            pass


    if len(values) == 0:
        values.append('parse_error')
    browser.close()
    return values

#print load('https://thingspeak.com//apps/matlab_visualizations/20035?size=iframe')
#print load('https://thingspeak.com//apps/matlab_visualizations/190296?size=iframe')
#TODO print load('https://thingspeak.com//apps/matlab_visualizations/141714?size=iframe')
#print load('https://thingspeak.com//apps/matlab_visualizations/173485?size=iframe')
#print load('https://thingspeak.com//apps/plugins/36883')
#print load('https://thingspeak.com//apps/plugins/166139')
#print load('https://thingspeak.com//apps/plugins/6732')
#print load('https://thingspeak.com//apps/plugins/3179')
#print load('https://thingspeak.com//apps/plugins/14346')
