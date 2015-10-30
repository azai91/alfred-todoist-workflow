import subprocess
import sys
from workflow import Workflow

def main(wf):
  url = wf.args[0]
  start_server()
  wf.logger.error(url)
  subprocess.call(['open',url])

def start_server():
    subprocess.Popen(['nohup','python','./server.py'])

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
