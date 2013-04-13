import sublime
import sublime_plugin
import urllib  
import urllib2
import re
from threading import Thread
from xml.dom import minidom

class TestCommand(sublime_plugin.TextCommand):
	LOCALHOST_VARSCOPER_URL = "http://localhost/varscoper/index.cfm"
	VARSCOPER_REGION = "varscoper_region"

	def run(self, edit):
		absolutePath = self.buildServerPath(self.view.file_name())

		if absolutePath is None or absolutePath == "":
			print "Could not locate file in ~/var/websites/"
		else:
			try:
				data = urllib.urlencode({
					"filePath" : absolutePath
					,"displayFormat" : "xml"
					,"recursiveDirectory" : "true"
					,"parseCFScript" : "disabled"
				})

				headers = {
					"Content-Type" : "text/xml"
		    		,"Content-Length": len(data)
				}

				result = self.httpGet(data=data, headers=headers)

				self.parseErrors(result)
			except Exception, e:
				print e

	def httpGet(self, data, headers):
		result = ""

		try:
			proxy_support = urllib2.ProxyHandler({})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)
			http_handler = urllib2.HTTPHandler()
			opener = urllib2.build_opener(http_handler)
			
			request = urllib2.Request(url=self.buidlUrl(self.LOCALHOST_VARSCOPER_URL, data)
				,headers=headers)
			response = urllib2.urlopen(request, "3")

			result = response.read()
		except urllib2.HTTPError, e:
			print ("HTTPError: " + str(e.code))
		except urllib2.URLError, e:
			print ("URLError: " + str(e.reason))

		return result


	# def parseErrors(self, result):
	# 	try:
	# 		xmlDoc = minidom.parseString(result)

	# 		self.errorArray = []
	# 		self.regions = []
	# 		lineNumbers = xmlDoc.getElementsByTagName("line_number")

	# 		if lineNumbers:
	# 			for node in lineNumbers:
	# 				ln = node.firstChild.nodeValue
					
	# 				self.errorArray.append(ln)
	# 				self.regions.append(self.getRegion(ln))

	# 			self.view.add_regions(constants.VARSCOPER_REGION, self.regions, "string")
	# 			self.loadPanel(self.errorArray)

	# 	except Exception as e:
	# 		util.error("Error parsing results : " + str(e))
	
	def parseErrors(self, result):
		try:
			xmlDoc = minidom.parseString(result)

			self.errorArray = []
			self.regions = []
			
			for node in xmlDoc.getElementsByTagName("line_number"):
				ln = node.firstChild.nodeValue
				
				self.errorArray.append(ln)
				self.regions.append(self.getRegion(ln))

			self.view.add_regions(self.VARSCOPER_REGION, self.regions, "string")
			self.loadPanel(self.view.window(), self.errorArray)
		except:
			print "Error parsing results"

	def buildServerPath(self, filePath):
		absolutePath = ""

		relativePath = re.search("websites(.+)", filePath)

		if relativePath:
			absolutePath = "/var/" + relativePath.group()

		return absolutePath

	def buidlUrl(self, url, queryString):
		return url + "?" + queryString
	
	def loadPanel(self, window, errorArray):
		window.show_quick_panel(errorArray, self.gotoLine)

	def getRegion(self, ln):
		point = self.getPoint(ln)
		return self.view.full_line(point)

	def getPoint(self, lineNumber):
		return self.view.text_point(int(lineNumber)-1, 0)

	def gotoLine(self, lineNumber):
		ln = self.errorArray[lineNumber]
		self.view.show(self.getPoint(ln))
	

	
