from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
import requests

UPDATE_SETTINGS = {'github_slug' : 'azai91/alfred-drive-workflow'}
HELP_URL = 'https://github.com/azai91/alfred-drive-workflow/issues'

wf = Workflow(update_settings=UPDATE_SETTINGS, help_url=HELP_URL)

def main(_):
  user_input = wf.args[0]

  if wf.update_available:
    wf.add_item(
      'An update is available!',
      autocomplete='workflow:update',
      valid=False
    )

  if user_input in "Add Account":
    wf.add_item(title="Add Account",
      arg="login",
      autocomplete='Add Account',
      valid=True)
  if user_input in "Remove Account":
    wf.add_item(title="Remove Account",
      arg="logout",
      autocomplete="Remove Account",
      valid=True)

  wf.send_feedback()
  return 0


if __name__ == '__main__':
  wf.run(main)