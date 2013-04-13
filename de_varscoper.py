import constants
import sublime
import sublime_plugin
import urllib
import de_util
from xml.dom import minidom
from de_base import LinterBase

class de_varscoperCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = sublime.active_window().active_view()
		self.baseLinter = LinterBase(view)

		if not (".cfc" in view.file_name()):
			return

		absolutePath = util.buildServerPath(view.file_name())

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

				xmlResult = util.httpGet(data=data, headers=headers)
			except Exception as e:
				util.error("Error getting http response : " + str(e))

			try:
				result = self.parseXmlDoc(xmlResult)

				if result["errors"]:
					self.baseLinter.parseErrors(result)
			except Exception as e:
				util.error(str(e))

	def parseXmlDoc(self, xmlResult):
		result = {}
		result["errors"] = []
		result["regions"] = []

		try:
			xmlDoc = minidom.parseString(xmlResult)

			functionNodes =xmlDoc.getElementsByTagName("function")

			for fNode in functionNodes:
				fName = fNode.getAttribute("name")
				fDetail = fNode.firstChild

				fVariable = fDetail.getElementsByTagName("type")[0].firstChild.nodeValue
				fLineNumber = fDetail.getElementsByTagName("line_number")[0].firstChild.nodeValue
				
				errorText = "Function [ %s ] :: Variable [ %s ] " % (fName, fVariable)
				errorCaption = "VarScoper :: %s " % (fLineNumber)

				result["errors"].append(util.returnErrorArray(errorCaption, errorText))
				result["regions"].append(self.baseLinter.getRegion(fLineNumber))

		except Exception as e:
			util.log("Error parsing xml results :: " + str(e))

		return result
	



