import os
import urllib

from google.appengine.api import mail

import jinja2
import webapp2
import logging
import json

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
            person = ChristmasNames.Person.get_by_id(int(self.request.get('id')))
            people = ChristmasNames.Person.query(ChristmasNames.Person.name == person.name).fetch(1000)
            for next_person in people:
                if next_person.assigned_name_key is not None:
                    assigned_people.append(next_person.assigned_name_key.get())
            found = True
        template_values = {
            'person': person,
            'assigned_people': assigned_people,
            'found_person': found,
        }

        #Experimenting with this as a better way to send server information to javascript.
        #Supposedly this can just be read directly using $.getJSON()
        #self.request.write(json.dumps({'person_id': person_id}))
        

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
        
class Fulfilled(webapp2.RequestHandler):

    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        fulfilled = data['fulfilled']
        description = data['description']
        assigned_person_name = data['assigned_person_name']
        assigned_people = ChristmasNames.Person.query(ChristmasNames.Person.name == assigned_person_name).fetch(1000)
        logging.info("""Fulfilled: Assigned person name is """ + assigned_person_name + """ and the number of people found are: """ + str(len(assigned_people)))
        for person in assigned_people:
            logging.info("""Fulfilled: Number of items: """ + str(len(person.items)))
            for item in person.items:
                logging.info("""Fulfilled: Checking to see if """ + item.description + """=""" + description)
                if item.description == description:
                    item.is_fulfilled = (fulfilled == "True")
                    logging.info("""Fulfilled: They match!""")
                    logging.info("""Person """ + person.name + """ is changing description """ + description + """ to """ + fulfilled)
                else:
                    logging.info("""Fulfilled: They did NOT match""")
                    
            person.put()
            
            
class EditItem(webapp2.RequestHandler):

    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        old_description = data['old_description']
        new_description = data['new_description']
        new_link = data['new_link']
        person_name = data['person_name']
        people = ChristmasNames.Person.query(ChristmasNames.Person.name == person_name).fetch(1000)
        for person in people:
            for item in person.items:
                if item.description == old_description:
                    item.description = new_description
                    item.link = new_link
                    logging.info("""Person """ + person.name + """ is changing """ + old_description + """ to """ + new_description + """ : """ + new_link)
            person.put()       

class AddItem(webapp2.RequestHandler):

    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        new_description = data['new_description']
        new_link = data['new_link']
        person_name = data['person_name']
        people = ChristmasNames.Person.query(ChristmasNames.Person.name == person_name).fetch(1000)
        new_item = ChristmasNames.Item(description = new_description, link = new_link)
        person_id = ""
        for person in people:
            person_id = str(person.key.id());
            person.items.append(new_item)
            logging.info("""Person """ + person.name + """ is adding """ + new_description + """ : """ + new_link)
            person.put()              
        

class DeleteItem(webapp2.RequestHandler):

    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        description = data['description']
        person_name = data['person_name']
        people = ChristmasNames.Person.query(ChristmasNames.Person.name == person_name).fetch(1000)
        for person in people:
            #This is called "list comprehension" and is a technique to remove all occurrences of an element in a list.
            #Another way to do it is to call ".remove(index)" but that only removes the single occurrence.
            person.items = [x for x in person.items if x.description != description]
            logging.info("""Person """ + person.name + """ is removing """ + description)
            person.put()                 
    

        
