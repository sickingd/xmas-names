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

import ChristmasLists
import DebugTools


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
    exclude = ndb.StringProperty()
    assigned_name_key = ndb.KeyProperty()
    assigned_name = ndb.StringProperty()
    list = ndb.TextProperty()    
    list_updated = ndb.BooleanProperty()
    is_admin = ndb.BooleanProperty()
    items = ndb.StructuredProperty(Item, repeated=True)

def emailPerson(person):    
    name = person.name
    email = person.email

    if name == "":
        return

    if email == "":
        return
        
    if not person.is_assigned:
        return

    message = mail.EmailMessage(sender="sickingd@gmail.com",
                                subject="Christmas Names 2014")

    message.to = email
        
    message.body = """
Dear """ + name + """,

Here is the name you have picked for the """ + person.family + """ gift exchange:

""" + person.assigned_name + """

The people in charge have decided on a $50 limit per person, so please try to stay in that range.

Let me know if you have any questions.  Merry Christmas!

Danny

"""
    
    message.send()
            
    
class SendEmailPerson(webapp2.RequestHandler):

    def post(self):
    
        people = Person.query(Person.name == self.request.get('email_person')).fetch(1000)
        for person in people:
            emailPerson(person)
           
        all_names = Person.query().fetch(1000)

        template_values = {
            'emails_person_sent': True,
            'all_names': all_names,
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))    
        
class SendEmail(webapp2.RequestHandler):

    def post(self):
    
        people = Person.query(Person.family == self.request.get('email_family')).fetch(1000)
        
        for person in people:
            emailPerson(person)
            
        all_names = Person.query().fetch(1000)

        template_values = {
            'emails_sent': True,
            'all_names': all_names,
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))    


def assignNames(familyName):

    count = 0
    familyPeople = Person.query(Person.family == familyName).fetch(1000)
    
    # Reset the flag
    for person in familyPeople:
        person.is_assigned = False
        person.put()
                
    maxTries = len(familyPeople) * len(familyPeople) * len(familyPeople)
    logging.info('Max tries is %i', maxTries)
    
    #maxTries = 10000
    while True:
        fromPeople = copy.deepcopy(familyPeople)
        toPeople = copy.deepcopy(familyPeople)

        for fromPerson in fromPeople:
            logging.info('%i: From Person %s - ID: %d', count, fromPerson.name, fromPerson.key.id())
            
            index = random.randint(0, len(toPeople) - 1)
            toPerson = toPeople[index]
            logging.info('%i: To Person %s - ID: %d', count, toPerson.name, toPerson.key.id())

            if fromPerson.is_assigned:
                logging.info('%i: Already assigned to %s', count, fromPerson.assigned_name)
                continue

            # Cannot pick yourself
            if fromPerson.key.id() == toPerson.key.id():
                logging.info('%i: same person', count)
                continue

            # Exclude the exclusions
            #TODO 
            if fromPerson.exclude == toPerson.name:
                logging.info('%i: Excluded person is %s, same as %s', count, fromPerson.exclude, toPerson.name)
                continue
            logging.info('%i: Excluded person is %s, not %s', count, fromPerson.exclude, toPerson.name)

            fromPerson.assigned_name_key = toPerson.key
            fromPerson.assigned_name = toPerson.name
            fromPerson.is_assigned = True
            #TODO: Store IDS instead of names for assigned_name
            logging.info('%i: %s selected %s', count, fromPerson.name, toPerson.name)
            del toPeople[index]
                    
        if len(toPeople) is 0:
            for fromPerson in fromPeople:
                fromPerson.put()
            return fromPeople
            
        # Try to enforce some limit on number of tries
        count = count + 1
        if count > maxTries:
            return []
            
        
    
    
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
	
   
class FindNames(webapp2.RequestHandler):

    def post(self):
        found_names = Person.query(Person.name == self.request.get('find_name')).fetch(20)
        all_names = Person.query().fetch(1000)            
        template_values = {
            'found_names': found_names,
            'find_a_name': True,
            'all_names': all_names,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))        

    def get(self):
        found_names = Person.query(Person.name == self.request.get('find_name')).fetch(20)
        all_names = Person.query().fetch(1000)            
        template_values = {
            'found_names': found_names,
            'find_a_name': True,
            'all_names': all_names,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))        
		
		
class AddName(webapp2.RequestHandler):

    def post(self):
        person = Person()
        person.email = self.request.get('email')
        person.name = self.request.get('name')
        person.family = self.request.get('family')
        person.exclude = self.request.get('single_exclude')
        person.is_assigned = False        
        person.is_admin = False   
        person.put()

        all_names = Person.query().fetch(1000)            
        template_values = {
            'added_name': person.name,
            'name_added': True,
            'all_names': all_names,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))



class Assign(webapp2.RequestHandler):

    def post(self):
        family_assign = self.request.get('family_assign')
        family_names = assignNames(family_assign)
        all_names = Person.query().fetch(1000)            

        template_values = {
            'family_names': family_names,
            'assigned_names': True,
            'family_assign': family_assign,
            'all_names': all_names,
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))       


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/find', FindNames),
	('/add_name', AddName),
	('/assign', Assign),
	('/send_email', SendEmail),    
	('/send_email_person', SendEmailPerson),    
	('/send_list_emails', ChristmasLists.SendListEmails),    
    ('/list', ChristmasLists.DisplayLists),
    ('/generate_test_people', DebugTools.GenerateTestPeople),
    ('/fulfilled', ChristmasLists.Fulfilled),
], debug=True)
