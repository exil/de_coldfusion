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
		# self.errorArr=["ln 15: ","ln 20: "]
		# self.loadPanel(self.view.window(), self.errorArr)

		absolutePath = self.buildServerPath(self.view.file_name())

		if absolutePath is None:
			print "Could not local file in /var/websites/"
		else:
			try:
				# Thread(target=self.httpGet, kwargs={"filePath" : absolutePath}).start()
				self.httpGet(filePath=absolutePath)
			except Exception, e:
				print e

	def httpGet(self, filePath):
		data = urllib.urlencode({
			"filePath" : filePath
			,"displayFormat" : "xml"
			,"recursiveDirectory" : "true"
			,"parseCFScript" : "disabled"
		})

		headers = {
			"Content-Type" : "text/xml"
    		,"Content-Length": len(data)
		}

		try:
			# request = urllib2.Request(url=self.buidlUrl(self.LOCALHOST_VARSCOPER_URL, data)
			# 	,headers=headers)
			# response = urllib2.urlopen(request, "3")

			proxy_support = urllib2.ProxyHandler({})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)
			http_handler = urllib2.HTTPHandler()
			opener = urllib2.build_opener(http_handler)
			
			request = urllib2.Request(url=self.buidlUrl(self.LOCALHOST_VARSCOPER_URL, data)
				,headers=headers)
			response = urllib2.urlopen(request, "3")

			result = response.read()

			xmlDoc = minidom.parseString(result)

			self.errorArray = []
			
			# for node in xmlDoc.getElementsByTagName("function"):
			for node in xmlDoc.getElementsByTagName("line_number"):
				# errorString = "ln " + node.getAttribute("line") + " : " + node.getAttribute("name")
				errorString = node.firstChild.nodeValue
				print node
				self.errorArray.append(errorString)

			self.loadPanel(self.view.window(), self.errorArray)
		except urllib2.HTTPError, e:
			print ("HTTPError: " + str(e.code))
		except urllib2.URLError, e:
			print ("URLError: " + str(e.reason))
		except:
			print ("Cannot locate file in /var/ Or could not parse XML ")

	def buildServerPath(self, filePath):
		absolutePath = ""

		relativePath = re.search("websites(.+)", filePath)

		if relativePath:
			absolutePath = "/var/" + relativePath.group()

		return absolutePath

	def buidlUrl(self, url, queryString):
		return url + "?" + queryString
	
	def loadPanel(self, window, errorArray):
		window.show_quick_panel(errorArray, self.onDone)

	def printTest(self):
		print "test"

	def onDone(self, index):
		print self.errorArray[index]
		point = self.view.text_point(int(self.errorArray[index])-1, 1)
		self.view.show(point)
		self.view.add_regions(self.VARSCOPER_REGION, [self.view.full_line(point)], "string")
	

	
