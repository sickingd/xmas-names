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


def emailPerson(person):    
    name = person.name
    email = person.email

    if name == "":
        return

    if email == "":
        return
        
    if not person.is_assigned:
        return

    subject_string = person.family + " Family Christmas Exchange"
    logging.info(subject_string)
    message = mail.EmailMessage(sender="sickingd@gmail.com", 
                                subject=subject_string)

    message.to = email
        
    message.body = """
Dear """ + name + """,

Here is the name you have picked for the """ + person.family + """ gift exchange:

    """ + person.assigned_name + """

Feel free to use your personal site to help provide and receive gift ideas:

    xmas-xchange.com/list?id=""" + str(person.key.id()) + """

The top section is for you to add items to your Christmas wish list.  The bottom section contains the wish list of the person you have selected.  If you end up purchasing an item from your selected person's wish list, please check the "fulfilled" box.  That will ensure someone else doesn't also purchase that same item. 
 
The people in charge have decided on a $50-$75 limit per person, so please try to stay in that range.

Let me know if you have any questions.  Merry Christmas!

Danny

p.s. This is an automated email, I don't know who you selected :-)
"""
    logging.info(message.body)
    message.send()
            
    
class SendEmailPerson(webapp2.RequestHandler):

    def post(self):
    
        people = ChristmasNames.Person.query(ChristmasNames.Person.name == self.request.get('email_person')).fetch(1000)
        for person in people:
            emailPerson(person)
            
        self.redirect("/admin")

        
class SendEmail(webapp2.RequestHandler):

    def post(self):
    
        people = ChristmasNames.Person.query(ChristmasNames.Person.family == self.request.get('email_family')).fetch(1000)
        
        for person in people:
            emailPerson(person)
            
        self.redirect("/admin")


class ResetAssignments(webapp2.RequestHandler):

    def post(self):
    
        all_names = ChristmasNames.Person.query().fetch(1000)
        for person in all_names:
            person.assigned_name_key = None
            person.assigned_name = ""
            person.is_assigned = False
            person.put()
            
        self.redirect("/admin")
        
        
def assignNames(familyName):

    count = 0
    familyPeople = ChristmasNames.Person.query(ChristmasNames.Person.family == familyName).fetch(1000)
    
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
            
            # Set up a set of excluded people for fast lookup later
            excludedPeople = set()
            for excludePerson in fromPerson.exclude:
                excludedPeople.add(excludePerson)
            
            # Allow the person to pick multiple names before giving up, this number could be made
            # a bit bigger because it's faster to pick a few more times here than it is to start over.
            toPersonTries = len(toPeople)
            toPersonCount = 0
            foundMatch = False
            while toPersonCount < toPersonTries:
                toPersonCount = toPersonCount + 1
                index = random.randint(0, len(toPeople) - 1)
                toPerson = toPeople[index]
                logging.info('%i:%i To Person %s - ID: %d', count, toPersonCount, toPerson.name, toPerson.key.id())

                # Not really sure why this is even a check, as I don't think it's possible
                if fromPerson.is_assigned:
                    logging.info('%i:%i Already assigned to %s', count, toPersonCount, fromPerson.assigned_name)
                    continue

                # Cannot pick yourself
                if fromPerson.key.id() == toPerson.key.id():
                    logging.info('%i:%i same person', count, toPersonCount)
                    continue

                # Exclude the exclusions
                if toPerson.name in excludedPeople:
                    logging.info('%i:%i Excluded person match', count, toPersonCount)
                    continue;

                foundMatch = True
                break;

            if not foundMatch:
                logging.info('%i: Did not find a match', count)
                continue;

            fromPerson.assigned_name_key = toPerson.key
            fromPerson.assigned_name = toPerson.name
            fromPerson.is_assigned = True
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
            
        
class AdminPage(webapp2.RequestHandler):

    def get(self):
        all_names = ChristmasNames.Person.query().fetch(1000)
        
        #Find out the website for each person, display that in the list
        sites = []
        for name in all_names:
            sites.append("""/list?id=""" + str(name.key.id()))
        
        template_values = {
            'all_names': all_names,
            'sites': sites,
        }

        template = JINJA_ENVIRONMENT.get_template('admin.html')
        self.response.write(template.render(template_values))        
	
   
class FindNames(webapp2.RequestHandler):

    def post(self):
        found_names = ChristmasNames.Person.query(ChristmasNames.Person.name == self.request.get('find_name')).fetch(20)
        all_names = ChristmasNames.Person.query().fetch(1000)            
        template_values = {
            'found_names': found_names,
            'find_a_name': True,
            'all_names': all_names,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))        

    def get(self):
        found_names = ChristmasNames.Person.query(ChristmasNames.Person.name == self.request.get('find_name')).fetch(20)
        all_names = ChristmasNames.Person.query().fetch(1000)            
        template_values = {
            'found_names': found_names,
            'find_a_name': True,
            'all_names': all_names,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))        
		
		
class AddName(webapp2.RequestHandler):

    def post(self):
        person = ChristmasNames.Person()
        person.email = self.request.get('email')
        person.name = self.request.get('name')
        person.family = self.request.get('family')
        logging.info(self.request.get('exclude'))
        person.exclude = [x.strip() for x in self.request.get('exclude').split(",")]
        logging.info(person.exclude)
        person.is_assigned = False        
        person.is_admin = False   
        person.put()
        
        self.redirect("/admin")


class Assign(webapp2.RequestHandler):

    def post(self):
        family_assign = self.request.get('family_assign')
        family_names = assignNames(family_assign)
        
        self.redirect("/admin")
    


