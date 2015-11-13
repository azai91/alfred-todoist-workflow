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

  @classmethod
  def add_to_list(cls,user_input):
    data = cls.create_request_body("item_add", user_input)
    return requests.post(SYNC_URL, data)

  @classmethod
  def create_request_body(cls, command, user_input):
    access_token = cls.get_access_token()
    commands = cls.create_commands(command, user_input)
    data = {
      "token" : access_token,
      "commands" : commands
    }
    return data

  @classmethod
  def create_commands(cls, command, user_input):
    user_input = user_input.split(';')
    content = user_input[0]
    options = None
    priority = 1
    project_id = None
    projects = wf.stored_data('todoist_projects')

    try:
      options = user_input[1]
    except:
      options = None

    # assigns priority or project
    if options:
      if isinstance(options, int):
        priority = int(options)
      elif any(project['name'].lower() == options.lower() for project in projects):
        project = (item for item in projects if item["name"].lower() == options.lower()).next()
        project_id = project["id"]

    commands = {}
    commands['type'] = command

    commands['temp_id'] = random_id(10)
    commands['uuid'] = random_id(10)
    commands['args'] = {}
    commands['args']['priority'] = priority
    commands['args']['content'] = user_input[0]
    if project_id:
      commands['args']['project_id'] = project_id

    return json.dumps([commands])

  @classmethod
  def sync(cls):
    access_token = cls.get_access_token()
    response = requests.post(SYNC_URL, {
      "token" : access_token,
      "seq_no" : 0,
      "resource_types": '["all"]'
    }).json()['Projects'];

    wf.store_data('todoist_projects', response)


def random_id(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))