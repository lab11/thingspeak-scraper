import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# fixed nearly 30 items to remove quotes
# 3711.json tags super broken
# 256841.json had a \ to take out


d = {}

tag_list = []



def word_cloud():
    global tag_list
    word_str = ''.join(tag_list)
    wordcloud = WordCloud().generate(word_str)
    


    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")



    # lower max_font_size
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


def extract(j_str):
    global tag_list
    j = json.loads(j_str)
    tags = j['tags']
    for tag in tags:
        tag_list.append(tag)

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
#print tag_list
word_cloud()

#test_retrieve(40150)
#for key, value in d.iteritems() :
#    print key
