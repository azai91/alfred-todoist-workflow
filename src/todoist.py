from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
import requests
from config import API_KEY

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(_):
  user_input = wf.args[0].split(';')
  content=user_input[0]
  priority=None

  try:
    priority=user_input[1]
  except:
    prority=1

  if wf.update_available:
    wf.add_item(
      'An update is available!',
      autocomplete='workflow:update',
      valid=False
    )

  data = {
    "token" : API_KEY,
    "content" : user_input,
    "priority" : priority
  }

  try:
    requests.post('https://todoist.com/API/v6/add_item',data)
  except:
    pass

  return 0

if __name__ == '__main__':
  wf.run(main)