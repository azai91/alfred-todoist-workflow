import subprocess
import sys
from workflow import Workflow
from todoist_api import Todoist

def main(wf):
  user_input = wf.args[0].split(';')
  content=user_input[0]
  priority=None

  try:
    priority=user_input[1]
  except:
    prority=1

  if content[:5] in 'login':
    start_server()
    content = str(content)[5:]
    subprocess.call(['open',content])
  elif content[:6] in 'logout':
    Todoist.delete_access_token()

  return 0

def start_server():
    subprocess.Popen(['nohup','python','./server.py'])

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
