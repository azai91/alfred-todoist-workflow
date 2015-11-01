import requests
import sys
import subprocess
from config import CLIENT_ID, CLIENT_SECRET, SCOPE, AUTH_URL, ADD_ITEM_URL, TOKEN_URL
from workflow import Workflow

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
    data = cls.create_request_body(user_input)
    return requests.post(ADD_ITEM_URL, data)

  @classmethod
  def create_request_body(cls,user_input):
    user_input = user_input.split(';')
    content = user_input[0]
    priority = None

    try:
      priority = user_input[1]
    except:
      prority = 1

    access_token = cls.get_access_token()
    data = {
      "token" : access_token,
      "content" : content,
      "priority" : priority
    }
    return data
