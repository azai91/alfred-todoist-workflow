"""
Displays the options for adding and removing an account
"""

from workflow import Workflow

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-todoist-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-todoist-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(_):

  user_input = wf.args[0]

  # Displays update feedback if update is available
  if wf.update_available:
    wf.add_item(
      'An update is available!',
      autocomplete='workflow:update',
      valid=False)

  if user_input.lower() in "Add Account".lower():
    wf.add_item(title="Add Account",
      arg="login",
      autocomplete='Add Account',
      valid=True)

  if user_input.lower() in "Remove Account".lower():
    wf.add_item(title="Remove Account",
      arg="logout",
      autocomplete="Remove Account",
      valid=True)

  if user_input.lower() in "Sync Account".lower():
    wf.add_item(title="Sync Account",
      arg="sync",
      autocomplete="Sync Account",
      valid=True)

  if user_input.lower() in "Set Home Location ".lower():
    wf.add_item(title="Set Home Location [long,lat]",
      autocomplete="Set Home Location ")
  elif user_input.lower().startswith("Set Home Location ".lower()):
    coordinates = user_input[18:].replace(" ","")
    if validate_coordinates(coordinates):
      wf.add_item(title="Set Home Location %s" % user_input[18:],
        arg="home%s" % coordinates,
        valid=True)
    else:
      wf.add_item(title="Invalid Coordinates Format")

  if user_input.lower() in "Set Work Location ".lower():
    wf.add_item(title="Set Work Location [long,lat]",
      autocomplete="Set Work Location ")
  elif user_input.lower().startswith("Set Work Location ".lower()):
    coordinates = user_input[18:].replace(" ","")
    if validate_coordinates(coordinates):
      wf.add_item(title="Set Work Location %s" % user_input[18:],
        arg="work%s" % coordinates,
        valid=True)
    else:
      wf.add_item(title="Invalid Coordinates Format")

  wf.send_feedback()
  return 0

def validate_coordinates(coordinates):
  long = None
  lat = None
  if ';' in coordinates:
    coordinates = coordinates.split(';')
    [long,lat] = coordinates
  else:
    long = coordinates
    lat = 0

  return isinstance(long, int) and isinstance(lat, int)

if __name__ == '__main__':
  wf.run(main)