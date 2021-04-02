# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


# [START User]
class User(ndb.Model):
    id = ndb.KeyProperty()
    name = ndb.StringProperty()
    password = ndb.IntegerProperty()
# [END User]

USER_KEY = None 

class Login(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render(template_values))
        # User(id = ndb.Key('User','1212'), name = 'a', password = 1212).put()
        # User(id = ndb.Key('User','11'), name = 'a', password = 1).put()
        # User(id = ndb.Key('User','22'), name = 'b', password = 2).put()
        # User(id = ndb.Key('User','33'), name = 'c', password = 777777).put()

        # User(id = ndb.Key('User','s3710760'), name = 'ZhenzhuoYe', password = 123456).put()
        # User(id = ndb.Key('User','s3710761'), name = 'ZhenzhuoYeA', password = 234567).put()
        # User(id = ndb.Key('User','s3710762'), name = 'ZhenzhuoYeB', password = 345678).put()


    def post(self):
        userIdInput = ndb.Key('User', self.request.get('userIdInput'))
        passwordInput = self.request.get('passwordInput')

        user_query = User.query(User.id == userIdInput)
        user = user_query.get()

        
        if user is not None:
            if int(user.password) == int(passwordInput):
                global USER_KEY
                USER_KEY = user.key
                self.redirect("/main")
                
            else:
                self.response.write("wrong password")
        else:
            self.redirect("/")




class MainPage(webapp2.RequestHandler):
    def get(self):
        userName = USER_KEY.get().name
        template_values = {
            'user_name': userName
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        input = self.request.get('option')
        if str(input) == "name":
            self.response.write("select name")
            self.redirect("/name")
        else:
            self.response.write("select password")
            self.redirect("/password")


class Name(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('name.html')
        self.response.write(template.render(template_values))

    def post(self):
        input = self.request.get('name')
        if(input != ''):
            user = USER_KEY.get()
            user.name = input
            user.put()
        else:
            self.redirect("/main")

        

class Password(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('password.html')
        self.response.write(template.render(template_values))
    def post(self):
        input = self.request.get('password')
        oldPassword = self.request.get('old_password')
        user = USER_KEY.get()

        if int(user.password) == int(oldPassword):
            user.password = int(input)
            user.put()
        else:
            self.redirect("/main")




     
app = webapp2.WSGIApplication([
    ('/', Login),
    ('/main', MainPage),
    ('/name', Name),
    ('/password', Password)

], debug=True)
