import requests
from config import CLIENT_ID, CLIENT_SECRET, SCOPE
from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER

wf=Workflow()

auth_url='https://todoist.com/oauth/authorize?client_id=%s&scope=%s&state=%s' % (CLIENT_ID, SCOPE, 'Alfred')

class Todoist():

  @classmethod
  def get_auth_url(cls):
    return auth_url

  @classmethod
  def verify_credentials(cls):
    pass

  @classmethod
  def exchange_tokens(cls,code):
    response = requests.post('https://todoist.com/oauth/access_token', {
      "client_id" : CLIENT_ID,
      "client_secret" : CLIENT_SECRET,
      "code" : code
      })
    return response.json()['access_token']

  @classmethod
  def save_access_token(cls, access_token):
    wf.save_password('todoist_access_token',access_token)

  @classmethod
  def get_access_token(cls):
    return wf.get_password('todoist_access_token')

  @classmethod
  def delete_access_token(cls):
    wf.delete_password('todoist_access_token')

  @classmethod
  def add_to_list(cls,user_input):
    data = cls.create_request_body(user_input)
    requests.post('https://todoist.com/API/v6/add_item',data)
    return 0

  @classmethod
  def create_request_body(user_input):
    user_input = user_input.split(';')
    content=user_input
    priority=None

    try:
      priority=user_input[1]
    except:
      prority=1

    access_token = cls.get_access_token()
    data = {
      "token" : access_token,
      "content" : content,
      "priority" : priority
    }
    return data

  @classmethod
  def refresh(cls):
    pass
