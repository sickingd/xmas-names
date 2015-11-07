import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2
import random


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


def sendMail(names):

    name = ""
    email = ""
    for person in names:
        name = person.name
        email = person.email

    if name == "":
        return "Sorry no matches"

    if email == "":
        return "Sorry no email for " + name 
    
    message = mail.EmailMessage(sender="sickingd@gmail.com",
                                subject="Christmas Names 2014")

    message.to = email
        
    message.body = """
Dear """ + name + """,

Here are the name(s) you have picked for Christmas this year:
"""
    for person in names:
        message.body = message.body + person.toName + " for the " + person.familyName + " Christmas gift exchange.\n"
    
    message.body = message.body + """
The people in charge have decided on a $50 limit per person, so please try to stay in that range.

Let me know if you have any questions.  Can't wait to see everyone at Christmas!

Danny

p.s. This is an autogenerated email and the names were randomly selected.  I don't know what names you have. :-)

"""
    
    message.send()
    return message.body
    

class Person(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    name = ndb.StringProperty()
    email = ndb.StringProperty(indexed=False)
    familyName = ndb.StringProperty(indexed=False)
    toName = ndb.StringProperty(indexed=False)

class PersonCreator:
    def __init__(self, name):
        self.name = name
        

def createPerson(name, exclude, email):
    person = PersonCreator(name)
    person.email = ""
    person.exclude = exclude
    person.toPerson = ""
    return person


def createNames(familyName):

    people = []

    people.append(createPerson("Kaitie", "Danny", "ksicking@gmail.com"))
    people.append(createPerson("Danny", "Kaitie", "sickingd@yahoo.com"))
    people.append(createPerson("Matt", "Morgan", "mtooley2006@gmail.com"))
    
    jenna = createPerson("Jenna", "Derek", "jennatooley@gmail.com")
    if familyName is "Tooleys":
        jenna.toPerson = "Kristen"
    people.append(jenna)

    people.append(createPerson("MikeT", "Laura", "mtooleyh2o@gmail.com"))
    people.append(createPerson("Laura", "MikeT", "lauratooley@gmail.com"))
    
    if familyName is "Svehlas":
        people.append(createPerson("MikeS", "Cheryl", "msvehla@fairfield.ca.gov"))
        people.append(createPerson("Cheryl", "MikeS", "cheryls3131@yahoo.com"))
        people.append(createPerson("Don", "Elaine", "svehla.don@gmail.com"))
        people.append(createPerson("Elaine", "Don", "elainesvehla@gmail.com"))
        people.append(createPerson("Morgan", "Matt", "sportygirl32692@sbcglobal.net"))
        people.append(createPerson("Derek", "Jenna", "dbrangha@gmail.com"))

    if familyName is "Tooleys":
        people.append(createPerson("Jill", "Rob", "jill.youngberg@comcast.net"))
        people.append(createPerson("Rob", "Jill", "rob_youngberg@hotmail.com"))
        people.append(createPerson("Alex", "", "alex.youngberg@comcast.net"))
        people.append(createPerson("Kristen", "", "kristen.youngberg@comcast.net"))
        people.append(createPerson("Grammie", "Papa", "jandbtooley@comcast.net"))
        people.append(createPerson("Papa", "Grammie", "jandbtooley@comcast.net"))
        
    return people

def getNames(fromPeople, familyName):
    toPeople = []
    for fromPerson in fromPeople:
        if fromPerson.name is not "Kristen":
            toPeople.append(fromPerson.name)

    return toPeople

def getAllNames():
    return ["Kaitie", "Danny", "Matt", "Morgan", "Jenna", "Derek", "MikeT", "Laura", "MikeS", "Cheryl", "Don", "Elaine", "Jill", "Rob", "Alex", "Kristen", "Grammie", "Papa"]


def assignNames(familyName):

    while True:
        fromPeople = createNames(familyName)
        toPeople = getNames(fromPeople, familyName)

        for fromPerson in fromPeople:
            
            index = random.randint(0, len(toPeople) - 1)
            toPerson = toPeople[index]

            # Already has a selection
            if fromPerson.toPerson is not "":
                continue

            # Cannot pick yourself
            if fromPerson.name is toPerson:
                continue

            # Exclude the exclusions
            if fromPerson.exclude is toPerson:
                continue

            if fromPerson.name is "Don" or fromPerson.name is "Elaine":
                if toPerson is "Derek" or toPerson is "Morgan":
                    continue
            
            fromPerson.toPerson = toPerson
            del toPeople[index]
                    
        if len(toPeople) is 0:
            return fromPeople
        

def storeNames(names, familyName):
    for name in names:
        person = Person()
        person.email = name.email
        person.name = name.name
        person.familyName = familyName
        person.toName = name.toPerson
        person.put()
    
    
    
class MainPage(webapp2.RequestHandler):

    def get(self):
        
        template_values = {}

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class FindNames(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        find_name = self.request.get('find_name')

        found_names = []
        email_body = ""

        if False:        
            if find_name == "Regenerate":
                ndb.delete_multi(Person.query().fetch(keys_only=True))
                svehlas = assignNames("Svehlas")
                storeNames(svehlas, "Svehlas")
                tooleys = assignNames("Tooleys")
                storeNames(tooleys, "Tooleys")
            elif find_name == "Delete":
                ndb.delete_multi(Person.query().fetch(keys_only=True))
            elif find_name == "Email":
                all_names = getAllNames()
                for name in all_names:
                    found_names = Person.query(Person.name == name)
                    #email_body = email_body + sendMail(found_names)
        else:
            found_names = Person.query(Person.name == find_name)
            #email_body = sendMail(found_names)

        
        template_values = {
            'found_names': found_names,
            'find_a_name': True,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))        

class AddName(webapp2.RequestHandler):

    def post(self):

		
class ListNames(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        found_names = []
        email_body = ""

		all_names = getAllNames()
		for name in all_names:
			found_names = Person.query(Person.name == name)
			#email_body = email_body + sendMail(found_names)

        
        template_values = {
            'found_names': found_names,
            'find_a_name': True,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))       


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/find', FindNames),
	('/add_name', AddName),
	('/list_names', ListNames),
], debug=True)
