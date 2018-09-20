
import requests
subscription_key = '0f27bbcf921f4891b9c52819f96fb41a'
#'371c2fad1bb8416fb36b741444a26aa5'
assert subscription_key
analytics_base_url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/"


import os

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]


e = {}

def do_forum():
    cnt = 0
    f = open('author_forum', 'r')
    forums = f.read()
    lines = forums.split("\n")
    documents = list(chunks(lines, 500))
    for document in documents:
        c_json = {}
        c_json['documents'] = []
        for line in document:
            try:
                f_spl = line.split(",")
                e[cnt] = line
                author = f_spl[0]
                post = f_spl[1][:4500]
                #print len(post)
                c_json['documents'].append( { 'id': cnt, 'text': post })
            except:
                print line
            cnt = cnt+1
        text_analytics_base_url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/"
        sentiment_api_url = text_analytics_base_url + "sentiment"
        headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
        response  = requests.post(sentiment_api_url, headers=headers, json=c_json)
        key_phrases = response.json()
        docs = key_phrases['documents']
        for doc in docs:
            print str(e[int(doc['id'])]) + "," + str(doc['score'])
#        print e
            
        #print key_phrases

def do_keywords():
    f = open('discs_labeled_indexed.csv','r')
    discs = f.read()
    c_json = {}
    c_json['documents'] = []

    b_json = {}
    b_json['documents'] = []


    A = discs.split("\n")
    B = A[:len(A)//2]
    C = A[len(A)//2:]


    for line in C:
        try:
            disc = line.split(",")[1]
            if len(disc) > 0:
                j_str = "{ 'id': '" + line.split(",")[2] + "', 'text': '" + disc + "'}"
                c_json['documents'].append( { 'id': line.split(",")[2], 'text': disc })
        except:
            pass

    for line in B:
        try:
            disc = line.split(",")[1]
            if len(disc) > 0:
                j_str = "{ 'id': '" + line.split(",")[2] + "', 'text': '" + disc + "'}"
                b_json['documents'].append( { 'id': line.split(",")[2], 'text': disc })
        except:
            pass

    text_analytics_base_url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/"
    key_phrase_api_url = text_analytics_base_url + "keyPhrases"
    headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
    response  = requests.post(key_phrase_api_url, headers=headers, json=c_json)
    key_phrases = response.json()
    print key_phrases

    text_analytics_base_url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/"
    key_phrase_api_url = text_analytics_base_url + "keyPhrases"
    headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
    response  = requests.post(key_phrase_api_url, headers=headers, json=b_json)
    key_phrases = response.json()
    print key_phrases



do_forum()

#print run_azure_keywords('try to find the keywords')

#thingspeak
#371c2fad1bb8416fb36b741444a26aa5
#4f44a20351ea402bb4ce166c475d3d15
