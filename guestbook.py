import cgi
import sys
sys.path.insert(0,'libs')

from google.appengine.api import users

import webapp2
import urllib
from bs4 import BeautifulSoup
sample = ""
title = " "

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/sign" method="post">
      <title>Hello World Page</title>
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
  </body>
</html>
"""

def getSiteData(url):
    	sock = urllib.urlopen(url)
    	htmlSource = sock.read()
    	sock.close()
    	sample = htmlSource
    	
class HtmlParser:
    def __init__(self):
    	sock = urllib.urlopen("http://canvasjs.com")
    	data = sock.read()
    	sock.close()
    	if "<title>" in data:
    		start = data.index("<title>") + 7
    		end = data.index("</title>")
    		title = data[start:end]



class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_HTML)


class Guestbook(webapp2.RequestHandler):
	   
    def post(self):    	
    	parser = HtmlParser()
    	#sock = urllib.urlopen("http://canvasjs.com")
    	#htmlSource = sock.read()
    	#sock.close()
    	#sample = cgi.escape(htmlSource)    	
    	sock = urllib.urlopen("http://sourcebits.com")
    	data = sock.read()
    	sock.close()

    	if "<meta name=\"description\"" in data:
    		tempind1 = data.index("meta name=\"description\"")
    		tempstr1 = data[tempind1:]
    		end = tempstr1.index("/>") - 1
    		start = tempstr1.index("content=") + 9
    		keywords = tempstr1[start:end]
    		title = keywords
    	#if "<meta name=\"keywords\"" in data:
    		#tempind1 = data.index("meta name=\"keywords\"")
    		#tempstr1 = data[tempind1:]
    		#end = tempstr1.index("/>") - 1
    		#start = tempstr1.index("content=") + 9
    		#keywords = tempstr1[start:end]
    		#title = keywords
    	#if "<title>" in data:
    	#	start = data.index("<title>") + 7
    	#	end = data.index("</title>")
    	#	title = data[start:end]
    	#if "<title>" not in data:
    	#	title  = "whatever"

    	self.response.write('<html><body>You wrote:<pre>')
    	self.response.write(title)
    	self.response.write('</pre></body></html>')


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)