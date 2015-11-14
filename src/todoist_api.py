import requests
import sys
import subprocess
import json
from config import CLIENT_ID, CLIENT_SECRET, SCOPE, AUTH_URL, ADD_ITEM_URL, TOKEN_URL, SYNC_URL
from workflow import Workflow
import random, string

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-todoist-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-todoist-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

class Todoist():

  @classmethod
  def open_auth_page(cls):
    cls.start_auth_server()
    subprocess.call(['open', AUTH_URL])

  @classmethod
  def start_auth_server(cls):
    subprocess.Popen(['nohup','python','./server.py'])

  @classmethod
  def exchange_tokens(cls,code):
    response = requests.post(TOKEN_URL, {
      "client_id" : CLIENT_ID,
      "client_secret" : CLIENT_SECRET,
      "code" : code
      })
    return response.json()['access_token']

  @classmethod
  def save_access_token(cls, access_token):
    wf.save_password('todoist_access_token', access_token)

  @classmethod
  def get_access_token(cls):
    return wf.get_password('todoist_access_token')

  @classmethod
  def delete_access_token(cls):
    wf.delete_password('todoist_access_token')

  # change name to add_item
  @classmethod
  def add_to_list(cls, user_input):
    data = cls.create_request_body(user_input)
    return requests.post(SYNC_URL, data)

  @classmethod
  def create_request_body(cls, user_input):
    access_token = cls.get_access_token()
    commands = cls.create_commands(user_input)
    data = {
      "token" : access_token,
      "commands" : commands
    }
    return data

  @classmethod
  def create_commands(cls, user_input):
    user_input = user_input.split(';')
    commands = []
    content = user_input[0]
    options = None
    priority = 1
    project_id = None
    uuid = random_id(10)
    reminder = None

    try:
      options = user_input[1].strip()
    except:
      options = None

    if options:
      if 'work' in options.lower() or 'home' in options.lower():
        reminder = cls.create_reminder(options, uuid)
      elif isinstance(options, int):
        priority = int(options)
      else:
        project_id = cls.get_project_id(options)


    command = {}
    command['type'] = 'item_add'

    command['temp_id'] = uuid
    command['uuid'] = random_id(10)
    command['args'] = {}

    command['args']['priority'] = priority
    command['args']['content'] = user_input[0]
    if project_id:
      command['args']['project_id'] = project_id

    commands.append(command)
    if reminder:
      commands.append(reminder)


    return json.dumps(commands)

  @classmethod
  def create_reminder(cls, user_input, uuid):
    options = {}
    option = None

    try:
      results = user_input.split(' ')
      location = results[1]
      option = results[0]
    except:
      location = user_input

    loc_trigger = 'on_leave' if option == 'after' else 'on_enter'
    coordinates = wf.stored_data('todoist_%s' % location).split(',')

    options['type'] = 'reminder_add'
    options['temp_id'] = random_id(10)
    options['uuid'] = random_id(10)

    options['args'] = {}
    options['args']['type'] = 'location'
    options['args']['service'] = 'mobile'
    options['args']['item_id'] = uuid

    options['args']['name'] = location.title()
    options['args']['loc_lat'] = coordinates[0]
    options['args']['loc_long'] = coordinates[1]
    options['args']['loc_trigger'] = loc_trigger
    options['args']['radius'] = 800 # half a mile

    return options

  @classmethod
  def get_project_id(cls, project_name):
    project_id = None
    projects = wf.stored_data('todoist_projects')
    if not any(project['name'].lower() == project_name.lower() for project in projects):
        cls.sync()
    try:
      project = (item for item in projects if item["name"].lower() == project_name.lower()).next()
      project_id = project["id"]
    except:
      project_id = None

    return project_id


  @classmethod
  def sync(cls):
    access_token = cls.get_access_token()
    response = requests.post(SYNC_URL, {
      "token" : access_token,
      "seq_no" : 0,
      "resource_types": '["all"]'
    }).json();
    wf.store_data('todoist_locations', response['Locations'])
    wf.store_data('todoist_projects', response['Projects'])

    return True

  @classmethod
  def get_locations(cls):
    return wf.stored_data('todoist_locations')

  @classmethod
  def add_coordinates(cls, location, coordinates):
    wf.store_data('todoist_%s' % location, coordinates)

def random_id(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))