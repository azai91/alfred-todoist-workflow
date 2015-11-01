CLIENT_ID = '959e19a2843c4afa9086c76659dd17f4'
CLIENT_SECRET = '2c16535ef1d44511b383ed2fd2caad59'
SCOPE = 'task:add'

AUTH_URL = 'https://todoist.com/oauth/authorize?client_id=%s&scope=%s&state=%s' % (CLIENT_ID, SCOPE, 'Alfred')
ADD_ITEM_URL = 'https://todoist.com/API/v6/add_item'
TOKEN_URL = 'https://todoist.com/oauth/access_token'