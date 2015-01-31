# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2
from BeautifulSoup import BeautifulSoup as bs
from pdb import set_trace as dbg
import re
import copy
import json

# class HackerNewsRest(BaseHTTPRequestHandler):
#     def do_GET(self):
#         pass

class yCombinatorParser(object):
    __url = "https://news.ycombinator.com/"
    __datajson = {
        "nextId":2,
        "items":
        [],
        "version":"0.1a"
    }
    __data_item = {
        "title":"",
        "url":"",
        "id":"",
        "commentCount":"",
        "points":"",
        "postedAgo":"",
        "postedBy":""
    }

    __d = re.compile("\d*")

    def __init__(self):
        self.refresh()

    def refresh(self):
        try:
            self.__data = bs(urllib2.urlopen(self.__url).read())('tr')
        except:
            print("Failed to get %s"%self.__url)

    def parse(self):
        for i in xrange(4,len(self.__data)-5, 3):
            print("it: %s" % i);
            url = self.__data[i]('td')[2]
            item = copy.deepcopy(self.__data_item)
            item["title"] = url.a.text
            item["url"] = url.a.attrs[0][1]
            td = self.__data[i+1]
            td = td('td')
            td = td[1]
            if not td.span is None:
                tdf = self.__d.match(td.span.text)
                item["points"] = td.span.text[tdf.start():tdf.end()]
                item["postedBy"] = td('a')[0].text
                tdf = self.__d.match(td('a')[1].text)
                item["commentCount"] = td('a')[0].text[tdf.start():tdf.end()]
            self.__datajson["items"].append(item)


    def getData(self):
        return self.__data

    def getJson(self):
        return json.dumps(self.__datajson)
