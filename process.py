import re
import watson
#import azure_query
import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import simplejson
from urlparse import urlparse
from urlparse import *
import ast
from pprint import pprint


# fixed nearly 30 items to remove quotes
# 3711.json tags super broken
# 256841.json had a \ to take out



# g1: super users?
# g2: languages?
# g3: static or dynamic graphs? per type?
# g4: what is being graphed? (based on tags, disc, axis names)
# g5: are certain graphs most commented upon? most shared?
# g6: do people make the same types of graphs?
# g7: how well do people describe graphs?
# g8: makeup of a channel (i.e. how many graphs / what grouping?)


# channel structure '{"name": "' + self.name + '", "gauges": "' + self.gauges + '", "gauges2": "' + self.gauges2 + '", "statuses": "' + self.statuses + '", "url": "' + self.url + '", "author": "' + self.author + '", "disc": "' + self.disc + '", "tags": ' + self.tags + ', "shares": "' + self.shares + '", "charts": ' + self.charts + ', "comments": ' + self.comments + ', "maps": "' + self.maps + '", "matlabs": "' + self.matlabs + '", "language": "' + self.language + '"}'

# forum structure forum[threads[posts[author,content]
# feeds {"channel":{"id":292812,"name":"BME280" 




d = {} #channels
r = {} #forums
l = {} #feeds
a = {} #author index
language_count = {}
chart_list = []
tag_list = []
discs = []
author_count = {}
tags_per_author = {}
num_authors = 0
num_tags = 0
num_languages = 0
num_disc = 0
num_graphs_w_xaxis = 0
num_graphs_w_yaxis = 0
avg_number_graphs_w_any_axis_label_per_author = 0
avg_tags_per_author = 0
avg_graphs_per_author = 0
avg_disc_length = 0
num_comments = 0
num_comments_with_link = 0
num_line_charts = 0
num_gauges = 0
num_images = 0


def word_cloud():
    global tag_list
    tag_list2 = filter( lambda x: ( 'temp' not in x.lower() ) and ( 'hum' not in x.lower() ) and ( 'dew' not in x.lower() ) and ( 'weather' not in x.lower() ), tag_list )
    word_str = '+'.join(tag_list2)
    wordcloud = WordCloud(width=1000, height=500, regexp=r"\w[\w' ]+").generate(word_str)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    wordcloud = WordCloud(max_font_size=40).generate(word_str)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

def word_cloud_array(array):
    word_str = ''.join(array)
    wordcloud = WordCloud().generate(word_str)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    wordcloud = WordCloud(max_font_size=40).generate(word_str)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    

def load_to_mem(forums_on, channels_on, feeds_on):
    global d
    global r
    global a
    global r
    cnt = 0
    if forums_on:
        for filename in os.listdir("./forums"):
            #print filename
            if ".json" in filename and not filename == ".json":
                fi = open("./forums/"+filename, "r")
                j_str = fi.read()
                j = ast.literal_eval(j_str)
                url = j['url']
                url_s = url.split("/")
                forum_name = url_s[-3] # + "-" + url_s[-2]
        
                #reverse forum into author index
                f_dd = {}
                for thread in j['threads']:
                    thread_url = thread['url']
                    posts = thread['posts']
                    for post in posts:
                        rev_post = {}
                        author = post['author']
                        date = post['date']
                        content = post['content']
                        rev_post['date'] = date
                        rev_post['content'] = content
                        rev_post['thread_url'] = thread_url
                        rev_post['forum_name'] = forum_name
                        rev_post['forum_url'] = url


                        print author + "," + clean_text(content)

                        #wt = watson.run_watson(clean_text(content))
                        #print author + "@@@" + clean_text(content) + "@@@" + wt
                        #exit()
                        
                        '''
                        try:
                            f_dd[content] = f_dd[content] + 1
                        except:
                            f_dd[content] = 1
                        '''

                        try: 
                            a[author].append(rev_post)
                        except:
                            a[author] = []
                            a[author].append(rev_post)

                
                try:
                    g = r[forum_name]
                    r[forum_name] = g.append(j)
                except:
                    r[forum_name] = []
                    r[forum_name].append(j)

                 

                '''
                for author, value in a.iteritems():
                    for post in value:
                        ct = clean_text(post['content'])
                        wt = watson.run_watson(ct)
                        print author + "@@@" + ct + "@@@" + str(wt)
                '''

                '''
                threads = j['threads']
                for thread in threads:
                    posts = thread['posts']
                    for post in posts:
                        print post
                        exit()
                '''
                '''
                for r in a:
                    print r
                    exit()
                '''
    if channels_on:
        for filename in os.listdir("./json/"):
            if ".json" in filename and not filename == ".json":
                #print filename
                fi = open("./json/"+filename,"r")
                j_str = fi.read()
                
                if '"tags": ]' in j_str: #fix broken tags section :/
                    j_str = j_str.replace('"tags": ]', '"tags": []') 
               
                if '"charts": ]' in j_str: #fix broken tags section :/
                    j_str = j_str.replace('"charts": ]', '"charts": []') 

                j_str = j_str.replace("\n",'').replace('\r','').replace('\t','')

                if "}{" in j_str: #fix append error
                    n = j_str.find("}{")
                    j_str = j_str[:n+1]
                js = simplejson.loads(j_str)
                d[filename[:-5]] = j_str
    if feeds_on:
        for filename in os.listdir("./feeds/"):
            if ".json" in filename and not filename == ".json":
                #print filename
                fi = open("./feeds/"+filename,"r")
                j_str = fi.read()
                #print j_str
                js = simplejson.loads(j_str)
                l[filename[:-5]] = j_str


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
    #print tags_per_author
    

def extract(j_str):
    global tag_list
    global author_count
    global tags_per_author
    global language_count
    global discs
    #print j_str
   
    #exit()

    ''' 
    uf_discs = {}
    f = open('discs_labeled.csv','r')
    dis = f.read()
    dis_s = dis.split("\n")
    for line in dis_s:
        if len(line.split(",")) == 2:
            l_spl = line.split(",")
            disc = l_spl[0]
            label = l_spl[1]
            uf_discs[disc] = label
    '''
    
    
    
    j = json.loads(j_str)
    tags = j['tags']
    author = j['author']
    charts = j['charts']
    language = j['language']
    disc = j['disc']
    c_id = j['url'].split("/")[-1]

    REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

    if not len(disc) == 0 and language == 'en':
        #disc = [REPLACE_NO_SPACE.sub("", line.lower()) for line in disc]
        #disc = [REPLACE_WITH_SPACE.sub(" ", line) for line in disc]
        discs.append(clean_text(disc))
#        print author + "@@@" + clean_text(disc) + "@@@" + c_id + "@@@" + azure.run_azure_keywords(clean_text(disc))
#        exit()


    try:
        cur = language_count[language]
        cur = cur + 1
        language_count[language] = cur
    except:
        language_count[language] = 0

    # construct word_str for word cloud 
    for tag in tags:
        tag_list.append(tag)

    # sort into author list
    try:
        author_count[author] = author_count[author] + 1
    except:
        author_count[author] = 1
    #print "authors: " + str(len(author_count.keys()))



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

    # all charts
    for chart in charts:
        chart_list.append([chart,c_id])


def parse_update(url):
    qs = urlparse(url)[4]
    o = parse_qs(qs)
    try:
        return o['update']
    except:
        return None

def parse_title(url):
    qs = urlparse(url)[4]
    o = parse_qs(qs)
    try:
        return o['title']
    except:
        return None

        

def test_retrieve(index):
    global d
    try:
        j_str = d[str(index)]
        extract(j_str)
    except:
        print index
        print j_str
        cnt = cnt + 1

def query_forum():
    global a
    for key, value in a.iteritems():
        #print key
        #exit()
        try:
            print key, len(f[key])
        except:
            pass
    #exit()

def query_all():
    global d
    for key,value in d.iteritems():
        extract(d[key])

def feed_parsing():
    global l
    for key, value in l.iteritems():
        js = simplejson.loads(value)
        print js['channel']['id']

def chart_parsing():
    line = 0
    line_titles = []
    line_update = []
    video = 0
    status = 0
    maps = 0
    total = 0
    column = 0
    column_titles = []
    column_update = []
    spline = 0
    spline_titles = []
    spline_update = []
    bar = 0
    bar_titles = []
    bar_update = []
    step = 0
    step_titles = []
    step_update = []
    unknown = 0
    unknown_titles = []
    unknown_update = []
    for chart_l in chart_list:
        chart = chart_l[0]
        uid = chart_l[1]
        total += 1
        if "type=line" in chart:
            line += 1
            print "line,"+uid
            title = parse_title(chart)
            if title:
                line_titles.append(title[0])
            update = parse_update(chart)
            if update:
                line_update.append(update[0])
        elif "www.youtube.com" in chart:
            video += 1
            print "video,"+uid
        elif "status/recent" in chart:
            status += 1
            print "s,"+uid
        elif "type=column" in chart:
            column += 1
            print "column,"+uid
            title = parse_title(chart)
            if title:
                column_titles.append(title[0])
            update = parse_update(chart)
            if update:
                column_update.append(update[0])
        elif "type=spline" in chart:
            spline += 1
            print "spline,"+uid
            title = parse_title(chart)
            if title:
                spline_titles.append(title[0])
            update = parse_update(chart)
            if update:
                spline_update.append(update[0])
        elif "type=bar" in chart:
            bar += 1
            print "bar,"+uid
            title = parse_title(chart)
            if title:
                bar_titles.append(title[0])
            update = parse_update(chart)
            if update:
                bar_update.append(update[0])
        elif "type=step" in chart:
            step += 1
            print "step,"+uid
            title = parse_title(chart)
            if title:
                step_titles.append(title[0])
            update = parse_update(chart)
            if update:
                step_update.append(update[0])
        elif "maps/channel_show" in chart:
            print "map,"+uid
            maps += 1
        elif "channel" in chart and "chart" in chart:
            print "unknown,"+uid
            unknown += 1
            title = parse_title(chart)
            if title:
                unknown_titles.append(title[0])
            update = parse_update(chart)
            if update:
                unknown_update.append(update[0])
        else:
            pass
    #        print chart
    #word_cloud_array(line_titles)
#    print line, video, status, maps, total, column, spline, bar, step, unknown





def rake():
    from rake_nltk import Rake, Metric
    #r = Rake()
    r = Rake(ranking_metric=Metric.WORD_FREQUENCY)
    words = ""
    for disc in discs:
        words = words + ". " + disc
    r.extract_keywords_from_text(words)
    print r.get_ranked_phrases_with_scores()

    '''
    tags = ""
    for tag in tag_list:
        tags =  tags + " " + tag
    r.extract_keywords_from_text(tags)
    print r.get_ranked_phrases_with_scores()
    '''


def create_author_index():
    pass

#    words = get_all_descriptions()

def clean_text(text):
    text = text.encode('utf-8')
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip(' ')
    return text


    '''
    for line in dis.split("\n"):
        l_spl = line.split(",")
        print line
    '''


load_to_mem(False, True, False)
query_all()
#for disc in discs:
#    print clean_text(disc)

#query_forum()


#rake()

#print len(language_count.keys())
# chart_parsing()
#feed_parsing()

#print len(tag_list)
#print len(discs)

#print line, video, status, maps, total

#print tag_list

word_cloud()
#author_histogram()
#tag_per_author()
#test_retrieve(40150)
#for key, value in d.iteritems() :
#    print key
