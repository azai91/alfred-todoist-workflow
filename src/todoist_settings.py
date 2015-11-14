"""
Displays settings
"""

from workflow import Workflow

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-todoist-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-todoist-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(_):

  user_input = wf.args[0]

  """
  Displays update feedback if update is available
  """
  if wf.update_available:
    wf.add_item(
      'An update is available!',
      autocomplete='workflow:update',
      valid=False)

  """
  Display option to add and remove account
  """
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


  """
  Allows user to input Home and Work coordinates.
  """
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
  """
  Validates that user inputted coordinates following format: float,float

  Args:
    coordinates: string, User inputted string to validate

  Returns:
    Boolean indicating whether or not the input string is properly formatted

  """

  if ';' in coordinates:
    coordinates = coordinates.split(';')
    long = coordinates[0]
    lat = coordinates[1] if len(coordinates[1]) else 0
  else:
    long = coordinates
    lat = 0

  try:
    float(long)
    float(lat)
    return True
  except:
    return False

if __name__ == '__main__':
  wf.run(main)