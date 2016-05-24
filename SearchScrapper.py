# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:56:47 2015

@author: prakhar

"""

from urllib2 import urlopen
from bs4 import BeautifulSoup
import requests
import urlparse
import sqlite3
import re
import tweepy
import subprocess
import datetime


#mainURL
url = 'http://www.news18.com/search-result.php'
poll_url = 'http://www.news18.com'
poll_url_POST = 'http://www.news18.com/index.php/?pollone=poll-submitted'
news_headings = []
news_href = []
news_summary = []
final_news = []
i=0
answer_code = 0

'''
#Creates Database and obtain cursor
createDB = sqlite3.connect('/home/prakhar/Desktop/scraping/news18.db')
qc = createDB.cursor()


#takes user input
def TakeInput(i):
    if i == 1:
        query_string = raw_input("\nEnter the query to be searched: ").lower()
        return query_string
    if i == 2:
        query_state = raw_input("\nEnter the state for news: ").lower()
        return query_state
'''

#requests data    
def SendPostRequest(url,p):
    try:
        postIt = requests.post(url,data=p)
        return postIt
    except Exception as e:
        print e

'''
#BeautifulSoup Obj Creator
def CreateBeautifulSoupObj(s):
    soup = BeautifulSoup(s)
    return soup


#Prints Instructions
def Instructions(p):
    print '\n\n...............News Search - www.news18.com ..............\n'
    print ':: Below are the parameters of your search ::\n'
    print p
    print '-'*90
    
    
#Link Extractor
def ExtractLinks(soup):
    for i in soup.find_all('li','clearfix'):
        headlines = i.find('p').find('a',href=True).contents[0]
        link = i.find('p').find('a',href=True)
        #print link['href']
        news_headings.append(headlines)
        news_href.append(link['href'])
    #print news_headings[0]
    #print news_href[0]   
    return news_headings, news_href


#News Extractor
def ExtractNews(i):        
    while i < len(news_href):
        
        tempURL = news_href[i]
        html = urlopen(tempURL)
        htmlText = html.read()
        html.close()
        
        soup = BeautifulSoup(htmlText)
        #n = soup.find('article',{"id":"story_box"}).find('aside',{'id':'mid_box_inner'}).findAll('p')[:]
        news_summary.append(soup.find('article',{"id":"story_box"}).find('aside',{'id':'mid_box_inner'}).findAll('p')[:]) 
        #print soup.find('article',{"id":"story_box"})
        i += 1
        
    return news_summary


#Clean Text
def CleanNews(n):
    nws = re.sub('<[^>]*>', '', n)
    nws = re.sub('#','',nws)
    nws = nws.strip()
    return nws

        
#---------------------------------------------------------------------------------------------
#--------------------------------------------------MAIN BEGINS--------------------------------
#---------------------------------------------------------------------------------------------



#User Input and string transformation    
query_string = TakeInput(1).replace(' ','+')
query_state = TakeInput(2).replace(' ','-')
param = {'search_type':'news','query_string':query_string,'search_state':query_state,'search_city':'','limit':'10'}


#prints Instructions
Instructions(param)


#send post request
try:
    search = SendPostRequest(url,param)
except Exception as e:
    print e
    
soup = CreateBeautifulSoupObj(search.text)

news_headings,news_href = ExtractLinks(soup)

news_summary = ExtractNews(i)   

    
#print news_summaryy
for i in news_summary[:]:
    j=0
    while j < len(i):
        news = str(i[j]) 
        news_clean = CleanNews(news)
        final_news.append(news_clean)
        print news_clean
        j+=1
    print '.'*95
    print '\n' 
    
    

#print final_news[2]



############################################################################
#                Ask if user wants to tweet the news
############################################################################


tweet_response = raw_input("Do you want to tweet the news(y/n): ").lower()

ckey = 'QMnucKw3xZ57tjf1ZXQmitkg8'
csecret = 'l2BGiHUVDE7rEAs2pfQ7H2b4hxnPh30PhFIpLVFZ0ExYDFSy5K'
atoken = '285448554-u28HxHmKOaxqg0OAASwraH0jUKlT3ZToKUy9DrB8'
asecret = 'QhmW7Wixxq5bqdkFyuLKma6GTWg2O1M9K3tXgc0W1Pi49'

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

if tweet_response == 'y':
    news_index = int(raw_input("Enter the news index[0,1,....,8,9] : "))
    api.update_status(status=str(news_href[news_index]))
    print '\n\n:::::: Status updated successfully :::::::\n'
if tweet_response == 'n':
    print '\n\nWe respect your decision\n'

'''

'''
for i in final_news[:3]:
    print i
############################################################################
#                Ask if user wants to speak out the news
############################################################################ 


activeEspeak = raw_input("Do you wish to listen any news(y/n): ").lower()

if activeEspeak:
    idx = int(raw_input("Enter the news index[0,1,....,8,9] : "))
    text = str(final_news[idx])
    print text
   
    #subprocess.call('espeak '+text, shell=True)
#else:
#    print '\n\nWe respect your decision\n'''






############################################################################
#                Ask if user wants to poll
############################################################################

wants_to_poll = raw_input("Do you wish to use news18 poll option(y/n): ").lower()

html = urlopen(poll_url)
htmlText = html.read()
html.close()

soup = BeautifulSoup(htmlText)


def FetchPoll(soup):
	for p in soup.find_all('div',{'id':'pool1'}):
		question = p.find('div','poll_question_cls').contents[0]
		options = p.find_all('li','poll_ans_li_cls')

		option1 = options[0].next.next.strip()
		value1 = options[0].contents[0]['value']

		option2 = options[1].next.next.strip()
		value2 = options[0].contents[0]['value']
	
	return question, option1, value1, option2, value2


question, option1, value1, option2, value2 = FetchPoll(soup)

dict_opt_val = {'option1':value1,'option2':value2}

print 'Q. ', question
print '\n', option1, '\n', option2

option_input = int(raw_input('\n\ntype 1 or 2 to select options\n'))

if option_input == 1:
	value = dict_opt_val['option1']
if option_input == 2:
	value = dict_opt_val['option2']

#time = subprocess.call('date')
#time = str(time) + 'GMT+0530 (India Standard Time)'
#today = datetime.date.today()
#t = datetime.time(0)
#print t, 'GMT+0530 (India Standard Time)'
fd = {'ans':'value','timestamp':'Thu Oct 01 2015 17:40:34 GMT+0530 (India Standard Time)','action':'0.13215709175698032'}
response_poll = SendPostRequest(poll_url_POST,fd)

soup = BeautifulSoup(response_poll.text)
print soup






