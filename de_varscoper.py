import constants
import sublime
import sublime_plugin
import urllib  
import urllib2
import re
import util
from threading import Thread
from xml.dom import minidom
from de_base import LinterBase

class VarScoper(LinterBase):	
	def __init__(self, view):
   		super(LinterBase, VarScoper).__init__(view)
		self.view = view

	def run(self):
		if not (".cfc" in self.view.file_name()):
			return

		absolutePath = util.buildServerPath(self.view.file_name())

		if absolutePath is None or absolutePath == "":
			util.error("Could not locate file in ~/var/websites/")
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
			except Exception as e:
				util.error("Error getting http response : " + str(e))

	def httpGet(self, data, headers):
		result = ""

		try:
			proxy_support = urllib2.ProxyHandler({})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)
			http_handler = urllib2.HTTPHandler()
			opener = urllib2.build_opener(http_handler)
			
			request = urllib2.Request(url=util.buidlUrl(constants.LOCALHOST_VARSCOPER_URL, data)
				,headers=headers)
			response = urllib2.urlopen(request, "3")

			result = response.read()
		except urllib2.HTTPError as e:
			util.error("HTTPError: " + str(e.code))
		except urllib2.URLError as e:
			util.error("URLError: " + str(e.reason))

		return result

	def parseErrors(self, result):
		try:
			xmlDoc = minidom.parseString(result)

			self.errorArray = []
			self.regions = []
			lineNumbers = xmlDoc.getElementsByTagName("line_number")

			if lineNumbers:
				for node in lineNumbers:
					ln = node.firstChild.nodeValue
					
					self.errorArray.append(ln)
					self.regions.append(self.getRegion(ln))

				self.view.add_regions(constants.VARSCOPER_REGION, self.regions, "string")
				self.loadPanel(self.errorArray)

		except Exception as e:
			util.error("Error parsing results : " + str(e))
	
