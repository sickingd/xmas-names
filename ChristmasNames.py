import os
import urllib

from google.appengine.ext import ndb

import jinja2
import webapp2
import logging
import copy

import Lists
import DebugTools
import Admin


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class Item(ndb.Model):
    description = ndb.StringProperty()
    link = ndb.StringProperty()
    is_fulfilled = ndb.BooleanProperty()
    
class Person(ndb.Model):
    name = ndb.StringProperty()
    family = ndb.StringProperty()
    email = ndb.StringProperty()
    is_assigned = ndb.BooleanProperty()
    exclude = ndb.StringProperty(repeated=True)
    assigned_name_key = ndb.KeyProperty()
    assigned_name = ndb.StringProperty()
    list = ndb.TextProperty()    
    list_updated = ndb.BooleanProperty()
    is_admin = ndb.BooleanProperty()
    items = ndb.StructuredProperty(Item, repeated=True)

    
class MainPage(webapp2.RequestHandler):

    def get(self):
        all_names = Person.query().fetch(1000)
        
        #Find out the website for each person, display that in the list
        sites = []
        for name in all_names:
            sites.append(self.request.url + """list?id=""" + str(name.key.id()))
        
        template_values = {
            'all_names': all_names,
            'sites': sites,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin', Admin.AdminPage),
    ('/find', Admin.FindNames),
	('/add_name', Admin.AddName),
	('/assign', Admin.Assign),
	('/reset_assignments', Admin.ResetAssignments),
    ('/send_email', Admin.SendEmail),    
	('/send_email_person', Admin.SendEmailPerson),    
    ('/list', Lists.DisplayLists),  
    ('/fulfilled', Lists.Fulfilled),
    ('/edit_item', Lists.EditItem),
    ('/add_item', Lists.AddItem),
    ('/delete_item', Lists.DeleteItem),
    ('/generate_test_people', DebugTools.GenerateTestPeople),], debug=True)
