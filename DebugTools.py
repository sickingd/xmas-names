import os
import urllib

from google.appengine.ext import ndb

import jinja2
import webapp2
import logging

import ChristmasNames


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])



class GenerateTestPeople(webapp2.RequestHandler):

    def post(self):
        A1 = ChristmasNames.Person(name='A', 
                          family='AA', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')],
                          is_admin=True)
        A1.put()
        A2 = ChristmasNames.Person(name='A', 
                          family='BB', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')],
                          is_admin=True,
                          email='sickingd@gmail.com')
        A2.put()
        
        B1 = ChristmasNames.Person(name='B', 
                          family='AA', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')])
        B1.put()
        B2 = ChristmasNames.Person(name='B', 
                          family='BB', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')],
                          email='sickingd@gmail.com')
        B2.put()

        C1 = ChristmasNames.Person(name='C', 
                          family='AA', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')])
        C1.put()
        C2 = ChristmasNames.Person(name='C', 
                          family='BB', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')],
                          email='sickingd@gmail.com')
        C2.put()

        D = ChristmasNames.Person(name='D', 
                          family='AA', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')])
        D.put()

        E = ChristmasNames.Person(name='E', 
                          family='AA', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')])
        E.put()

        F = ChristmasNames.Person(name='F', 
                          family='AA', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')])
        F.put()
        
        
        self.redirect("/admin")


