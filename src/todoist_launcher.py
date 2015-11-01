import sys
from workflow import Workflow
from todoist_api import Todoist

def main(wf):
  options = wf.args[0]

  if options[:5] in 'login':
    Todoist.open_auth_page()
  elif options[:6] in 'logout':
    Todoist.delete_access_token()

  return 0

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
