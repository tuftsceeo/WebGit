# (1) Open a Python Server
# (2) Receive Commands (e.g. Command Line Interface UNIX commands)
# (3) Execute Commands and Return Result
#
# - NOTE: this application is a HUGE security risk, so only run if know what you are doing!
#         it takes in ANY commands sent to it and blindly executes them
#
# Acknowledgements:
# - Server modified from: https://pythonbasics.org/webserver/
# - Execute commands modified from: https://janakiev.com/blog/python-shell-commands/
# - URL Decoding modified from: https://www.urldecoder.io/python/

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib.parse

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
	# this replies back to the HTTP request by writing data
	def send_data(self, data, headers=True):
		self.send_response(200)
		if (headers):
			self.send_header("Content-type", "text/html")
			self.end_headers()
		self.wfile.write(bytes(data, "utf-8"))
		# end send_data
	
	# this processes the HTTP request
	def do_GET(self):
		path = self.path
		print('- Process Request, path is:', path)
		if (path == '/' or path == '/index.html'):
			# open index.html and server it up
			print('- SERVER: opening and sending "index.html"')
			f = open("index.html")
			self.send_data(f.read()) # send content
			f.close()
		else:
			# check if sending in a command
			command = None # start as None and update if find command

			# parse looking for command
			command_string = '?command='
			location = path.find(command_string)
			if (location >= 0):
				# found command
				command = path[location + len(command_string):] # get everything AFTER command_string
				# decode
				command = urllib.parse.unquote(command)

			# process command (if exists)
			if (command == None):
				# no command detected; send blank
				self.send_data('')
			else:
				print('- SERVER: executing command', command)
				stream = os.popen(command)
				self.send_data(stream.read())
		# end do_GET

if __name__ == "__main__":
	# start the server
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))
	print("- Control-C to stop Server")

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	# end the server
	webServer.server_close()
	print("Server stopped.")