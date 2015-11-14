from workflow import Workflow

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-todoist-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-todoist-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(_):
  user_input = wf.args[0]

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
  if user_input.lower() in "Set Home Location".lower():
    wf.add_item(title="Set Home Location [long,lat]",
      autocomplete="Set Home Location")
  if user_input.lower().startswith("Set Home Location ".lower()):
    # insert long lat checker
    wf.add_item(title="Set Home Location %s" % user_input[18:],
      arg="home %s" % user_input[18:].replace(" ",""),
      valid=True)
  if user_input.lower() in "Set Work Location".lower():
    wf.add_item(title="Set Work Location [long,lat]",
      autocomplete="Set Work Location")
  if user_input.lower().startswith("Set Work Location ".lower()):
    # insert long lat checker
    wf.add_item(title="Set Work Location %s" % user_input[18:],
      arg="home %s" % user_input[18:].replace(" ",""),
      valid=True)

  wf.send_feedback()
  return 0
33.979758, -118.422545

if __name__ == '__main__':
  wf.run(main)