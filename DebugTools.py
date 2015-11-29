import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2
import random
import logging
import copy

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
                          is_admin=True)
        A2.put()
        
        B1 = ChristmasNames.Person(name='B', 
                          family='AA', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')])
        B1.put()
        B2 = ChristmasNames.Person(name='B', 
                          family='BB', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')])
        B2.put()

        C1 = ChristmasNames.Person(name='C', 
                          family='AA', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')])
        C1.put()
        C2 = ChristmasNames.Person(name='C', 
                          family='BB', 
                          items=[ChristmasNames.Item(description='Google', link='https://google.com'),
                                 ChristmasNames.Item(description='Yahoo', link='https://yahoo.com')])
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
        
        A1.assigned_name_key = B1.key
        A1.assigned_name = B1.name
        A1.is_assigned = True
        A1.put()
        A2.assigned_name_key = C2.key
        A2.assigned_name = C2.name
        A2.is_assigned = True
        A2.put()
        B1.assigned_name_key = C1.key
        B1.assigned_name = C1.name
        B1.is_assigned = True
        B1.put()
        B2.assigned_name_key = A2.key
        B2.assigned_name = A2.name
        B2.is_assigned = True
        B2.put()     
        C1.assigned_name_key = A1.key
        C1.assigned_name = A1.name
        C1.is_assigned = True
        C1.put()            
        C2.assigned_name_key = B2.key
        C2.assigned_name = B2.name
        C2.is_assigned = True
        C2.put()            
        D.assigned_name_key = E.key
        D.assigned_name = E.name
        D.is_assigned = True
        D.put()      
        E.assigned_name_key = F.key
        E.assigned_name = F.name
        E.is_assigned = True
        E.put()         
        F.assigned_name_key = D.key
        F.assigned_name = D.name
        F.is_assigned = True
        F.put()       
        
        self.redirect("/")


