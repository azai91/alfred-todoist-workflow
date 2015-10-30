import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from todoist_api import Todoist
import urlparse

class HandlerClass(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(s):
    try:
      ##TODO, compare state, better parser to  check params
      code = urlparse.urlparse(s.path)[4].split('=')[2]
      access_token = Todoist.exchange_tokens(code)
      Todoist.save_access_token(access_token)
      s.wfile.write('Your code has been saved in Alfred')
    except:
      s.wfile.write('Error with setting code')

ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

server_address = ('127.0.0.1', 1337)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)
httpd.timeout = 20
httpd.handle_request()
