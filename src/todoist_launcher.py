import sys
from workflow import Workflow
from todoist_api import Todoist

def main(wf):
  options = wf.args[0]

  if options == 'login':
    Todoist.open_auth_page()
  elif options == 'logout':
    Todoist.delete_access_token()
    sys.stdout.write('Account Removed')
  elif options == 'sync':
    Todoist.sync()
    sys.stdout.write('Account Synced')
  elif options.startswith('home'):
    Todoist.add_coordinates('home',options[4:])
    sys.stdout.write('Home Coordinates Saved')
  elif options.startswith('work'):
    Todoist.add_coordinates('home',options[4:])
    sys.stdout.write('Home Coordinates Saved')

  return 0

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
