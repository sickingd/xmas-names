import os
import urllib

from google.appengine.api import mail

import jinja2
import webapp2
import logging

import ChristmasNames


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


    
class DisplayLists(webapp2.RequestHandler):

    def get(self):
        id = self.request.get('id')
        found = False
        assigned_people = []
        if not id == "":
            person_id = ChristmasNames.Person.get_by_id(int(self.request.get('id')))
            people = ChristmasNames.Person.query(ChristmasNames.Person.name == person_id.name).fetch(1000)
            for person in people:
                if person.assigned_name_key is not None:
                    assigned_people.append(person.assigned_name_key.get())
            found = True
        template_values = {
            'person': person_id,
            'assigned_people': assigned_people,
            'found_person': found,
        }

        template = JINJA_ENVIRONMENT.get_template('list.html')
        self.response.write(template.render(template_values)) 

    def post(self):
        id = self.request.get('id')
        found = False
        assigned_people = []
        if not id == "":
            person_id = ChristmasNames.Person.get_by_id(int(self.request.get('id')))
            people = ChristmasNames.Person.query(ChristmasNames.Person.name == person_id.name).fetch(1000)
            for person in people:
                person.list = self.request.get('person_list')
                person.list_updated = True
                person.put()
                assigned_people.append(person.assigned_name_key.get())
            
            found = True
        template_values = {
            'person': person_id,
            'assigned_people': assigned_people,
            'found_person': found,
        }

        template = JINJA_ENVIRONMENT.get_template('list.html')
        self.response.write(template.render(template_values))          

    
def emailPerson(person):    
        
    message = mail.EmailMessage(sender="sickingd@gmail.com", subject="Christmas Lists")
    message.to = person.email
        
    message.body = """
Dear """ + person.name + """,

To help communicate your Christmas wish list to the person who chose your name, you can use the following link.

www.sickingd-xmas-2014.appspot.com/list?id=""" + str(person.key.id()) + """

The top section is where you write in any items that you want for Christmas.  The bottom section contains the list of the people you have selected.

Please let me know if it's not working as expected.  

Danny

"""

    #Debugging hack
    #if person.name == 'Danny Sicking':
    message.send()
        
    return message.body

    
class SendListEmails(webapp2.RequestHandler):

    def post(self):
    
        all_names = ChristmasNames.Person.query().fetch(1000)
        emailed = set()
        emails_sent = False
        all_messages = ''
        for person in all_names:
            if person.is_assigned and person.name not in emailed:
                all_messages = all_messages + emailPerson(person)
                emailed.add(person.name)
                emails_sent = True

        all_names = ChristmasNames.Person.query().fetch(1000)            

        template_values = {
            'list_emails_sent': emails_sent,
            'all_list_email_messages': all_messages,
            'all_names': all_names,
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))           
        


        
