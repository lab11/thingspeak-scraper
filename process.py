import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

# fixed nearly 30 items to remove quotes
# 3711.json tags super broken
# 256841.json had a \ to take out


d = {}

tag_list = []
author_count = {}
tags_per_author = {}


def word_cloud():
    global tag_list
    word_str = ''.join(tag_list)
    wordcloud = WordCloud().generate(word_str)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    wordcloud = WordCloud(max_font_size=40).generate(word_str)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
def load_to_mem():
    global d
    cnt = 0
    for filename in os.listdir("./json/"):
        if ".json" in filename:
            f = open("./json/"+filename,"r")
            j_str = f.read()
            if '"tags": ]' in j_str: #fix broken tags section :/
                j_str = j_str.replace('"tags": ]', '"tags": []') 
           
            if '"charts": ]' in j_str: #fix broken tags section :/
                j_str = j_str.replace('"charts": ]', '"charts": []') 

            j_str = j_str.replace("\n",'')

            if "}{" in j_str: #fix append error
                n = j_str.find("}{")
                j_str = j_str[:n+1]

            d[filename[:-5]] = j_str

def author_histogram():
    global author_count 
    num_channels_np = map(int, author_count.values())
    num_channels = np.array(num_channels_np)
    max_cnt = 0
    for num in num_channels_np:
        if max_cnt < num:
            max_cnt = num
    bins = range(0, max_cnt+10)
    plt.hist(num_channels, bins=bins) 
    #plt.yscale('log', nonposy='clip')
    plt.yscale('log')
    plt.title("histogram") 
    plt.show()

def tag_per_author():
    global tags_per_author
    print tags_per_author
    

def extract(j_str):
    global tag_list
    global author_count
    global tags_per_author
    j = json.loads(j_str)
    tags = j['tags']
    author = j['author']

    # construct word_str for word cloud 
    for tag in tags:
        tag_list.append(tag)

    # sort into author list
    try:
        author_count[author] = author_count[author] + 1
    except:
        author_count[author] = 1


    # tags per author
    try:
        cur_tag_list = tags_per_author[author];
        for tag in tags:
            cur_tag_list.append(tag)
        tags_per_author[author] = cur_tag_list
    except:
        cur_tag_list = []
        for tag in tags:
            cur_tag_list.append(tag)
        tags_per_author[author] = cur_tag_list

def test_retrieve(index):
    global d
    try:
        j_str = d[str(index)]
        extract(j_str)
    except:
        print index
        print j_str
        cnt = cnt + 1
    
def query_all():
    global d
    for key,value in d.iteritems():
        extract(d[key])

load_to_mem()
query_all()

print tag_list

#word_cloud()
#author_histogram()
#tag_per_author()

#test_retrieve(40150)
#for key, value in d.iteritems() :
#    print key
