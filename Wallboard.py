# UK ITCC Wallboard
# Author: Carter Fifield
# Date: 5/17/17

from http.server import BaseHTTPRequestHandler, HTTPServer
from bs4 import BeautifulSoup
from os import curdir, sep
import requests


# HTTPRequestHandler class
class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

	# GET
	def do_GET(self):

		try:
			#Check the file extension required and
			#set the right mime type
			mimetype = ''

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if self.path.endswith(".ico"):
				mimetype='image/x-icon'
				sendReply = True

			if sendReply == True and mimetype is not 'text/html':
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type', mimetype)
				self.end_headers()
				self.wfile.write(bytes(f.read(), "utf-8"))
				f.close()

			else:
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(bytes(generatePage(), "utf-8"))
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

# Pulls in data from the ITCC Wallboard and returns a string containg all the data
def getWallboardData():
	# Get Wallboard Page
	page = requests.get('http://172.17.241.221/ContactCenterDirector/device.aspx?device=ITCC_01')

	# Parse request data into text
	data = page.text

	# Pull in data using lxml
	soup = BeautifulSoup(data, "lxml")

	# Intialize output
	output = ""

	# Pull in data for all available call queues
	queues = soup.find("div", {"id": "DYN001"})

	# For each queue
	for table in queues.find_all('tr'):

		# Get the name of the queue
	    output += table.get_text()
	    # Add delimiter
	    output += '?t?r?'

	    # For each sub status of the queue (Logged in agents, etc...)
	    for item in table.find_all('td'):
	    	# Get value
		    output += item.get_text()
		    # Add delimiter
		    output += '?t?d?'

	# Add delimiter to split queues and agents later
	output += '[Split]'

	# Pull in data for all available agents
	agents = soup.find("div", {"id": "DYN002"})

	# For each Agent
	for table in agents.find_all('tr'):
		# Get the name of the agent
	    output += table.get_text()
	    # Add delimiter
	    output += '?t?r?'

	    # For each sub status of the agent (Agent State, etc...)
	    for item in table.find_all('td'):
		    output += item.get_text()
		    # Add delimiter
		    output += '?t?d?'

	return output

# Generates the HTML code to push to the web clients, returns a string
def generatePage():
	# Get the Wallboard data
	wallboardData = getWallboardData()

	# Grab only the queue data from the wallboard data
	queueData = wallboardData.split('[Split]')[0]
	queues = queueData.split('?t?r?')

	# Grab only the agent data from the wallboard data
	agentData = wallboardData.split('[Split]')[1]
	agents = agentData.split('?t?r?')

	# Intialize output
	pageHTML = ""

	#Define Page Template
	# Header
	pageHTML += '<!DOCTYPE html>'
	pageHTML += '<html lang="en">'
	pageHTML += '<head>'
	pageHTML += '<title>ITCC Wallboard</title>'
	pageHTML += '<meta charset="utf-8">'
	pageHTML += '<meta name="viewport" content="width=device-width, initial-scale=1">'

	# Bootstrap
	pageHTML += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">'
	pageHTML += '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>'
	pageHTML += '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>'

	# Custom Styles
	pageHTML += '<link rel="stylesheet" type="text/css" href="WallboardStyle.css">'

	# Body
	pageHTML += '<body>'
	pageHTML += '<div class="container-fluid container-full">'

	# Wallboard Header
	pageHTML += '<div class="row">'
	pageHTML += '<div class="col-sm-12 column">'
	pageHTML += '<div class="wallboardTitle">ITCC Wallboard</div>'
	pageHTML += '</div>'
	pageHTML += '</div>'


	# Queue Table
	pageHTML += '<div class="row">'
	pageHTML += '<div class="col-sm-12 column">'
	pageHTML +=	'<table class="table table-curved">'

	# Table Headers
	pageHTML += '<thead>'
	pageHTML += '<tr>'
	pageHTML += '<th>Queue</th>'
	pageHTML += '<th>Logged In</th>'
	pageHTML += '<th>Talking</th>'
	pageHTML += '<th>Waiting Calls</th>'
	pageHTML += '<th>Abandoned %</th>'
	pageHTML += '</tr>'
	pageHTML += '</thead>'

	# Table Body
	pageHTML += '<tbody>'

	# Setup Queues
	# For each queue
	for i in range(3, 7):
		pageHTML += '<tr>'

		# For each sub item
		for j in range(0, 5):
			if j == 1:
				pageHTML += '<td class="logged">'
			elif j == 2:
				pageHTML += '<td class="talk">'
			elif j == 3:
				pageHTML += '<td class="wait">'
			elif j == 4:
				pageHTML += '<td class="abd">'
			else:
				pageHTML += '<td>'
			# Parse sub item from queue data
			pageHTML += queues[i].split('?t?d?')[j]
			pageHTML += '</td>'
		
		pageHTML += '</tr>'


	pageHTML += '</tbody>'
	pageHTML += '</table>'
	pageHTML += '</div>'
	pageHTML += '</div>'


	###################################################################
	###################################################################
	###################################################################

	# Agent Table
	pageHTML += '<div class="row">'
	pageHTML += '<div class="col-sm-12 column">'
	pageHTML += '<div class="wallboardTitle">ITCC Agent Status</div>'
	pageHTML +=	'<table class="table table-curved">'

	# Table Headers
	pageHTML += '<thead>'
	pageHTML += '<tr>'
	pageHTML += '<th>Agent</th>'
	pageHTML += '<th>State</th>'
	pageHTML += '<th>Reason</th>'
	pageHTML += '<th>Time In State</th>'
	pageHTML += '</tr>'
	pageHTML += '</thead>'
	pageHTML += '<tbody>'

	# Setup Agents
	# For each agent
	for i in range(3, len(agents)):
		pageHTML += '<tr>'

		# For each sub item
		for j in range(0, 4):
			if j == 1:
				pageHTML += '<td class="as">'
			elif j == 2:
				pageHTML += '<td class="rd">'
			elif j == 3:
				pageHTML += '<td class="tis">'
			else:
				pageHTML += '<td>'
			
			# Parse sub item from agent data
			pageHTML += agents[i].split('?t?d?')[j]
			pageHTML += '</td>'
		
		pageHTML += '</tr>'


	pageHTML += '</tbody>'
	pageHTML += '</table>'
	pageHTML += '<div class="row">'
	pageHTML += '<div class="col-lg-12">'

	# Close Container & Body
	pageHTML += '</div>'
	pageHTML += '</body>'
	pageHTML += '</html>'

	# Reload only HTML every 5 seconds
	pageHTML += '<script>'
	pageHTML += 'setInterval(function() {'
	pageHTML += 'document.location.reload(true);'
	pageHTML+= '}, 15000);'
	pageHTML += '</script>'

	# Conditonal Formatting
	pageHTML += '<script src="cond.js"></script>'

	return pageHTML


def run():
	try:
		# Server settings
		port = 8080
		server_address = '10.163.89.252'
		server_settings = (server_address, port)

		print("Starting Server...")
		httpd = HTTPServer(server_settings, HTTPServer_RequestHandler)

		print("Server Stared on {}:{}".format(server_address,port))
		httpd.serve_forever()

	except KeyboardInterrupt:
		print ('Shutting down the web server')
		httpd.socket.close()
run()