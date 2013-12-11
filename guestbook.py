from google.appengine.api import users
import urllib
import webapp2
import cgi
import json
from urlparse import urlparse
#from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
#from google.appengine.api import mail


DEFAULT_GUESTBOOK_NAME = "default_book"

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    return ndb.Key('Guestbook',guestbook_name)

class Website(ndb.Model):   
    url = ndb.StringProperty(required=True)
    title = ndb.StringProperty()
    keywords = ndb.StringProperty()
    description = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add = True)


class HTMLParser:
    def __init__(self, url):
        self.url = url      
        try:
            sock = urllib.urlopen(url)
            data = sock.read()
            sock.close()
            self.Error = ""
        except Exception, e:
            data = ""
            self.Error = "Error Occurd!"            
        
        if "<title>" in data:
            start = data.index("<title>") + 7
            end = data.index("</title>")
            self.title = data[start:end]
            #webData.title = self.title
            #return title
        else:
            self.title = "Not found!"
        if "<meta name=\"keywords\"" in data:
            tempind1 = data.index("meta name=\"keywords\"")
            tempstr1 = data[tempind1:]
            end = tempstr1.index("/>") - 1
            start = tempstr1.index("content=") + 9
            self.keywords = tempstr1[start:end]
            #webData.keywords = self.keywords
            
        else:
            self.keywords = "Not found"

        if "<meta name=\"description\"" in data:
            tempind1 = data.index("<meta name=\"description\"")
            tempstr1 = data[tempind1:]
            end = tempstr1.index("/>") - 1
            start = tempstr1.index("content=") + 9
            self.description = tempstr1[start:end]
            #webData.description = self.description
            
        else:
            self.description = "Not found"

        self.siteInfo = {"Error":self.Error,"url":self.url,"title":self.title,"keywords":self.keywords,"description":self.description}


class MainPage(webapp2.RequestHandler):
    def get(self):
        # if users.get_current_user():
        #   url = users.create_logout_url(self.request.uri)
        #   url_linktext = 'Logout'

        # else:
        #   url = users.create_login_url(self.request.uri)
        #   url_linktext = 'Login'
        guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
        website_query = Website.query(ancestor=guestbook_key(guestbook_name)).order(-Website.date)
        websites = website_query.fetch()

        template_values = {
            'websites':websites,            
        }
        self.response.write(template.render('index.html',template_values))
                
        
class Guestbook(webapp2.RequestHandler):
    def post(self):
        website = self.request.get('domain')
        website_title = self.request.get('title')
        website_keywords = self.request.get('keywords')
        website_description = self.request.get('description')

        
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)

        greeting = Website(parent = guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()
        greeting.url = website
        greeting.title = website_title
        greeting.keywords = website_keywords
        greeting.description = website_description
        greeting.put()

        query_params = {'guestbook_name':guestbook_name}
        self.redirect('/?')

class GetSiteData(webapp2.RequestHandler):  
    def post(self):
        url = urlparse(self.request.POST['website'])        
        dd = ""
        if url.scheme:          
            dd = url.scheme + "://"
        else:
            dd = "http://"

        if url.netloc:
            dd = dd + url.netloc
        else:
            dd = dd + url.path

        temp = HTMLParser(dd)       
        self.response.write(json.dumps(temp.siteInfo));
        
class Delete(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
        website_query = Website.query(ancestor=guestbook_key(guestbook_name)).order(-Website.date)
        websites = website_query.fetch()
        for website in websites:
            website.key.delete()
            websites = website_query.fetch()

        self.redirect('/?')
    
application = webapp2.WSGIApplication([
        ('/',MainPage),
        ('/getdata',GetSiteData),
        ('/sign',Guestbook),
        ('/delete',Delete)],debug=True)